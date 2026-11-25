# Krishna Aircons – Website

Static, SEO-focused website for **Krishna Aircons, Vadodara** (HTML + CSS + Bootstrap 5).
Works on any static host: Hostinger, GitHub Pages, Netlify, cPanel, and others.

## Structure
- `index.html`: home page
- `services/…`: 8 service pages (AC repair, AC service, AMC, gas refilling, installation, inverter/PCB repair, deep cleaning, shifting)
- `areas/…`: 19 Vadodara area pages (Gotri, Laxmipura, Alkapuri, Akota, Manjalpur, and more)
- `blog/…`: AC tips articles
- `about/`, `contact/`, `404.html`, `sitemap.xml`, `robots.txt`
- `assets/`: CSS, JS, logo

## Editing content
All text (phone, address, hours, services, areas, FAQs, blog posts) is in `_build/content.py`.
After editing, regenerate every page with:

```bash
python3 _build/build.py
```

Then commit and push the regenerated files.
