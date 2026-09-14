#!/usr/bin/env python3
"""
Diamond Dumpster Solutions - static site generator.

Run:  python3 build.py
Out:  site/

build.py is the source of truth. Never edit site/ directly.
"""

import os
import shutil
import json

# ---------------------------------------------------------------------------
# CONSTANTS - change these here, they propagate sitewide
# ---------------------------------------------------------------------------

SITE_URL = "https://www.diamonddumpstersolutions.com"
BUSINESS = "Diamond Dumpster Solutions"
TAGLINE = "Roll-off dumpster rental in the Des Moines metro"

PHONE_DISPLAY = "515-877-DUMP"
PHONE_SPOKEN = "(515) 877-3867"
PHONE_TEL = "+15158773867"

BOOK_URL = "https://form.jotform.com/241194632319153"
BOOK_LABEL = "Book a dumpster"

SIZE_YARDS = "30 yard"
PRICE_WEEK = 400
PRICE_WEEK_DISPLAY = "$400"

# Trim this list to the towns they actually deliver to.
SERVICE_AREA = [
    "Des Moines", "West Des Moines", "Ankeny", "Urbandale", "Johnston",
    "Clive", "Waukee", "Grimes", "Altoona", "Pleasant Hill", "Bondurant",
    "Polk City", "Norwalk", "Indianola", "Carlisle", "Adel", "Dallas Center",
    "Granger", "Elkhart", "Mitchellville", "Windsor Heights", "Huxley",
]

OUT = "site"

# ---------------------------------------------------------------------------
# STYLE
# ---------------------------------------------------------------------------

