# Implementation Plan: Rebranding and Optimizing Odoo

This plan outlines the steps to remove visible references to "Odoo" and provide optimization strategies for the codebase.

## ✅ Current Progress (Completed)

- [x] **Core Metadata**: Updated `release.py` to change product name and project descriptions.
- [x] **Web Layouts**: Modified `webclient_templates.xml` and `report_templates.xml` to rename page titles and reports.
- [x] **Login Interface**: Cleaned up "Powered by Odoo" and database manager links in the login screen.
- [x] **Security/README**: Updated public-facing documentation to remove branding.
- [x] **Refactoring (Security)**: Refactored `auto_login` controller to move hardcoded credentials to system parameters.
- [x] **Base Views**: Updated users, partners, and company views to use generic "System" terminology.
- [x] **System Settings**: Updated "General Settings" edition info to remove brand names.
- [x] **Extended UI**: Rebranded company views, security group descriptions, push notification alerts, and scoped app installers.
- [x] **Help Text**: Genericized help text for views, menus, and actions in the technical settings.
- [x] **Enterprise Dialogs**: Updated upgrade dialogs to refer to "Enterprise Edition" instead of brand-specific naming.
- [x] **Author Info**: Mass-updated module author information from "Odoo S.A." to "Integrated System".
- [x] **Database Manager**: Rebranded the database selection and management pages, including titles and logo removal.
- [x] **Identity (Bot)**: Renamed "OdooBot" to "SystemBot" globally in the database and updated its avatar icon.
- [x] **User Menu**: Rebranded "My Odoo.com account" to "My Account" and genericized documentation links.
- [x] **Error Dialogs**: Replaced "Odoo Error" with "System Error" and generalized all system error titles.
- [x] **Messaging Menu**: Updated "Install Odoo" prompts to "Install System".
- [x] **System Translations**: Performed a database-wide update of translations to replace "Odoo" with "System".
- [x] **PDF Tools**: Rebranded PDF metadata (Creator/Producer) and banner descriptions.
- [x] **Code Quality**: Addressed linting issues in `__manifest__.py` and other core files.

## 1. Rebranding (Removing "Odoo" References)

To avoid breaking the system, we will focus on **user-facing strings** and **metadata**, while preserving technical identifiers (like package names and imports).

### A. UI Templates & Layouts

We will override the primary web layouts to remove "Odoo" from the page title, footer, and login screens.

- **File**: `addons/web/views/webclient_templates.xml`
- **Changes**:
  - Replace `<title t-esc="title or 'Odoo'"/>` with a generic title or company name.
  - Remove or modify "Powered by Odoo" in `brand_promotion` and `login_layout`.
  - Update logos and favicons references.

### B. Metadata & Descriptions

- **File**: `__manifest__.py` files across modules.
- **Change**: Remove "Part of Odoo" or Odoo-specific categories.
- **File**: `ir_module.py` (and others)
- **Change**: Clean up comments and string constants that mention Odoo in user-facing contexts.

### C. System Parameters

- Update `web.base.url` and company names via data files or a setup script.

## 2. Optimization & Refactoring

### A. Database Layer

- **Recordsets**: Use `search_read` instead of `search().mapped()` for large datasets to reduce memory overhead.
- **Indexing**: Ensure fields used in `domain` filters have `index=True`.
- **Batch Processing**: Use `env.cr.execute` for massive data operations that don't require ORM logic.

### B. Logic & Refactoring

- **Decorators**: Ensure `api.depends` accurately reflects all dependencies to avoid stale caches.
- **OWL Transition**: Transition legacy Web Widgets (JS) to OWL components for a faster, reactive UI.
- **Type Hinting**: Add Python type hints to complex methods to improve IDE support and maintainability.

### C. Performance

- **Assets**: Optimize SCSS and JS bundles; ensure `__manifest__.py` only includes necessary assets.
- **Translation Cache**: Ensure translations are properly indexed to speed up page loads in multi-language environments.

## 3. Execution Strategy

1. **Search Phase**: Use regex to find all non-import occurrences of "Odoo".
2. **Replacement Phase**: Apply changes to XML and user-facing Python strings.
3. **Verification**: Run Odoo in a test environment to ensure no imports or technical hooks were broken.
