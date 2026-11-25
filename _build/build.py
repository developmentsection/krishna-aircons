# -*- coding: utf-8 -*-
"""
Static site generator for krishnaaircons.com
Usage (from the project root):   python3 _build/build.py
Writes all HTML pages + sitemap.xml + robots.txt into the project root.
"""
import html
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import SITE, SERVICES, AREAS, BLOG  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()
BS_CSS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
BS_JS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
BI_CSS = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"

AREA_BY_SLUG = {a["slug"]: a for a in AREAS}
SITEMAP = []  # (path, priority)


def esc(s):
    return html.escape(s, quote=True)


def area_path(a):
    return f"areas/ac-repair-service-{a['slug']}/"


def service_path(s):
    return f"services/{s['slug']}/"


def blog_path(b):
    return f"blog/{b['slug']}/"


def wa_link(text="Hi Krishna Aircons, I need AC service."):
    from urllib.parse import quote
    return f"https://wa.me/{SITE['whatsapp']}?text={quote(text)}"


# --------------------------------------------------------------------------
# Social / review links with brand logos
# --------------------------------------------------------------------------
GOOGLE_G = ('<svg class="g-logo" viewBox="0 0 48 48" width="18" height="18" aria-hidden="true">'
            '<path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/>'
            '<path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>'
            '<path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/>'
            '<path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>')
JD_LOGO = ('<svg class="jd-logo" viewBox="0 0 32 32" width="18" height="18" aria-hidden="true">'
           '<rect width="32" height="32" rx="7" fill="#FF6600"/>'
           '<text x="16" y="21.5" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" fill="#fff">Jd</text></svg>')


def social_list():
    return [
        ("facebook", "Facebook", SITE["facebook"], '<i class="bi bi-facebook" aria-hidden="true"></i>'),
        ("instagram", "Instagram", SITE["instagram"], '<i class="bi bi-instagram" aria-hidden="true"></i>'),
        ("linkedin", "LinkedIn", SITE["linkedin"], '<i class="bi bi-linkedin" aria-hidden="true"></i>'),
        ("gmaps", "Google Maps", SITE["maps_url"], '<i class="bi bi-geo-alt-fill" aria-hidden="true"></i>'),
        ("justdial", "Justdial", SITE["justdial"], JD_LOGO),
    ]


def social_icons(extra_class=""):
    items = "".join(
        f'<a class="social-btn s-{k}" href="{u}" target="_blank" rel="noopener" aria-label="Krishna Aircons on {n}" title="{n}">{icon}</a>'
        for k, n, u, icon in social_list() if u)
    return f'<div class="social-icons {extra_class}">{items}</div>'


def review_buttons(dark=False):
    cls = " review-btns-dark" if dark else ""
    return f"""<div class="review-btns{cls}">
  <a class="review-btn rb-google" href="{SITE['review_url']}" target="_blank" rel="noopener">{GOOGLE_G}<span>Review us on Google</span></a>
  <a class="review-btn rb-jd" href="{SITE['justdial_review']}" target="_blank" rel="noopener">{JD_LOGO}<span>Rate us on Justdial</span></a>
</div>"""


def find_us_online():
    rows = "".join(
        f'<a class="online-row s-{k}" href="{u}" target="_blank" rel="noopener"><span class="online-icon">{icon}</span><span>{n}</span><i class="bi bi-box-arrow-up-right ms-auto" aria-hidden="true"></i></a>'
        for k, n, u, icon in social_list() if u)
    return f'<div class="online-list">{rows}</div>'


# --------------------------------------------------------------------------
# Structured data
# --------------------------------------------------------------------------
def business_schema():
    same_as = [u for u in (SITE["facebook"], SITE["instagram"], SITE["linkedin"], SITE["justdial"], SITE["maps_url"]) if u]
    return {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "@id": SITE["domain"] + "/#business",
        "name": SITE["name"],
        "url": SITE["domain"] + "/",
        "logo": SITE["domain"] + "/assets/img/logo.svg",
        "image": SITE["domain"] + "/assets/img/logo.svg",
        "telephone": SITE["phone_tel"],
        "email": SITE["email"],
        "foundingDate": SITE["founded"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SITE["street"],
            "addressLocality": SITE["city"],
            "addressRegion": SITE["region"],
            "postalCode": SITE["postal"],
            "addressCountry": SITE["country"],
        },
        "hasMap": SITE["maps_url"],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": SITE["opens"],
            "closes": SITE["closes"],
        }],
        "areaServed": [{"@type": "City", "name": "Vadodara"}] +
                      [{"@type": "Place", "name": f"{a['name']}, Vadodara"} for a in AREAS],
        "sameAs": same_as,
    }


def breadcrumb_schema(crumbs):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE["domain"] + "/" + path}
            for i, (name, path) in enumerate(crumbs)
        ],
    }


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def service_schema(s, area=None):
    place = f"{area['name']}, Vadodara" if area else "Vadodara"
    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": s["name"],
        "name": f"{s['name']} in {place}",
        "description": s["meta"],
        "provider": {"@id": SITE["domain"] + "/#business"},
        "areaServed": {"@type": "Place", "name": place},
        "url": SITE["domain"] + "/" + service_path(s),
    }
    return data


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