CSS = """
:root{
  --ink:#14242E;
  --ink-2:#1C3140;
  --steel:#2A4150;
  --paper:#EDEFF0;
  --white:#FFFFFF;
  --orange:#F04E23;
  --muted:#8399A5;
  --line:rgba(255,255,255,.14);
  --line-dark:rgba(20,36,46,.16);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;
  background:var(--paper);
  color:var(--ink);
  font-family:Archivo,"Helvetica Neue",Arial,sans-serif;
  font-size:17px;
  line-height:1.6;
  font-synthesis-weight:none;
}
img{max-width:100%;display:block}
a{color:inherit}

.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
.narrow{max-width:660px;margin:0}

/* hazard band ---------------------------------------------------------- */
.band{
  height:14px;
  background:repeating-linear-gradient(
    -45deg, var(--orange) 0 14px, var(--ink) 14px 28px
  );
}

/* header --------------------------------------------------------------- */
header{background:var(--ink);color:var(--white)}
.bar{display:flex;align-items:center;gap:24px;padding:18px 0;flex-wrap:wrap}
.mark{
  font-weight:800;letter-spacing:-.02em;font-size:20px;line-height:1;
  text-decoration:none;display:flex;align-items:center;gap:9px;
}
.mark span{color:var(--orange)}
nav{margin-left:auto;display:flex;align-items:center;gap:26px;flex-wrap:wrap}
nav a{
  text-decoration:none;font-size:15px;font-weight:500;color:var(--paper);
  padding:4px 0;border-bottom:2px solid transparent;
}
nav a:hover,nav a:focus-visible{border-bottom-color:var(--orange)}
nav a[aria-current="page"]{border-bottom-color:var(--orange)}
.calllink{font-weight:700;color:var(--white);white-space:nowrap}

/* buttons -------------------------------------------------------------- */
.btn{
  display:inline-block;background:var(--orange);color:var(--white);
  text-decoration:none;font-weight:700;font-size:16px;
  padding:15px 26px;border:0;letter-spacing:.01em;
}
.btn:hover,.btn:focus-visible{background:#D33F16}
.btn-ghost{
  display:inline-block;text-decoration:none;font-weight:700;font-size:16px;
  padding:14px 25px;border:2px solid currentColor;color:var(--white);
}
.btn-ghost:hover,.btn-ghost:focus-visible{background:rgba(255,255,255,.1)}
a:focus-visible,button:focus-visible{outline:3px solid var(--orange);outline-offset:3px}

/* hero ----------------------------------------------------------------- */
.hero{background:var(--ink);color:var(--white);padding:76px 0 68px}
.hero h1{
  font-size:clamp(52px,12.5vw,138px);
  font-weight:800;line-height:.86;letter-spacing:-.035em;
  margin:0;text-transform:uppercase;
}
.hero .sub{
  margin:26px 0 0;max-width:34ch;font-size:clamp(18px,2.2vw,22px);
  color:var(--paper);line-height:1.45;
}
.hero .acts{display:flex;gap:14px;margin-top:34px;flex-wrap:wrap}

/* page head for interior pages ----------------------------------------- */
.phead{background:var(--ink);color:var(--white);padding:56px 0 50px}
.phead h1{
  font-size:clamp(38px,6.5vw,68px);font-weight:800;line-height:.95;
  letter-spacing:-.03em;margin:0;text-transform:uppercase;
}
.phead p{margin:18px 0 0;max-width:52ch;color:var(--paper);font-size:18px}

/* sections ------------------------------------------------------------- */
section{padding:66px 0}
section.tight{padding:48px 0}
section.dark{background:var(--ink);color:var(--white)}
h2{
  font-size:clamp(27px,3.6vw,40px);font-weight:800;letter-spacing:-.02em;
  line-height:1.08;margin:0 0 22px;
}
h3{font-size:20px;font-weight:700;letter-spacing:-.01em;margin:0 0 8px}
p{max-width:68ch}
.lede{font-size:19px;max-width:60ch}

/* reasons: three stacked rules, not cards ------------------------------ */
.reasons{margin:34px 0 0;border-top:1px solid var(--line-dark)}
.reason{
  display:grid;grid-template-columns:1fr 2fr;gap:28px;
  padding:26px 0;border-bottom:1px solid var(--line-dark);
}
.reason h3{margin:0}
.reason p{margin:0;color:var(--steel)}
section.dark .reason{border-color:var(--line)}
section.dark .reason p{color:var(--paper)}

/* steps: a real sequence, so numbered ---------------------------------- */
.steps{counter-reset:s;margin:34px 0 0;padding:0;list-style:none}
.steps li{
  counter-increment:s;position:relative;padding:0 0 28px 66px;
  border-left:2px solid var(--line-dark);margin-left:20px;
}
.steps li:last-child{border-left-color:transparent;padding-bottom:0}
.steps li::before{
  content:counter(s);position:absolute;left:-21px;top:-4px;
  width:40px;height:40px;background:var(--orange);color:var(--white);
  font-weight:800;font-size:18px;display:grid;place-items:center;
}
.steps h3{margin:6px 0 6px}
.steps p{margin:0;color:var(--steel)}

/* price slab ----------------------------------------------------------- */
.slab{background:var(--ink);color:var(--white);padding:44px;max-width:560px}
.slab .size{font-size:20px;font-weight:700;margin:0}
.slab .fig{
  font-size:clamp(66px,13vw,104px);font-weight:800;line-height:.9;
  letter-spacing:-.04em;margin:10px 0 0;
}
.slab .per{font-size:17px;color:var(--muted);margin:10px 0 0}
.slab .dims{margin:22px 0 0;color:var(--paper);font-size:16px}
.slab .btn{margin-top:28px}

.note{border-left:3px solid var(--orange);padding:4px 0 4px 20px;margin:34px 0 0}
.note p{margin:0}

/* service list --------------------------------------------------------- */
.jobs{margin:34px 0 0;padding:0;list-style:none;
  display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1px;
  background:var(--line-dark)}
.jobs li{background:var(--paper);padding:26px 24px 28px}
.jobs p{margin:0;color:var(--steel);font-size:16px}

/* towns ---------------------------------------------------------------- */
.towns{margin:26px 0 0;padding:0;list-style:none;
  display:flex;flex-wrap:wrap;gap:8px 10px}
.towns li{font-size:15px;color:var(--paper);
  border:1px solid var(--line);padding:6px 12px}

/* faq ------------------------------------------------------------------ */
.faq{margin:34px 0 0;border-top:1px solid var(--line-dark)}
.faq details{border-bottom:1px solid var(--line-dark)}
.faq summary{
  cursor:pointer;padding:20px 0;font-weight:700;font-size:18px;
  list-style:none;display:flex;justify-content:space-between;gap:20px;
}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--orange);font-weight:800}
.faq details[open] summary::after{content:"\\2013"}
.faq .ans{padding:0 0 22px;color:var(--steel)}
.faq .ans p{margin:0 0 10px}
.faq .ans p:last-child{margin:0}

/* closing cta ---------------------------------------------------------- */
.cta{background:var(--ink);color:var(--white);padding:66px 0;
  border-top:1px solid var(--line)}
.cta h2{margin:0 0 14px}
.cta p{color:var(--paper);margin:0 0 30px}
.cta .acts{display:flex;gap:14px;flex-wrap:wrap}

/* footer --------------------------------------------------------------- */
footer{background:var(--ink);color:var(--muted);padding:40px 0 100px;
  border-top:1px solid var(--line);font-size:15px}
footer a{color:var(--paper)}
.fgrid{display:flex;gap:40px;flex-wrap:wrap;justify-content:space-between}
footer .fnav{display:flex;gap:20px;flex-wrap:wrap}

/* sticky call bar, mobile only ----------------------------------------- */
.callbar{
  position:fixed;left:0;right:0;bottom:0;z-index:20;display:none;
  background:var(--orange);color:var(--white);text-decoration:none;
  font-weight:800;font-size:18px;text-align:center;padding:16px 0;
}
@media (max-width:760px){
  .callbar{display:block}
  .reason{grid-template-columns:1fr;gap:6px}
  .bar{gap:14px}
  nav{gap:18px;margin-left:0;width:100%}
  .slab{padding:30px 26px}
  section{padding:52px 0}
}
@media (prefers-reduced-motion:reduce){
  *{animation:none !important;transition:none !important}
}
.skip{position:absolute;left:-9999px}
.skip:focus{left:24px;top:12px;position:fixed;z-index:50;background:var(--orange);
  color:#fff;padding:12px 18px;font-weight:700}
"""

