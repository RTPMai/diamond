#!/usr/bin/env python3
"""
Pre-flight checks for the built site. Run against site/ after build.py.

  python3 build.py && python3 verify.py
"""

import json
import os
import re
import sys

OUT = "site"
REQUIRED = [
    "index.html",
    "how-it-works.html",
    "services.html",
    "pricing.html",
    "robots.txt",
    "sitemap.xml",
    "llms.txt",
    "vercel.json",
]

fails = []
warns = []


def fail(msg):
    fails.append(msg)


def warn(msg):
    warns.append(msg)


def read(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return f.read()


# required files -------------------------------------------------------------
for f in REQUIRED:
    if not os.path.exists(os.path.join(OUT, f)):
        fail("missing file: " + f)

if fails:
    for f in fails:
        print("FAIL", f)
    sys.exit(1)

pages = [p for p in REQUIRED if p.endswith(".html")]
titles = {}

for p in pages:
    html = read(p)

    # single H1
    h1s = re.findall(r"<h1[ >]", html)
    if len(h1s) != 1:
        fail("%s has %d <h1> tags, expected 1" % (p, len(h1s)))

    # title present and unique
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m:
        fail("%s has no <title>" % p)
    else:
        t = m.group(1).strip()
        if t in titles:
            fail("duplicate title on %s and %s" % (p, titles[t]))
        titles[t] = p
        if len(t) > 62:
            warn("%s title is %d chars, may truncate in results" % (p, len(t)))

    # meta description
    md = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
    if not md:
        fail("%s has no meta description" % p)
    elif len(md.group(1)) > 165:
        warn("%s meta description is %d chars" % (p, len(md.group(1))))

    # canonical
    if 'rel="canonical"' not in html:
        fail("%s has no canonical" % p)

    # JSON-LD parses
    for block in re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S
    ):
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            fail("%s has invalid JSON-LD: %s" % (p, e))

    # no placeholder links
    if 'href="#"' in html:
        fail("%s has a placeholder href=\"#\"" % p)

    # no accidental noindex
    if "noindex" in html:
        fail("%s contains noindex" % p)

    # external links carry rel=noopener
    for tag in re.findall(r"<a [^>]*https?://[^>]*>", html):
        if "fonts.googleapis" in tag or "fonts.gstatic" in tag:
            continue
        if 'target="_blank"' in tag and "noopener" not in tag:
            fail("%s external link missing rel=noopener: %s" % (p, tag[:70]))

    # internal links must be extensionless
    for href in re.findall(r'href="(/[^"]*)"', html):
        if href.endswith(".html"):
            fail("%s links to %s, should be extensionless" % (p, href))

    # phone link present
    if "tel:+15158773867" not in html:
        fail("%s is missing the tel: link" % p)

# sitemap membership ---------------------------------------------------------
sm = read("sitemap.xml")
expected_urls = ["/", "/how-it-works", "/services", "/pricing"]
for u in expected_urls:
    if "diamonddumpstersolutions.com%s<" % u not in sm.replace("www.", "www."):
        if not re.search(re.escape(u) + r"</loc>", sm):
            fail("sitemap missing " + u)

# robots ---------------------------------------------------------------------
rb = read("robots.txt")
if "Sitemap:" not in rb:
    fail("robots.txt has no Sitemap line")
for bot in ["GPTBot", "ClaudeBot", "PerplexityBot", "OAI-SearchBot"]:
    if bot not in rb:
        warn("robots.txt does not mention " + bot)

# vercel.json sync -----------------------------------------------------------
with open(os.path.join(OUT, "vercel.json"), encoding="utf-8") as f:
    inner = json.load(f)
if os.path.exists("vercel.json"):
    with open("vercel.json", encoding="utf-8") as f:
        root = json.load(f)
    if inner != root:
        fail("root vercel.json and site/vercel.json are out of sync")
else:
    warn("no repo-root vercel.json")

if inner.get("cleanUrls") is not True:
    fail("vercel.json cleanUrls is not true")

# report ---------------------------------------------------------------------
for w in warns:
    print("WARN", w)
for f in fails:
    print("FAIL", f)

if fails:
    print("\n%d failure(s)." % len(fails))
    sys.exit(1)

print("\nOK - %d pages, %d warning(s)." % (len(pages), len(warns)))
