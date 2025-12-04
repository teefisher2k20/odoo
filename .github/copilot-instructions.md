# Odoo Copilot Instructions

## Architecture Overview
Odoo is a modular ERP system with core framework in `odoo/` and business modules in `addons/`. Key components:
- **ORM**: `odoo/models.py` provides base `models.Model` for data models with fields as class attributes (e.g., `name = fields.Char()`).
- **Views**: XML files in `addons/*/views/` define UI with `<record model="ir.ui.view"><field name="arch">` containing form/tree elements.
- **Controllers**: Python classes in `addons/*/controllers/` inheriting `Controller`, using `@route` decorators for web endpoints.
- **Services**: `odoo/service/` handles RPC, DB connections, and server management.
Data flows: HTTP requests → Controllers → Models → PostgreSQL DB. Modules communicate via ORM and dependencies in `__manifest__.py`.

## Developer Workflows
- **Run server**: `python odoo-bin -c odoo_local.conf` (configures DB, addons path).
- **Install dependencies**: `pip install -r requirements.txt` (includes psycopg2 for PostgreSQL).
- **Tests**: Use `TransactionCase` subclasses in `addons/*/tests/`, decorated with `@tagged('post_install')`; run via `odoo-bin --test-enable --test-tags=post_install`.
- **Debug**: Enable logging in config; use `import pdb; pdb.set_trace()` in code.
- **Module installation**: Add to `addons_path` in config; install via UI or `--init=module_name`.

## Conventions
- **Models**: Inherit `models.Model`, define `_name`, fields as `snake_case`. Example: `class AccountAccount(models.Model): _name = 'account.account'; name = fields.Char(required=True)`.
- **Views**: XML records with `<form><sheet><field name="field_name"/></sheet></form>`. Reference: `addons/account/views/account_account_views.xml`.
- **Controllers**: `@route('/api/endpoint', auth='user')` methods. Example: `class AccountController(http.Controller): @route('/account/chart', auth='user')`.
- **Manifest**: `__manifest__.py` lists `depends`, `data` (XML/CSV files), `demo`, `test`.
- **Naming**: snake_case for fields/methods, CamelCase for classes; avoid reserved words like `id`, `name`.

## Integration Points
- **Database**: PostgreSQL via `psycopg2`; models auto-generate tables.
- **External APIs**: Via IAP modules (e.g., `crm_iap_*`) or custom connectors; controllers handle REST-like endpoints.
- **Cross-module**: Use `self.env['module.model']` for ORM access; wizards for complex flows.
Reference key files: `odoo/models.py`, `addons/account/models/account_account.py`, `addons/account/__manifest__.py`.