# ---------------------------------------------------------------------------
# SCHEMA
# ---------------------------------------------------------------------------

BIZ_ID = SITE_URL + "/#business"

BUSINESS_SCHEMA = {
    "@type": "LocalBusiness",
    "@id": BIZ_ID,
    "name": BUSINESS,
    "url": SITE_URL + "/",
    "telephone": PHONE_TEL,
    "description": (
        "Roll-off dumpster rental for homeowners and contractors in Des Moines "
        "and the surrounding metro. Flat weekly pricing, scheduled delivery "
        "and pickup, responsible disposal."
    ),
    "areaServed": [
        {"@type": "City", "name": t, "addressRegion": "IA"} for t in SERVICE_AREA
    ],
    "priceRange": "$$",
    "makesOffer": {
        "@type": "Offer",
        "name": SIZE_YARDS + " roll-off dumpster, one week rental",
        "price": str(PRICE_WEEK),
        "priceCurrency": "USD",
        "availability": "https://schema.org/InStock",
        "url": SITE_URL + "/pricing",
        "itemOffered": {
            "@type": "Service",
            "name": SIZE_YARDS + " roll-off dumpster rental",
            "serviceType": "Dumpster rental",
            "provider": {"@id": BIZ_ID},
        },
    },
}


def jsonld(*nodes):
    graph = {"@context": "https://schema.org", "@graph": list(nodes)}
    return (
        '<script type="application/ld+json">'
        + json.dumps(graph, separators=(",", ":"))
        + "</script>"
    )


# ---------------------------------------------------------------------------
# SHELL
# ---------------------------------------------------------------------------

NAV = [
    ("/", "Home"),
    ("/how-it-works", "How it works"),
    ("/services", "Services"),
    ("/pricing", "Pricing"),
]