# --------------------------------------------------------------------------
# Layout pieces
# --------------------------------------------------------------------------
def head(title, meta, path, root, schemas, og_type="website"):
    canonical = SITE["domain"] + "/" + path
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="IN-GJ">
<meta name="geo.placename" content="Vadodara">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta)}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(meta)}">
<meta name="theme-color" content="#0b5ed7">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="{BS_CSS}">
<link rel="stylesheet" href="{BI_CSS}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{BI_CSS}"></noscript>
<link rel="stylesheet" href="{root}assets/css/style.css">
{chr(10).join(ld(s) for s in schemas)}
</head>
<body>
<a class="visually-hidden-focusable skip-link" href="#main">Skip to content</a>
"""


def header(root, active=""):
    svc_items = "\n".join(
        f'<li><a class="dropdown-item" href="{root}{service_path(s)}"><i class="bi {s["icon"]}"></i><span>{s["name"]}</span></a></li>' for s in SERVICES
    )

    def act(key):
        return ' active" aria-current="page' if key == active else ""

    return f"""<div class="topbar d-none d-md-block">
  <div class="container d-flex justify-content-between align-items-center">
    <ul class="topbar-list">
      <li><i class="bi bi-geo-alt-fill"></i> Laxmipura Road, Gotri, Vadodara</li>
      <li><i class="bi bi-clock-fill"></i> {SITE['hours_display']}</li>
      <li class="d-none d-lg-flex"><a href="mailto:{SITE['email']}"><i class="bi bi-envelope-fill"></i> {SITE['email']}</a></li>
    </ul>
    <div class="d-flex align-items-center gap-3">
      <a class="topbar-rating" href="{SITE['review_url']}" target="_blank" rel="noopener"><i class="bi bi-star-fill"></i> {SITE['rating']} · {SITE['reviews']}+ Google Reviews</a>
      {social_icons("social-mini")}
    </div>
  </div>
</div>
<header class="site-header sticky-top">
<nav class="navbar navbar-expand-lg" aria-label="Main navigation">
  <div class="container">
    <a class="navbar-brand brand" href="{root}">
      <span class="brand-mark"><img src="{root}assets/img/logo.svg" width="40" height="40" alt="Krishna Aircons logo"></span>
      <span class="brand-text"><span class="brand-name">Krishna <b>Aircons</b></span><span class="brand-tag">AC Experts · Vadodara</span></span>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="toggler-bar"></span><span class="toggler-bar"></span><span class="toggler-bar"></span>
    </button>
    <div class="collapse navbar-collapse" id="mainNav">
      <ul class="navbar-nav ms-auto align-items-lg-center">
        <li class="nav-item"><a class="nav-link{act('home')}" href="{root}">Home</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle{act('services')}" href="{root}services/" role="button" data-bs-toggle="dropdown" aria-expanded="false">Services</a>
          <ul class="dropdown-menu dropdown-premium">
            <li class="dropdown-head"><a href="{root}services/">All AC Services <i class="bi bi-arrow-right"></i></a></li>
            {svc_items}
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link{act('areas')}" href="{root}areas/">Areas</a></li>
        <li class="nav-item"><a class="nav-link{act('about')}" href="{root}about/">About</a></li>
        <li class="nav-item"><a class="nav-link{act('blog')}" href="{root}blog/">Blog</a></li>
        <li class="nav-item"><a class="nav-link{act('contact')}" href="{root}contact/">Contact</a></li>
        <li class="nav-item ms-lg-3 mt-2 mt-lg-0">
          <a class="call-pill" href="tel:{SITE['phone_tel']}">
            <span class="call-icon"><i class="bi bi-telephone-fill"></i></span>
            <span class="call-text"><small>Call us now</small><strong>{SITE['phone_display']}</strong></span>
          </a>
        </li>
      </ul>
    </div>
  </div>
</nav>
</header>
<main id="main">
"""


def breadcrumbs_html(crumbs, root):
    items = []
    for i, (name, path) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li class="breadcrumb-item active" aria-current="page">{esc(name)}</li>')
        else:
            items.append(f'<li class="breadcrumb-item"><a href="{root}{path}">{esc(name)}</a></li>')
    return f'<nav aria-label="breadcrumb"><ol class="breadcrumb">{"".join(items)}</ol></nav>'


def footer(root):
    svc = "\n".join(f'<li><a href="{root}{service_path(s)}"><i class="bi bi-chevron-right"></i>{s["name"]}</a></li>' for s in SERVICES)
    areas = "".join(f'<a href="{root}{area_path(a)}">{a["name"]}</a>' for a in AREAS)
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-info row g-3">
      <div class="col-md-4"><a class="info-card" href="{SITE['maps_url']}" target="_blank" rel="noopener"><span class="info-icon"><i class="bi bi-geo-alt-fill"></i></span><span><small>Visit our shop</small><strong>Opp. Aashray Hospital, Laxmipura Rd, Gotri</strong></span></a></div>
      <div class="col-md-4"><a class="info-card" href="tel:{SITE['phone_tel']}"><span class="info-icon"><i class="bi bi-telephone-fill"></i></span><span><small>Call or WhatsApp</small><strong>{SITE['phone_display']}</strong></span></a></div>
      <div class="col-md-4"><div class="info-card"><span class="info-icon"><i class="bi bi-clock-fill"></i></span><span><small>Working hours</small><strong>{SITE['hours_display']}</strong></span></div></div>
    </div>
    <div class="row g-4 footer-main">
      <div class="col-lg-4">
        <a class="brand brand-light" href="{root}">
          <span class="brand-mark"><img src="{root}assets/img/logo.svg" width="40" height="40" alt="" loading="lazy"></span>
          <span class="brand-text"><span class="brand-name">Krishna <b>Aircons</b></span><span class="brand-tag">AC Experts · Vadodara</span></span>
        </a>
        <p class="mt-3">Trusted AC repair, service, AMC, gas refilling and installation for homes and businesses across Vadodara. Honest diagnosis, upfront quotes and same-day visits.</p>
        <a class="footer-badge" href="{SITE['review_url']}" target="_blank" rel="noopener"><span class="stars">★★★★★</span><span><strong>{SITE['rating']}</strong> rating · {SITE['reviews']}+ Google reviews</span></a>
        <p class="footer-title mt-4">Follow Us</p>
        {social_icons("social-footer")}
      </div>
      <div class="col-sm-6 col-lg-3">
        <p class="footer-title">Our Services</p>
        <ul class="list-unstyled footer-links">{svc}</ul>
      </div>
      <div class="col-sm-6 col-lg-5">
        <p class="footer-title">Areas We Serve</p>
        <div class="footer-areas">{areas}</div>
        <p class="footer-title mt-4">Get in Touch</p>
        <address class="footer-address">
          <span><i class="bi bi-geo-alt"></i> {SITE['street']}, {SITE['city']}, {SITE['region']} {SITE['postal']}</span>
          <span><i class="bi bi-envelope"></i> <a href="mailto:{SITE['email']}">{SITE['email']}</a></span>
        </address>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container d-md-flex justify-content-between align-items-center text-center text-md-start">
      <p class="mb-2 mb-md-0">&copy; <span id="year">{date.today().year}</span> Krishna Aircons, Vadodara. All rights reserved.</p>
      <ul class="footer-bottom-links">
        <li><a href="{root}about/">About</a></li>
        <li><a href="{root}blog/">Blog</a></li>
        <li><a href="{root}contact/">Contact</a></li>
        <li><a href="{root}sitemap.xml">Sitemap</a></li>
      </ul>
    </div>
  </div>
</footer>
<div class="mobile-cta d-lg-none">
  <a href="tel:{SITE['phone_tel']}" class="cta-call"><i class="bi bi-telephone-fill"></i> Call Now</a>
  <a href="{wa_link()}" class="cta-wa" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> WhatsApp</a>
</div>
<script src="{BS_JS}" defer></script>
<script src="{root}assets/js/main.js" defer></script>
</body>
</html>
"""


