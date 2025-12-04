My Logo Module
===============

Purpose
-------
Lightweight module used for replacing the default Odoo logos with a custom company logo. It contains a data file that installs the logo on the `res.company` record and provides a simple `my_logo.png` placeholder in `static/img/`.

Files created
-------------
- `addons/my_logo/__manifest__.py` — Manifest for the module.
- `addons/my_logo/data/logo.xml` — Data that updates the `res.company` logo.
- `addons/my_logo/static/img/my_logo.png` — Placeholder logo (replace with your own file).

Global replacements made (non-modular)
-------------------------------------
To visually update the UI and PDFs, the following global static images were replaced with the placeholder image:
- `addons/web/static/img/logo.png` (web header)
- `addons/web/static/img/odoo_logo.svg` (web logo - now an SVG wrapper that embeds PNG)
- `odoo/addons/base/static/img/main_partner-image.png` (used in PDFs, reports)

Backups
-------
Backup copies of these original files are present next to the modified files with a `.bak` suffix:
- `addons/web/static/img/logo.png.bak`
- `odoo/addons/base/static/img/main_partner-image.png.bak`
- If `odoo_logo.svg` existed before, a `.bak` backup will be created as well.

Usage
-----
1) Place your logo file (prefer SVG or PNG) at:
```
addons/my_logo/static/img/my_logo.png
```
   or use `my_logo.svg` if available (recommended for vector quality).

2) Install the module (optional):
```
python odoo-bin -c odoo_local.conf --init=my_logo
```
   Installing will also set the company logo via data; this is the recommended approach for multi-company setups.

3) If you used the global replacement method (already done in this workspace), restart Odoo server to apply the UI changes.

Reverting
--------
To revert, restore the original files from `.bak` copies:
```bash
cp addons/web/static/img/logo.png.bak addons/web/static/img/logo.png
cp odoo/addons/base/static/img/main_partner-image.png.bak odoo/addons/base/static/img/main_partner-image.png
# if odoo_logo.svg.bak exists:
cp addons/web/static/img/odoo_logo.svg.bak addons/web/static/img/odoo_logo.svg
```

Notes
-----
- For production, prefer installing a module that sets `res.company` logos rather than replacing static files.
- If you have an SVG, use it for `odoo_logo.svg` (keeps vector quality). If not, this module embeds the PNG inside a small SVG wrapper.
- This commit intentionally does not add `.bak` files to Git. They are only present locally as safety backups.

If you'd like, I can:
- Replace the placeholder with an uploaded actual logo and keep the SVG as vector if available.
- Commit or clean backups, or add a `.gitignore` rule for `*.bak` files.
- Rework replacements to be modular-only (set company logo via XML without editing global static files).