def nav_html(current):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        out.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    out.append(
        '<a class="calllink" href="tel:%s">%s</a>' % (PHONE_TEL, PHONE_SPOKEN)
    )
    return "".join(out)


def page(path, title, description, body, schema_extra=None, current=None):
    canonical = SITE_URL + (path if path != "/" else "/")
    nodes = [BUSINESS_SCHEMA]
    if schema_extra:
        nodes.extend(schema_extra)

    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{business}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#14242E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>{css}</style>
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="wrap bar">
    <a class="mark" href="/">Diamond <span>Dumpster</span> Solutions</a>
    <nav>{nav}</nav>
  </div>
</header>
<div class="band"></div>
<main id="main">
{body}
</main>
<div class="band"></div>
<footer>
  <div class="wrap fgrid">
    <div>
      <p style="margin:0 0 6px"><strong style="color:var(--white)">{business}</strong></p>
      <p style="margin:0">Roll-off dumpster rental, Des Moines metro.<br>
      <a href="tel:{tel}">{phone_spoken}</a></p>
    </div>
    <div class="fnav">{fnav}</div>
  </div>
</footer>
<a class="callbar" href="tel:{tel}">Call {phone_spoken}</a>
</body>
</html>
""".format(
        title=title,
        description=description,
        canonical=canonical,
        business=BUSINESS,
        css=CSS,
        schema=jsonld(*nodes),
        nav=nav_html(current if current is not None else path),
        body=body,
        tel=PHONE_TEL,
        phone_spoken=PHONE_SPOKEN,
        fnav="".join(
            '<a href="%s">%s</a>' % (h, l) for h, l in NAV
        )
        + '<a href="%s">Book now</a>' % BOOK_URL,
    )
    return html


def closing_cta(heading, line):
    return """
<div class="cta">
  <div class="wrap">
    <h2>{h}</h2>
    <p>{l}</p>
    <div class="acts">
      <a class="btn" href="{book}">{book_label}</a>
      <a class="btn-ghost" href="tel:{tel}">Call {phone}</a>
    </div>
  </div>
</div>
""".format(
        h=heading,
        l=line,
        book=BOOK_URL,
        book_label=BOOK_LABEL,
        tel=PHONE_TEL,
        phone=PHONE_SPOKEN,
    )


# ---------------------------------------------------------------------------
# PAGES
# ---------------------------------------------------------------------------

def home():
    towns = "".join("<li>%s</li>" % t for t in SERVICE_AREA)
    body = """
<div class="hero">
  <div class="wrap">
    <h1>We love<br>a good dump.</h1>
    <p class="sub">Roll-off dumpsters delivered across the Des Moines metro. One price, one week, no surprises.</p>
    <div class="acts">
      <a class="btn" href="{book}">{book_label}</a>
      <a class="btn-ghost" href="tel:{tel}">Call {phone}</a>
    </div>
  </div>
</div>

<section>
  <div class="wrap">
    <h2>Renovation, cleanout, job site. Same dumpster.</h2>
    <p class="lede">We rent {size} roll-off containers to homeowners and contractors around Des Moines. Tell us where it goes and when you need it gone.</p>
    <div class="reasons">
      <div class="reason">
        <h3>Pricing you can read</h3>
        <p>{price} for a week, and free delivery in the Des Moines area. That number is on the pricing page, not behind a quote form. No fuel surcharge, no hidden fees.</p>
      </div>
      <div class="reason">
        <h3>Delivered and picked up on schedule</h3>
        <p>We agree on a drop day and a pickup day, and we hit them. If your project slides, call us and we will move it.</p>
      </div>
      <div class="reason">
        <h3>Sorted, not just buried</h3>
        <p>Loads go to licensed facilities and we recycle what can be recycled instead of sending the whole container to a landfill.</p>
      </div>
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <h2>Where we deliver</h2>
    <p style="color:var(--paper);max-width:58ch">Des Moines and the surrounding metro. Outside this list, call us. If we can get a truck there, we will.</p>
    <ul class="towns">{towns}</ul>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{size}. {price} a week.</h2>
    <div class="slab">
      <p class="size">{size} roll-off</p>
      <p class="fig">{price}</p>
      <p class="per">per week, delivery and pickup included</p>
      <p class="dims">Enough room for a full kitchen and bath gut, a garage cleanout, or a small roof tear-off.</p>
      <a class="btn" href="{book}">{book_label}</a>
    </div>
    <div class="note">
      <p>Running a job longer than a week, or need containers swapped on a commercial site? Call for contractor pricing.</p>
    </div>
  </div>