def cta_band(root, place="Vadodara"):
    return f"""<section class="cta-band">
  <div class="container d-lg-flex align-items-center justify-content-between text-center text-lg-start">
    <div>
      <p class="h3 mb-1">Need AC help in {esc(place)} today?</p>
      <p class="mb-3 mb-lg-0">Call or WhatsApp us. Same-day visits, clear pricing, all brands.</p>
    </div>
    <div class="d-flex gap-2 justify-content-center flex-wrap">
      <a class="btn btn-light btn-lg" href="tel:{SITE['phone_tel']}"><i class="bi bi-telephone-fill"></i> {SITE['phone_display']}</a>
      <a class="btn btn-success btn-lg" href="{wa_link()}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> WhatsApp</a>
    </div>
  </div>
</section>"""


def faq_html(faqs, uid):
    items = []
    for i, (q, a) in enumerate(faqs):
        items.append(f"""<div class="accordion-item">
  <h3 class="accordion-header"><button class="accordion-button{' collapsed' if i else ''}" type="button" data-bs-toggle="collapse" data-bs-target="#{uid}{i}" aria-expanded="{'true' if i == 0 else 'false'}" aria-controls="{uid}{i}">{esc(q)}</button></h3>
  <div id="{uid}{i}" class="accordion-collapse collapse{'' if i else ' show'}" data-bs-parent="#{uid}"><div class="accordion-body">{esc(a)}</div></div>
</div>""")
    return f'<div class="accordion" id="{uid}">{"".join(items)}</div>'


def service_cards(root, cols="col-sm-6 col-lg-3", place=None):
    out = []
    for s in SERVICES:
        label = f'{s["name"]} in {place}' if place else s["name"]
        out.append(f"""<div class="{cols}">
  <a class="service-card h-100" href="{root}{service_path(s)}">
    <i class="bi {s['icon']} service-icon" aria-hidden="true"></i>
    <h3 class="h5">{esc(label)}</h3>
    <p>{esc(s['short'])}</p>
    <span class="more">Learn more &rarr;</span>
  </a>
</div>""")
    return '<div class="row g-3">' + "".join(out) + "</div>"


def area_chips(root, exclude=None):
    return '<div class="area-chips">' + "".join(
        f'<a href="{root}{area_path(a)}"><i class="bi bi-geo-alt"></i> {a["name"]}</a>'
        for a in AREAS if a["slug"] != exclude) + "</div>"


def trust_strip():
    return f"""<section class="trust-strip">
  <div class="container">
    <div class="row text-center g-3">
      <div class="col-6 col-md-3"><strong>{SITE['rating']}★</strong><span>{SITE['reviews']}+ Google reviews</span></div>
      <div class="col-6 col-md-3"><strong>Same Day</strong><span>Visits across Vadodara</span></div>
      <div class="col-6 col-md-3"><strong>All Brands</strong><span>Split, window &amp; inverter</span></div>
      <div class="col-6 col-md-3"><strong>7 Days</strong><span>Open till 11 PM</span></div>
    </div>
  </div>
</section>"""


def why_us():
    pts = [
        ("bi-search", "Honest diagnosis", "We find the real fault and only replace what actually needs replacing."),
        ("bi-cash-coin", "Upfront pricing", "You get the cost before work starts. No hidden charges."),
        ("bi-lightning-charge", "Same-day service", "Our Gotri workshop lets us reach most of Vadodara quickly."),
        ("bi-shield-check", "Service warranty", "Our repair work is covered by a service warranty."),
        ("bi-person-badge", "Trained technicians", "Experienced with split, window, cassette and inverter ACs."),
        ("bi-stars", f"Rated {SITE['rating']}★ on Google", f"Trusted by {SITE['reviews']}+ happy customers in Vadodara."),
    ]
    cards = "".join(f"""<div class="col-sm-6 col-lg-4"><div class="why-item"><i class="bi {i}" aria-hidden="true"></i><div><h3 class="h6 mb-1">{t}</h3><p class="mb-0">{d}</p></div></div></div>""" for i, t, d in pts)
    return f'<div class="row g-3">{cards}</div>'


REVIEWS = [
    ("Abhishek Bakshi", "Best and quick service. Solved my problem in 40 minutes, at a very reasonable price."),
    ("Sandeep Singhvi", "Service and work is very good. Technicians are very cooperative."),
    ("Param Bhatt", "Very good experience with the service providers."),
]


