"""Generate the Pages sitemap and notify IndexNow about changed public articles."""

import argparse
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

HOST = "pathrestore.com"
ORIGIN = f"https://{HOST}"
SITEMAP = f"{ORIGIN}/sitemap.xml"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
ARTICLE_PATH = re.compile(r"resources/[a-z0-9]+(?:-[a-z0-9]+)*\.html")
NOINDEX = re.compile(r"\b(?:noindex|none)\b", re.I)


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = set()
        self.canonicals = []
        self.meta = {}
        self.title = ""
        self.structured_data = ""
        self.capture = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = {name: value or "" for name, value in attrs}
        if tag == "a":
            self.links.add(attrs.get("href", ""))
        elif tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href", ""))
        elif tag == "meta":
            name = attrs.get("name", attrs.get("property", "")).lower()
            self.meta[name] = attrs.get("content", "").strip()
        elif tag == "title":
            self.capture = "title"
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self.capture = "structured_data"

    def handle_endtag(self, tag):
        if tag in {"title", "script"}:
            self.capture = None

    def handle_data(self, data):
        if self.capture:
            setattr(self, self.capture, getattr(self, self.capture) + data)

    def blocks_indexing(self):
        return any(NOINDEX.search(self.meta.get(agent, "")) for agent in ("robots", "googlebot", "bingbot"))


def public_articles(library, read_article):
    articles = {}
    for path in sorted(Page(library).links):
        if not ARTICLE_PATH.fullmatch(path):
            continue
        html = read_article(path)
        page = Page(html)
        if page.blocks_indexing():
            continue
        require(page.canonicals == [f"{ORIGIN}/{path}"], f"{path}: expected an exact HTTPS canonical")
        articles[path] = html
    return articles


def article_data(page):
    return json.loads(page.structured_data) if page.structured_data.strip() else {}


def article_content(html):
    page = Page(html)
    data = article_data(page)
    # Dates alone do not warrant a URL submission.
    data.pop("datePublished", None)
    data.pop("dateModified", None)
    main = re.search(r"<main\b[^>]*>(.*?)</main>", html, re.S)
    return (
        page.title, data,
        {key: value for key, value in page.meta.items() if key == "description" or key.startswith("og:")},
        re.sub(r"\s+", " ", re.sub(r"<!--.*?-->", "", main[1] if main else html, flags=re.S)).strip(),
    )


def require(condition, message):
    if not condition:
        raise ValueError(message)


def generate_sitemap(root):
    sitemap = root / "sitemap.xml"
    tree = ET.parse(sitemap)
    urls = tree.getroot()
    for entry in list(urls):
        if ARTICLE_PATH.fullmatch(urls_path(entry)):
            urls.remove(entry)

    library = (root / "resources.html").read_text(encoding="utf-8")
    for path, html in public_articles(library, lambda name: (root / name).read_text(encoding="utf-8")).items():
        entry = ET.SubElement(urls, NS + "url")
        ET.SubElement(entry, NS + "loc").text = f"{ORIGIN}/{path}"
        data = article_data(Page(html))
        lastmod = data.get("dateModified") or data.get("datePublished")
        if lastmod:
            require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", lastmod), f"{path}: use YYYY-MM-DD for article dates")
            ET.SubElement(entry, NS + "lastmod").text = date.fromisoformat(lastmod).isoformat()

    ET.register_namespace("", NS[1:-1])
    ET.indent(tree, space="  ")
    with sitemap.open("wb") as stream:
        stream.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(stream, encoding="utf-8", xml_declaration=False)
        stream.write(b"\n")


def urls_path(entry):
    return urlsplit(entry.findtext(NS + "loc", "")).path.lstrip("/")


def commit_file(revision, path):
    result = subprocess.run(["git", "show", f"{revision}:{path}"], check=True, capture_output=True, text=True, encoding="utf-8")
    return result.stdout


def fetch_live(url):
    request = Request(url, headers={"Cache-Control": "no-cache"}, method="GET")
    with urlopen(request, timeout=15) as response:
        require(response.status == 200 and response.url == url, f"{url}: expected a direct HTTP 200")
        return response.read(), response.headers