</section>
{cta}
""".format(
        book=BOOK_URL,
        book_label=BOOK_LABEL,
        tel=PHONE_TEL,
        phone=PHONE_SPOKEN,
        size=SIZE_YARDS,
        price=PRICE_WEEK_DISPLAY,
        towns=towns,
        cta=closing_cta(
            "Ready when you are",
            "Book online in about two minutes, or call and we will sort it out over the phone.",
        ),
    )

    website = {
        "@type": "WebSite",
        "@id": SITE_URL + "/#website",
        "url": SITE_URL + "/",
        "name": BUSINESS,
        "publisher": {"@id": BIZ_ID},
    }

    return page(
        "/",
        "Dumpster Rental in Des Moines | " + BUSINESS,
        "Roll-off dumpster rental in Des Moines and the surrounding metro. "
        + SIZE_YARDS
        + " containers, "
        + PRICE_WEEK_DISPLAY
        + " per week, delivery and pickup included.",
        body,
        schema_extra=[website],
    )


HOW_FAQ = [
    (
        "How much space do I need for the dumpster?",
        "Plan on a clear stretch of driveway roughly 22 feet long and 10 feet wide, "
        "with open sky above it. The truck needs room to back in and tilt the "
        "container off, so no low branches, carports or power lines over the spot.",
    ),
    (
        "Will it damage my driveway?",
        "We set containers down carefully, but any heavy steel box on asphalt can "
        "leave marks. If you are worried about it, lay down plywood where the "
        "rails will sit and tell us when you book so the driver knows.",
    ),
    (
        "What can I put in it?",
        "General construction debris, demolition material, furniture, carpet, "
        "household junk, yard waste and roofing. Load it level with the top rail "
        "so it can be tarped and hauled legally.",
    ),
    (
        "What can't I put in it?",
        "Paint, chemicals, fuel, oil, batteries, tires, asbestos and anything else "
        "classed as hazardous waste. Appliances with refrigerant and some "
        "electronics also need separate handling. If you are not sure about "
        "something, call before you throw it in.",
    ),
    (
        "Do I need to be home for delivery?",
        "No, as long as we know exactly where the container goes and the spot is "
        "clear. Mark it with a cone or a bit of tape if it helps.",
    ),
    (
        "What if I need it longer than a week?",
        "Call us before the pickup date and we will extend it. Longer rentals and "
        "repeat swaps on commercial jobs are priced separately.",
    ),
]


def how_it_works():
    faq_html = "".join(
        """<details><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>"""
        .format(q=q, a=a)
        for q, a in HOW_FAQ
    )

    body = """
<div class="phead">
  <div class="wrap">
    <h1>How it works</h1>
    <p>Quote, drop-off, fill it, gone. We handle the ends, you handle the middle.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="narrow">
    <ol class="steps">
      <li>
        <h3>Reach out for a quote</h3>
        <p>Book online or call. We will get back to you in a timely manner.</p>
      </li>
      <li>
        <h3>Schedule a drop-off</h3>
        <p>Tell us when and where you need the dumpster delivered. Delivery is free in the Des Moines area.</p>
      </li>
      <li>
        <h3>Load your dumpster</h3>
        <p>Fill it at your convenience. Need more time, or another dumpster? Just call us.</p>
      </li>
      <li>
        <h3>Hassle-free cleanup</h3>
        <p>Once you are finished, we take care of the rest.</p>
      </li>
    </ol>
    </div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="narrow">
    <h2>Common questions</h2>
    <div class="faq">{faq}</div>
    </div>
  </div>