def reviews_html():
    cards = "".join(f"""<div class="col-md-4"><figure class="review-card h-100"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div><blockquote class="mb-2">“{esc(t)}”</blockquote><figcaption>{esc(n)} · Google review</figcaption></figure></div>""" for n, t in REVIEWS)
    return f'<div class="row g-3">{cards}</div><div class="text-center mt-4"><p class="mb-2 fw-semibold">Happy with our service? Your review helps other Vadodara families find us.</p>{review_buttons()}</div>'


def contact_card(root):
    rows = [
        ("bi-geo-alt-fill", "ic-blue", "Address", f"{SITE['street']}, {SITE['city']}, {SITE['region']} {SITE['postal']}", SITE["maps_url"], True),
        ("bi-telephone-fill", "ic-cyan", "Call us", SITE["phone_display"], f"tel:{SITE['phone_tel']}", False),
        ("bi-whatsapp", "ic-green", "WhatsApp", "Chat on WhatsApp", wa_link(), True),
        ("bi-envelope-fill", "ic-red", "Email", SITE["email"], f"mailto:{SITE['email']}", False),
        ("bi-clock-fill", "ic-gold", "Working hours", SITE["hours_display"], "", False),
    ]
    items = ""
    for icon, tone, label, value, href, ext in rows:
        target = ' target="_blank" rel="noopener"' if ext else ""
        inner = f'<span class="cc-icon {tone}"><i class="bi {icon}" aria-hidden="true"></i></span><span class="cc-body"><small>{label}</small><span class="cc-value">{esc(value)}</span></span>'
        if href:
            items += f'<li><a class="cc-row" href="{href}"{target}>{inner}<i class="bi bi-arrow-up-right cc-go" aria-hidden="true"></i></a></li>'
        else:
            items += f'<li><div class="cc-row">{inner}<span class="cc-open">Open today</span></div></li>'
    return f"""<div class="contact-card">
  <div class="cc-head">
    <span class="brand-mark"><img src="{root}assets/img/logo.svg" width="44" height="44" alt="" loading="lazy"></span>
    <div><p class="cc-title">Krishna Aircons</p><p class="cc-sub"><i class="bi bi-patch-check-fill"></i> AC repair &amp; service · Vadodara</p></div>
  </div>
  <address class="mb-0"><ul class="cc-list">{items}</ul></address>
  <div class="cc-actions">
    <a class="btn btn-primary" href="{SITE['maps_url']}" target="_blank" rel="noopener"><i class="bi bi-sign-turn-right-fill"></i> Get Directions</a>
    <a class="btn btn-success" href="{wa_link()}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> WhatsApp</a>
  </div>
</div>"""


def write(path, content, priority="0.6"):
    out_dir = os.path.join(ROOT, path)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)
    SITEMAP.append((path, priority))


def root_for(path):
    return "../" * path.count("/")


def page_hero(h1, lead, crumbs, root, extra=""):
    return f"""<section class="page-hero">
  <div class="container">
    {breadcrumbs_html(crumbs, root)}
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {extra}
    <div class="d-flex gap-2 flex-wrap mt-3">
      <a class="btn btn-warning btn-lg fw-semibold" href="tel:{SITE['phone_tel']}"><i class="bi bi-telephone-fill"></i> Call {SITE['phone_display']}</a>
      <a class="btn btn-outline-light btn-lg" href="{wa_link()}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> WhatsApp Us</a>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
HERO_SVG = """<svg class="hero-art" viewBox="0 0 360 260" role="img" aria-label="Split air conditioner illustration" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="40" width="320" height="96" rx="18" fill="#fff"/>
  <rect x="20" y="104" width="320" height="32" rx="0" fill="#e8f1ff"/>
  <rect x="44" y="114" width="272" height="8" rx="4" fill="#9ec5fe"/>
  <circle cx="300" cy="70" r="6" fill="#20c997"/>
  <text x="44" y="78" font-family="system-ui,sans-serif" font-size="22" font-weight="700" fill="#0b5ed7">24°C</text>
  <g stroke="#cfe2ff" stroke-width="6" stroke-linecap="round" fill="none">
    <path d="M80 160 q20 20 0 40 q-20 20 0 40"/>
    <path d="M180 160 q20 20 0 40 q-20 20 0 40"/>
    <path d="M280 160 q20 20 0 40 q-20 20 0 40"/>
  </g>
</svg>"""


def build_home():
    path, root = "", ""
    title = "AC Repair & Service in Vadodara | AMC, Gas Refilling | Krishna Aircons"
    meta = ("Trusted AC repair, AC service, AMC, gas refilling & installation in Vadodara. "
            "Same-day visits, all brands, rated 5.0★ on Google. Call +91 82009 37699.")
    faqs = [
        ("Which areas of Vadodara do you serve?", "We serve all of Vadodara, including Gotri, Laxmipura, Sevasi, Bhayli, Vasna Road, Atladra, Akota, Alkapuri, Old Padra Road, Subhanpura, Gorwa, Fatehgunj, Nizampura, Chhani, Sama, Karelibaug, Manjalpur and Waghodia Road."),
        ("What is your AC repair charge?", "The charge depends on the fault and any parts needed. Our technician inspects the AC and tells you the exact cost before starting any work."),
        ("Do you work on Sundays?", "Yes. We are open all 7 days, from 9 AM to 11 PM."),
        ("Which AC brands do you service?", "We service and repair all major brands, including LG, Samsung, Voltas, Daikin, Blue Star, Hitachi, Carrier, Lloyd, Panasonic, Godrej, Whirlpool and O General."),
        ("How do I book an AC service?", f"Call or WhatsApp us at {SITE['phone_display']}, or use the booking form on our contact page. We'll confirm a time that suits you."),
    ]
    schemas = [business_schema(),
               {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": SITE["domain"] + "/"},
               faq_schema(faqs)]
    body = head(title, meta, path, root, schemas) + header(root, "home") + f"""