def validate_live(changed):
    sitemap, _ = fetch_live(SITEMAP)
    locations = {entry.text for entry in ET.fromstring(sitemap).iter(NS + "loc")}
    robots, _ = fetch_live(f"{ORIGIN}/robots.txt")
    policy = RobotFileParser()
    policy.parse(robots.decode().splitlines())
    require(SITEMAP in (policy.site_maps() or []), "robots.txt does not reference the production sitemap")
    checked_images = set()
    for path, expected in changed.items():
        url = f"{ORIGIN}/{path}"
        require(url in locations, f"{url}: missing from the live sitemap")
        for crawler in ("Googlebot", "bingbot"):
            require(policy.can_fetch(crawler, url), f"{url}: robots.txt blocks {crawler}")
        html, headers = fetch_live(url)
        html = html.decode().replace("\r\n", "\n")
        require(html == expected, f"{url}: live HTML differs from the deployed commit")
        page = Page(html)
        require(page.canonicals == [url], f"{url}: incorrect HTTPS canonical")
        require(page.title.strip() and page.meta.get("description"), f"{url}: missing title or description")
        require(not page.blocks_indexing(), f"{url}: page requests noindex")
        require(not any(NOINDEX.search(value) for value in headers.get_all("X-Robots-Tag", [])), f"{url}: X-Robots-Tag blocks indexing")
        image = page.meta.get("og:image", "")
        require(urlsplit(image).scheme == "https" and urlsplit(image).netloc == HOST, f"{url}: expected a production HTTPS Open Graph image")
        if image not in checked_images:
            body, image_headers = fetch_live(image)
            require(body and image_headers.get_content_type().startswith("image/"), f"{image}: expected an accessible image")
            checked_images.add(image)
        print(f"Validated {url}", flush=True)


def notify(previous_sha):
    old = public_articles(commit_file(previous_sha, "resources.html"), lambda path: commit_file(previous_sha, path))
    current = public_articles(commit_file("HEAD", "resources.html"), lambda path: commit_file("HEAD", path))
    changed = {
        path: html for path, html in current.items()
        if path not in old or article_content(html) != article_content(old[path])
    }
    if not changed:
        print("No new or materially changed public articles.")
        return

    keys = [path for path in Path.cwd().glob("*.txt") if re.fullmatch(r"[a-f0-9]{32}", path.stem)]
    require(len(keys) == 1, "Expected one root IndexNow key file")
    key_file = keys[0]
    key_location = f"{ORIGIN}/{key_file.name}"
    require(key_file.read_text(encoding="utf-8").strip() == key_file.stem, "IndexNow key file does not match its filename")

    # Allow a short window for the new Pages deployment to reach the public CDN.
    for attempt in range(3):
        try:
            validate_live(changed)
            live_key, _ = fetch_live(key_location)
            require(live_key.decode().strip() == key_file.stem, "Live IndexNow key file has unexpected contents")
            break
        except (ValueError, URLError, TimeoutError, ET.ParseError) as error:
            if attempt == 2:
                raise
            print(f"Live validation attempt {attempt + 1} failed: {error}. Retrying in 10 seconds.", flush=True)
            time.sleep(10)

    payload = {"host": HOST, "key": key_file.stem, "keyLocation": key_location,
               "urlList": [f"{ORIGIN}/{path}" for path in changed]}
    request = Request("https://api.indexnow.org/indexnow", data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urlopen(request, timeout=15) as response:
        require(response.status in {200, 202}, f"Unexpected IndexNow response: HTTP {response.status}")
        print(f"IndexNow received {len(changed)} article URL(s): HTTP {response.status}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["sitemap", "notify"])
    parser.add_argument("target", help="Site artifact directory or previous successful commit SHA")
    args = parser.parse_args()
    try:
        if args.command == "sitemap":
            generate_sitemap(Path(args.target))
        else:
            notify(args.target)
    except (OSError, ValueError, ET.ParseError, subprocess.CalledProcessError) as error:
        sys.exit(f"Search discovery failed: {error}")