</section>
{cta}
""".format(
        faq=faq_html,
        cta=closing_cta(
            "Book your week",
            "Pick a delivery day and we will take it from there.",
        ),
    )

    faq_schema = {
        "@type": "FAQPage",
        "@id": SITE_URL + "/how-it-works#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in HOW_FAQ
        ],
    }

    return page(
        "/how-it-works",
        "How Dumpster Rental Works | " + BUSINESS,
        "Quote, drop-off, loading and pickup explained, plus what fits in a "
        + SIZE_YARDS
        + " roll-off and what has to stay out of it.",
        body,
        schema_extra=[faq_schema],
    )


JOBS = [
    (
        "Residential dumpster rentals",
        "Home renovations, cleanouts, moving, or any household project that "
        "generates more waste than the curb will take.",
    ),
    (
        "Commercial dumpster rentals",
        "Businesses, construction sites and industrial facilities that need "
        "larger containers or waste hauled on a regular schedule.",
    ),
]


def services():
    jobs_html = "".join(
        "<li><h3>%s</h3><p>%s</p></li>" % (t, d) for t, d in JOBS
    )

    body = """
<div class="phead">
  <div class="wrap">
    <h1>Services</h1>
    <p>Two ways we work: one driveway at a time, or a site that needs it handled all year.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <h2>What we rent</h2>
    <p class="lede">A {size} roll-off handles roughly the debris of a full kitchen and bath gut, or a garage you have been ignoring for a decade. Delivery is free in the Des Moines area.</p>
    <ul class="jobs">{jobs}</ul>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <h2>Need it longer, or need another one?</h2>
    <p style="color:var(--paper);max-width:58ch">Call us. Extensions, second containers and regular swaps on a commercial site are all handled over the phone, and priced for the length of the job rather than the week.</p>
    <p style="margin-top:26px"><a class="btn" href="tel:{tel}">Call {phone}</a></p>
  </div>
</section>
{cta}
""".format(
        size=SIZE_YARDS,
        jobs=jobs_html,
        tel=PHONE_TEL,
        phone=PHONE_SPOKEN,
        cta=closing_cta(
            "Get one on site",
            "Book a delivery day online, or call if your job needs something custom.",
        ),
    )

    return page(
        "/services",
        "Dumpster Rental Services | " + BUSINESS,
        "Residential and commercial roll-off dumpster rental across the Des Moines "
        "metro. Renovations, cleanouts, moving, construction sites and industrial waste.",
        body,
    )


def pricing():
    body = """
<div class="phead">
  <div class="wrap">
    <h1>Pricing</h1>
    <p>One size, one number, printed where you can find it.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="slab">
      <p class="size">{size} roll-off, short term</p>
      <p class="fig">{price}</p>
      <p class="per">per week, delivery and pickup included</p>
      <p class="dims">Enough for a full kitchen and bath gut, a garage cleanout, or a small roof tear-off.</p>
      <a class="btn" href="{book}">{book_label}</a>
    </div>

    <div class="note">
      <p>Loads have to sit level with the top rail and stay clear of hazardous material. Anything beyond that, we will tell you before we haul it, not after.</p>
    </div>
  </div>
</section>

<section class="dark tight">
  <div class="wrap">
    <h2>Long term, commercial and contractor</h2>
    <p style="color:var(--paper);max-width:58ch">Multi-week rentals, standing containers and scheduled swaps are priced per job. Call {phone} and we will work it out in one conversation.</p>
  </div>