<section class="hero">
  <div class="container">
    <div class="row align-items-center g-4">
      <div class="col-lg-7">
        <span class="badge-rating"><i class="bi bi-star-fill"></i> {SITE['rating']} rating · {SITE['reviews']}+ Google reviews</span>
        <h1>AC Repair &amp; Service in Vadodara</h1>
        <p class="lead">Same-day AC repair, servicing, AMC, gas refilling and installation for homes and businesses across Vadodara. All brands. Upfront pricing. Open 7 days until 11 PM.</p>
        <ul class="hero-points">
          <li><i class="bi bi-check-circle-fill"></i> Upfront quote before work</li>
          <li><i class="bi bi-check-circle-fill"></i> Split, window &amp; inverter ACs</li>
          <li><i class="bi bi-check-circle-fill"></i> Service warranty on work</li>
        </ul>
        <div class="d-flex gap-2 flex-wrap">
          <a class="btn btn-warning btn-lg fw-semibold" href="tel:{SITE['phone_tel']}"><i class="bi bi-telephone-fill"></i> Call {SITE['phone_display']}</a>
          <a class="btn btn-outline-light btn-lg" href="{wa_link()}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> Book on WhatsApp</a>
        </div>
      </div>
      <div class="col-lg-5 d-none d-lg-block">{HERO_SVG}</div>
    </div>
  </div>
</section>
{trust_strip()}
<section class="section">
  <div class="container">
    <div class="section-head">
      <h2>Our AC Services in Vadodara</h2>
      <p>Every service your air conditioner needs, from one trusted local team.</p>
    </div>
    {service_cards(root)}
  </div>
</section>
<section class="section bg-soft">
  <div class="container">
    <div class="row g-4 align-items-center">
      <div class="col-lg-6">
        <h2>Vadodara's Trusted Local AC Experts</h2>
        <p>Krishna Aircons is a local air conditioning service company based on Laxmipura Road, Gotri, opposite Aashray Hospital. Since opening in July 2025, we have built a reputation for honest diagnosis, fair pricing and fast service, and earned a {SITE['rating']}★ rating from more than {SITE['reviews']} customers on Google.</p>
        <p>From a quick <a href="{root}services/ac-repair-vadodara/">AC repair</a> to a full <a href="{root}services/ac-amc-vadodara/">annual maintenance contract</a> for your office, our trained technicians handle split, window, cassette and inverter ACs of all brands. We also specialise in <a href="{root}services/inverter-ac-repair-vadodara/">inverter AC PCB repair</a> and leak-first <a href="{root}services/ac-gas-refilling-vadodara/">AC gas refilling</a>.</p>
        <a class="btn btn-primary" href="{root}about/">More about us</a>
      </div>
      <div class="col-lg-6">{why_us()}</div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head">
      <h2>AC Service Areas in Vadodara</h2>
      <p>Same-day AC repair and service across the city. Choose your area:</p>
    </div>
    {area_chips(root)}
  </div>
</section>
<section class="section bg-soft">
  <div class="container">
    <div class="section-head"><h2>What Our Customers Say</h2><p>Rated {SITE['rating']}★ on Google by {SITE['reviews']}+ customers.</p></div>
    {reviews_html()}
  </div>
</section>
<section class="section">
  <div class="container narrow">
    <div class="section-head"><h2>Frequently Asked Questions</h2></div>
    {faq_html(faqs, "homefaq")}
  </div>
</section>
{cta_band(root)}
""" + footer(root)
    write(path, body, "1.0")


def build_service(s):
    path = service_path(s)
    root = root_for(path)
    crumbs = [("Home", ""), ("Services", "services/"), (s["name"], path)]
    schemas = [business_schema(), service_schema(s), breadcrumb_schema(crumbs), faq_schema(s["faqs"])]
    others = [o for o in SERVICES if o["slug"] != s["slug"]]
    other_links = "".join(f'<li><a href="{root}{service_path(o)}"><i class="bi {o["icon"]}"></i> {o["name"]} in Vadodara</a></li>' for o in others)
    steps = "".join(f'<div class="col-sm-6 col-lg-3"><div class="step"><span class="step-no">{i + 1}</span><h3 class="h6">{esc(t)}</h3><p>{esc(d)}</p></div></div>' for i, (t, d) in enumerate(s["steps"]))
    lst = "".join(f"<li>{esc(x)}</li>" for x in s["list"])
    intro = "".join(f"<p>{p}</p>" for p in s["intro"])
    body = head(s["title"], s["meta"], path, root, schemas) + header(root, "services") + page_hero(s["h1"], s["lead"], crumbs, root) + f"""
{trust_strip()}
<section class="section">
  <div class="container">
    <div class="row g-5">
      <div class="col-lg-8">
        <article class="content">
          <h2>{esc(s['name'])} by Krishna Aircons</h2>
          {intro}
          <h2>{esc(s['list_title'])}</h2>
          <ul class="check-list">{lst}</ul>
        </article>
      </div>
      <aside class="col-lg-4">
        <div class="side-box side-sticky">
          <p class="h5">Book {esc(s['name'])}</p>
          <p class="mb-3">Same-day visits across Vadodara. Open 7 days until 11 PM.</p>
          <a class="btn btn-primary w-100 mb-2" href="tel:{SITE['phone_tel']}"><i class="bi bi-telephone-fill"></i> {SITE['phone_display']}</a>
          <a class="btn btn-success w-100 mb-3" href="{wa_link('Hi Krishna Aircons, I need ' + s['name'] + '.')}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> WhatsApp</a>
          <p class="h6">Other services</p>
          <ul class="list-unstyled side-links">{other_links}</ul>
        </div>
      </aside>
    </div>
  </div>
</section>
<section class="section bg-soft">
  <div class="container">
    <div class="section-head"><h2>How Our {esc(s['name'])} Works</h2></div>
    <div class="row g-3">{steps}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head"><h2>{esc(s['name'])} Across Vadodara</h2><p>We provide {esc(s['name'].lower())} in all these areas of Vadodara:</p></div>
    {area_chips(root)}
  </div>
