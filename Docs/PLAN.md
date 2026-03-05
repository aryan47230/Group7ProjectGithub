# Group 7 — FinanceFlow PLAN.md

## App Overview

A web app that helps small businesses and solopreneurs manage their finances without an accountant. Users upload a bank statement (PDF or CSV), the ML backend automatically parses and categorizes every transaction, and the results are displayed in a clean dashboard that can be exported to Excel or Google Sheets. A tax optimization layer highlights deductible categories and estimated savings.

---

## Pages / Screens

### 1. Landing Page (`/`)
- Headline, subheadline, and "Get Started" CTA button
- 3-column features section (Parse, Categorize, Export)
- Navbar with logo and login button

### 2. Upload Page (`/upload`)
- Drag-and-drop zone for bank statement (PDF or CSV)
- File picker fallback button
- Accepted file types: `.pdf`, `.csv`
- Loading/processing state while ML runs
- Error state for unsupported file types

### 3. Dashboard (`/dashboard`)
- **Summary cards:** Total Income, Total Expenses, Top Spending Category
- **Transaction table:**
  - Columns: Date, Description, Amount, Category
  - Per-row edit button (user can correct ML category)
  - Search bar + category filter dropdown
- **Tax panel:** List of deductible categories with estimated savings

### 4. Export (`/export` or modal)
- Toggle: Excel vs Google Sheets
- Download button
- Confirmation message on success

---

## Core Features (MVP)

- [ ] Parse bank statements from PDF and CSV using ML
- [ ] Auto-categorize transactions (e.g. Food, Travel, Office, Utilities)
- [ ] Display categorized transactions in a sortable/filterable table
- [ ] Allow users to manually edit a transaction's category
- [ ] Export transactions to `.xlsx` or Google Sheets
- [ ] Tax optimization: flag deductible categories, show estimated savings

---

## Stretch Goals (Post-MVP)

- [ ] Auto-generate income statement and balance sheet
- [ ] AI insight panel: natural language summary of spending patterns
- [ ] Bank account manager: store multiple statements, track benefits

---

## Tech Stack

| Layer     | Technology      | Purpose                                      |
|-----------|-----------------|----------------------------------------------|
| IDE       | VS Code         | Development environment                      |
| Design    | Figma           | Wireframes and UI mockups                    |
| Frontend  | React           | UI components and page routing               |
| Backend   | Django          | REST API, file handling, ML pipeline trigger |
| ML        | Scikit-learn    | Transaction parsing and categorization       |
| Export    | openpyxl        | Generate `.xlsx` files                       |
| DB        | SQLite (dev)    | Store parsed transactions locally            |

---

## Data

### What the app stores
- Raw uploaded file (temporary, deleted after processing)
- Parsed transactions: `{ date, description, amount, category, is_edited }`
- User-corrected categories (for improving ML accuracy over time)
- Export history (optional)

### Where data lives
- All transaction data stored in Django backend (SQLite for development, PostgreSQL for production)
- No sensitive financial data persisted longer than the session unless user opts in

---

## API / External Dependencies

| Dependency     | Used For                        | Required for MVP? |
|----------------|---------------------------------|-------------------|
| openpyxl       | Excel export                    | Yes               |
| pdfplumber     | Parsing PDF bank statements     | Yes               |
| pandas         | CSV parsing and data processing | Yes               |
| scikit-learn   | Transaction categorization      | Yes               |
| Google Sheets API | Google Sheets export         | Stretch           |

---

## Team

| Role        | Members                        |
|-------------|--------------------------------|
| Website     | Brian, August                  |
| ML          | Saanvi, Peter, Jose            |
| PMs         | jmei52, lilyl4                 |

---

*Last updated: Sprint 2 — v1 planning phase*