</section>
{cta}
""".format(
        size=SIZE_YARDS,
        price=PRICE_WEEK_DISPLAY,
        book=BOOK_URL,
        book_label=BOOK_LABEL,
        phone=PHONE_SPOKEN,
        cta=closing_cta(
            "Book it",
            "Pick your delivery day and the container shows up.",
        ),
    )

    offer_page = {
        "@type": "Product",
        "@id": SITE_URL + "/pricing#offer",
        "name": SIZE_YARDS + " roll-off dumpster rental",
        "description": (
            "One week rental of a "
            + SIZE_YARDS
            + " roll-off dumpster in the Des Moines metro, delivery and pickup included."
        ),
        "brand": {"@id": BIZ_ID},
        "offers": {
            "@type": "Offer",
            "price": str(PRICE_WEEK),
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": SITE_URL + "/pricing",
            "seller": {"@id": BIZ_ID},
        },
    }

    return page(
        "/pricing",
        "Dumpster Prices in Des Moines | " + BUSINESS,
        SIZE_YARDS
        + " roll-off dumpster rental for "
        + PRICE_WEEK_DISPLAY
        + " per week in the Des Moines metro. Delivery and pickup included, no hidden fees.",
        body,
        schema_extra=[offer_page],
    )


# ---------------------------------------------------------------------------
# SUPPORT FILES
# ---------------------------------------------------------------------------

ROBOTS = """User-agent: *
Allow: /
Disallow: /api/

# Answer engines are welcome to read and cite this site.
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: {site}/sitemap.xml
""".format(site=SITE_URL)


def sitemap():
    urls = ["/", "/how-it-works", "/services", "/pricing"]
    items = "".join(
        "<url><loc>%s%s</loc><changefreq>monthly</changefreq></url>" % (SITE_URL, u)
        for u in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + items
        + "</urlset>"
    )


LLMS_TXT = """# {business}

> Roll-off dumpster rental serving Des Moines, Iowa and the surrounding metro.

## Facts
- Service: {size} roll-off dumpster rental, delivered and picked up.
- Price: {price} per week, delivery and pickup included. No fuel surcharge or hidden fees.
- Delivery is free in the Des Moines area.
- Two service lines: residential (renovations, cleanouts, moving) and commercial
  (businesses, construction sites, industrial facilities needing regular service).
- Extensions and additional containers are arranged by phone.
- Longer rentals, standing containers and contractor swaps are priced per job by phone.
- Phone: {phone}
- Booking: {book}
- Service area: {area}.
- Not accepted: paint, chemicals, fuel, oil, batteries, tires, asbestos, and other
  hazardous waste. Appliances with refrigerant and some electronics need separate handling.
- Space needed for delivery: about 22 feet of clear driveway, 10 feet wide, with open sky above.

## Pages
- [Home]({site}/): overview and service area
- [How it works]({site}/how-it-works): booking, delivery, loading, pickup, and common questions
- [Services]({site}/services): residential and commercial dumpster rental
- [Pricing]({site}/pricing): current rates
""".format(
    business=BUSINESS,
    size=SIZE_YARDS,
    price=PRICE_WEEK_DISPLAY,
    phone=PHONE_SPOKEN,
    book=BOOK_URL,
    area=", ".join(SERVICE_AREA),
    site=SITE_URL,
)

VERCEL_JSON = {
    "cleanUrls": True,
    "trailingSlash": False,
    "redirects": [
        {"source": "/home", "destination": "/", "permanent": True},
        {"source": "/index.html", "destination": "/", "permanent": True},
        {"source": "/_/:path*", "destination": "/", "permanent": False},
        {"source": "/system/:path*", "destination": "/", "permanent": False},
    ],
    "headers": [
        {
            "source": "/(.*)",
            "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            ],
        }
    ],
}


# ---------------------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("  wrote", full)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    print("building %s ..." % BUSINESS)
    write("index.html", home())
    write("how-it-works.html", how_it_works())
    write("services.html", services())
    write("pricing.html", pricing())
    write("robots.txt", ROBOTS)
    write("sitemap.xml", sitemap())
    write("llms.txt", LLMS_TXT)
    write("vercel.json", json.dumps(VERCEL_JSON, indent=2))

    # Vercel reads site/vercel.json (Root Directory = site/). Keep the repo
    # root copy in sync so the two never drift.
    with open("vercel.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(VERCEL_JSON, indent=2))
    print("  wrote vercel.json (repo root, mirror)")

    print("done.")


if __name__ == "__main__":
    main()