</section>
<section class="section bg-soft">
  <div class="container narrow">
    <div class="section-head"><h2>{esc(s['name'])}: FAQs</h2></div>
    {faq_html(s['faqs'], 'faq')}
  </div>
</section>
{cta_band(root)}
""" + footer(root)
    write(path, body, "0.9")


def build_area(a):
    path = area_path(a)
    root = root_for(path)
    name = a["name"]
    crumbs = [("Home", ""), ("Areas", "areas/"), (f"AC Service in {name}", path)]
    title = f"AC Repair & Service in {name}, Vadodara | Krishna Aircons"
    meta = (f"AC repair, service, AMC, gas refilling & installation in {name}, Vadodara. "
            f"Same-day visits, all brands, upfront quotes. Call {SITE['phone_display']}.")
    area_biz = dict(business_schema())
    schemas = [area_biz, breadcrumb_schema(crumbs), faq_schema(a["faqs"]),
               {"@context": "https://schema.org", "@type": "Service", "serviceType": "Air conditioner repair and maintenance",
                "name": f"AC Repair & Service in {name}, Vadodara", "provider": {"@id": SITE["domain"] + "/#business"},
                "areaServed": {"@type": "Place", "name": f"{name}, Vadodara, Gujarat"}}]
    intro = "".join(f"<p>{esc(p)}</p>" for p in a["intro"])
    hl = "".join(f"<li>{esc(h)}</li>" for h in a["highlights"])
    nearby = "".join(f'<a href="{root}{area_path(AREA_BY_SLUG[n])}"><i class="bi bi-geo-alt"></i> {AREA_BY_SLUG[n]["name"]}</a>' for n in a["nearby"])
    body = head(title, meta, path, root, schemas) + header(root, "areas") + page_hero(
        f"AC Repair &amp; Service in {esc(name)}, Vadodara",
        f"Fast, honest AC repair, servicing, AMC, gas refilling and installation for homes and businesses in {esc(name)}.",
        crumbs, root) + f"""
{trust_strip()}
<section class="section">
  <div class="container">
    <div class="row g-5">
      <div class="col-lg-8">
        <article class="content">
          <h2>Your Local AC Technicians in {esc(name)}</h2>
          {intro}
          <h3>Why {esc(name)} customers choose Krishna Aircons</h3>
          <ul class="check-list">{hl}
            <li>Upfront pricing: you know the cost before work starts</li>
            <li>All brands: LG, Samsung, Voltas, Daikin, Blue Star, Hitachi and more</li>
          </ul>
        </article>
      </div>
      <aside class="col-lg-4">
        <div class="side-box side-sticky">
          <p class="h5">Book AC service in {esc(name)}</p>
          <p class="mb-3">Call or WhatsApp with your AC problem and address in {esc(name)}.</p>
          <a class="btn btn-primary w-100 mb-2" href="tel:{SITE['phone_tel']}"><i class="bi bi-telephone-fill"></i> {SITE['phone_display']}</a>
          <a class="btn btn-success w-100 mb-3" href="{wa_link('Hi Krishna Aircons, I need AC service in ' + name + ', Vadodara.')}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> WhatsApp</a>
          <p class="h6">Nearby areas we serve</p>
          <div class="area-chips small-chips">{nearby}</div>
        </div>
      </aside>
    </div>
  </div>
</section>
<section class="section bg-soft">
  <div class="container">
    <div class="section-head"><h2>Our AC Services in {esc(name)}</h2></div>
    {service_cards(root, place=name)}
  </div>
</section>
<section class="section">
  <div class="container narrow">
    <div class="section-head"><h2>AC Service in {esc(name)}: FAQs</h2></div>
    {faq_html(a['faqs'], 'faq')}
  </div>
</section>
<section class="section bg-soft">
  <div class="container">
    <div class="section-head"><h2>Other Areas We Serve in Vadodara</h2></div>
    {area_chips(root, exclude=a['slug'])}
  </div>
</section>
{cta_band(root, name)}
""" + footer(root)
    write(path, body, "0.8")


def build_services_hub():
    path = "services/"
    root = root_for(path)
    crumbs = [("Home", ""), ("Services", path)]
    title = "AC Services in Vadodara | Repair, AMC, Gas Refilling | Krishna Aircons"
    meta = "All AC services in Vadodara: repair, service, AMC, gas refilling, installation, inverter PCB repair, deep cleaning & shifting. Same-day visits."
    schemas = [business_schema(), breadcrumb_schema(crumbs)]
    body = head(title, meta, path, root, schemas) + header(root, "services") + page_hero(
        "AC Services in Vadodara", "Repair, servicing, AMC, gas refilling, installation and more, for every type and brand of air conditioner.", crumbs, root) + f"""
<section class="section">
  <div class="container">
    {service_cards(root)}
  </div>
</section>
{cta_band(root)}
""" + footer(root)
    write(path, body, "0.9")


def build_areas_hub():
    path = "areas/"
    root = root_for(path)
    crumbs = [("Home", ""), ("Areas We Serve", path)]
    title = "Areas We Serve in Vadodara | AC Repair Near Me | Krishna Aircons"
    meta = "Krishna Aircons provides AC repair & service across Vadodara: Gotri, Laxmipura, Sevasi, Bhayli, Vasna Road, Akota, Alkapuri, Manjalpur, Waghodia Road & more."
    cards = "".join(f"""<div class="col-sm-6 col-lg-4"><a class="service-card h-100" href="{root}{area_path(a)}"><i class="bi bi-geo-alt-fill service-icon" aria-hidden="true"></i><h2 class="h5">AC Service in {a['name']}</h2><p>{esc(a['intro'][0][:150].rsplit(' ', 1)[0])}…</p><span class="more">View {a['name']} page &rarr;</span></a></div>""" for a in AREAS)
    schemas = [business_schema(), breadcrumb_schema(crumbs)]
    body = head(title, meta, path, root, schemas) + header(root, "areas") + page_hero(
        "AC Repair &amp; Service Areas in Vadodara", "From our workshop in Gotri, we cover the whole of Vadodara, usually with same-day visits.", crumbs, root) + f"""
<section class="section">
  <div class="container">
    <div class="row g-3">{cards}</div>
  </div>
</section>
<section class="section bg-soft">
  <div class="container narrow content">
    <h2>Don't see your area?</h2>
    <p>We serve all of Vadodara city and nearby localities. If your area isn't listed, call or WhatsApp us at <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a> and we'll confirm the earliest visit time.</p>
  </div>
</section>
{cta_band(root)}
""" + footer(root)
    write(path, body, "0.8")


def build_about():
    path = "about/"
    root = root_for(path)
    crumbs = [("Home", ""), ("About Us", path)]
    title = "About Krishna Aircons | AC Repair & Service Company in Vadodara"
    meta = f"Krishna Aircons is a trusted AC repair and service company in Gotri, Vadodara, open since July 2025 and rated {SITE['rating']}★ by {SITE['reviews']}+ customers on Google."
    schemas = [business_schema(), breadcrumb_schema(crumbs)]
    body = head(title, meta, path, root, schemas) + header(root, "about") + page_hero(
        "About Krishna Aircons", "Your trusted local air conditioning experts in Vadodara.", crumbs, root) + f"""
<section class="section">
  <div class="container">
    <div class="row g-5">
      <div class="col-lg-7 content">
        <h2>Cool comfort, honest service</h2>
        <p>Krishna Aircons is an air conditioning repair and service company based on Laxmipura Road, Gotri, Vadodara, opposite Aashray Hospital. We officially opened on 11 July 2025 with one simple goal: to give Vadodara families and businesses AC service they can trust.</p>
        <p>Too many customers have been overcharged for parts they didn't need, or had their AC "refilled" every season without anyone fixing the leak. We do things differently. Our technicians diagnose the real problem, explain it in plain words, and give you the price before starting work.</p>
        <p>That approach has earned us a <strong>{SITE['rating']}★ rating from {SITE['reviews']}+ customers on Google</strong> and a 5.0 rating on Justdial.</p>
        <h2>What we do</h2>
        <ul class="check-list">
          {''.join(f'<li><a href="{root}{service_path(s)}">{s["name"]}</a>: {esc(s["short"])}</li>' for s in SERVICES)}
        </ul>
        <h2>Our promise</h2>
        <ul class="check-list">
          <li>On-time visits, 7 days a week, until 11 PM</li>
          <li>Upfront, transparent pricing</li>
          <li>Genuine spare parts and correct refrigerant</li>
          <li>A clean work area: we cover your walls and floor</li>
          <li>A service warranty on our work</li>
        </ul>
      </div>
      <aside class="col-lg-5">
        {contact_card(root)}
        <div class="mt-4">{why_us()}</div>
      </aside>
    </div>
  </div>
</section>
<section class="section bg-soft">
  <div class="container">
    <div class="section-head"><h2>What Our Customers Say</h2></div>
    {reviews_html()}
  </div>
</section>
{cta_band(root)}
""" + footer(root)
    write(path, body, "0.6")


def build_contact():
    path = "contact/"
    root = root_for(path)
    crumbs = [("Home", ""), ("Contact", path)]
    title = "Contact Krishna Aircons | Book AC Repair & Service in Vadodara"
    meta = f"Book AC repair or service in Vadodara. Call {SITE['phone_display']}, WhatsApp us or visit our shop on Laxmipura Road, Gotri (opp. Aashray Hospital). Open 7 days, 9 AM–11 PM."
    schemas = [business_schema(), breadcrumb_schema(crumbs)]
    svc_opts = "".join(f"<option>{s['name']}</option>" for s in SERVICES)
    area_opts = "".join(f"<option>{a['name']}</option>" for a in AREAS) + "<option>Other area</option>"
    body = head(title, meta, path, root, schemas) + header(root, "contact") + page_hero(
        "Contact &amp; Book AC Service", "Call, WhatsApp or send the form below. We'll confirm your appointment at your preferred time.", crumbs, root) + f"""
<section class="section">
  <div class="container">
    <div class="row g-5">
      <div class="col-lg-6">
        <h2 class="h3">Book a service</h2>
        <p>Fill in the details and press the button. This opens WhatsApp with your booking message ready to send.</p>
        <form id="bookingForm" class="booking-form" novalidate>
          <div class="mb-3"><label class="form-label" for="fName">Your name</label><input class="form-control" id="fName" name="name" required autocomplete="name"></div>
          <div class="mb-3"><label class="form-label" for="fPhone">Phone number</label><input class="form-control" id="fPhone" name="phone" type="tel" required autocomplete="tel" inputmode="tel"></div>
          <div class="row">
            <div class="col-sm-6 mb-3"><label class="form-label" for="fService">Service</label><select class="form-select" id="fService" name="service">{svc_opts}</select></div>
            <div class="col-sm-6 mb-3"><label class="form-label" for="fArea">Area</label><select class="form-select" id="fArea" name="area">{area_opts}</select></div>
          </div>
          <div class="mb-3"><label class="form-label" for="fMsg">Problem / preferred time</label><textarea class="form-control" id="fMsg" name="message" rows="3"></textarea></div>
          <button class="btn btn-success btn-lg w-100" type="submit"><i class="bi bi-whatsapp"></i> Send booking on WhatsApp</button>
          <p class="form-error text-danger small mt-2 d-none" role="alert">Please enter your name and phone number.</p>
        </form>
      </div>
      <div class="col-lg-6">
        <div class="side-box mb-4">
          <h2 class="h4">Krishna Aircons</h2>
          <address class="mb-0">
            <p><i class="bi bi-geo-alt-fill"></i> {SITE['street']}, {SITE['city']}, {SITE['region']} {SITE['postal']}</p>
            <p><i class="bi bi-telephone-fill"></i> <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p>
            <p><i class="bi bi-whatsapp"></i> <a href="{wa_link()}" target="_blank" rel="noopener">Chat on WhatsApp</a></p>
            <p><i class="bi bi-envelope-fill"></i> <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
            <p class="mb-0"><i class="bi bi-clock-fill"></i> {SITE['hours_display']}</p>
          </address>
        </div>
        <div class="side-box mb-4">
          <h2 class="h5 mb-3">Find us online</h2>
          {find_us_online()}
          <p class="h6 mt-4 mb-2">Leave us a review</p>
          {review_buttons()}
        </div>
        <div class="map-wrap">
          <iframe src="{SITE['maps_embed']}" title="Krishna Aircons location on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
""" + footer(root)
    write(path, body, "0.7")


def build_blog_hub():
    path = "blog/"
    root = root_for(path)
    crumbs = [("Home", ""), ("Blog", path)]
    title = "AC Tips & Guides | Krishna Aircons Blog, Vadodara"
    meta = "Practical AC tips from Vadodara's AC experts: why your AC isn't cooling, how often to service it, signs of low gas, and more."
    schemas = [business_schema(), breadcrumb_schema(crumbs)]
    cards = "".join(f"""<div class="col-md-6 col-lg-4"><a class="service-card h-100" href="{root}{blog_path(b)}"><time datetime="{b['date']}" class="small text-muted">{date.fromisoformat(b['date']).strftime('%d %b %Y')}</time><h2 class="h5 mt-1">{esc(b['h1'])}</h2><p>{esc(b['excerpt'])}</p><span class="more">Read article &rarr;</span></a></div>""" for b in BLOG)
    body = head(title, meta, path, root, schemas) + header(root, "blog") + page_hero(
        "AC Tips &amp; Guides", "Simple advice to keep your AC cooling well through Vadodara's summers.", crumbs, root) + f"""
<section class="section"><div class="container"><div class="row g-3">{cards}</div></div></section>
{cta_band(root)}
""" + footer(root)
    write(path, body, "0.6")


def build_blog_post(b):
    path = blog_path(b)
    root = root_for(path)
    crumbs = [("Home", ""), ("Blog", "blog/"), (b["h1"], path)]
    article = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": b["h1"], "description": b["meta"], "datePublished": b["date"], "dateModified": b["date"],
        "author": {"@type": "Organization", "name": SITE["name"], "url": SITE["domain"] + "/"},
        "publisher": {"@id": SITE["domain"] + "/#business"},
        "mainEntityOfPage": SITE["domain"] + "/" + path,
    }
    schemas = [business_schema(), breadcrumb_schema(crumbs), article]
    others = "".join(f'<li><a href="{root}{blog_path(o)}">{esc(o["h1"])}</a></li>' for o in BLOG if o["slug"] != b["slug"])
    svc = "".join(f'<li><a href="{root}{service_path(s)}">{s["name"]} in Vadodara</a></li>' for s in SERVICES)
    body = head(b["title"], b["meta"], path, root, schemas, "article") + header(root, "blog") + f"""
<section class="page-hero">
  <div class="container narrow">
    {breadcrumbs_html(crumbs, root)}
    <h1>{esc(b['h1'])}</h1>
    <p class="mb-0"><time datetime="{b['date']}">{date.fromisoformat(b['date']).strftime('%d %B %Y')}</time> · By Krishna Aircons, Vadodara</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="row g-5">
      <article class="col-lg-8 content">{b['body'].replace('{root}', root)}</article>
      <aside class="col-lg-4">
        <div class="side-box side-sticky">
          <p class="h5">Need an AC technician?</p>
          <a class="btn btn-primary w-100 mb-2" href="tel:{SITE['phone_tel']}"><i class="bi bi-telephone-fill"></i> {SITE['phone_display']}</a>
          <a class="btn btn-success w-100 mb-3" href="{wa_link()}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> WhatsApp</a>
          <p class="h6">More articles</p><ul class="side-links list-unstyled">{others}</ul>
          <p class="h6">Our services</p><ul class="side-links list-unstyled">{svc}</ul>
        </div>
      </aside>
    </div>
  </div>
</section>
{cta_band(root)}
""" + footer(root)
    write(path, body, "0.6")


def build_404():
    # Served from any URL, so it uses absolute paths.
    root = "/"
    body = head("Page Not Found | Krishna Aircons", "The page you are looking for could not be found.", "404.html", root, []) \
        .replace('content="index, follow, max-image-preview:large"', 'content="noindex"') + header(root) + f"""
<section class="section text-center">
  <div class="container narrow">
    <h1 class="display-5">Page not found</h1>
    <p class="lead">Sorry, this page doesn't exist. Try one of these instead:</p>
    <p><a class="btn btn-primary m-1" href="/">Home</a> <a class="btn btn-outline-primary m-1" href="/services/">AC Services</a> <a class="btn btn-outline-primary m-1" href="/areas/">Areas</a> <a class="btn btn-outline-primary m-1" href="/contact/">Contact</a></p>
  </div>
</section>
""" + footer(root)
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(body)


def build_sitemap():
    urls = "\n".join(
        f"  <url><loc>{SITE['domain']}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>"
        for p, pr in SITEMAP)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {SITE['domain']}/sitemap.xml\n")


if __name__ == "__main__":
    build_home()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
    build_areas_hub()
    for a in AREAS:
        build_area(a)
    build_about()
    build_contact()
    build_blog_hub()
    for b in BLOG:
        build_blog_post(b)
    build_404()
    build_sitemap()
    print(f"Built {len(SITEMAP)} pages + 404.html, sitemap.xml, robots.txt")
