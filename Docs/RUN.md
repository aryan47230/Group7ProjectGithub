# Group 7 — FinanceFlow RUN.md

How to set up and run the project locally from scratch.

---

## Prerequisites

Make sure you have these installed before starting:

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **Node.js 18+** — [nodejs.org](https://nodejs.org/)
- **Git** — [git-scm.com](https://git-scm.com/)
- **VS Code** (recommended)

---

## 1. Clone the Repo

```bash
git clone https://github.com/YOUR_ORG/group7-financeflow.git
cd group7-financeflow
```

---

## 2. Backend Setup (Django)

```bash
# Navigate to the backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the Django dev server
python manage.py runserver
```

Backend will be running at: `http://localhost:8000`

---

## 3. Frontend Setup (React)

Open a **new terminal tab**, then:

```bash
# Navigate to the frontend folder
cd frontend

# Install dependencies
npm install

# Start the React dev server
npm start
```

Frontend will be running at: `http://localhost:3000`

---

## 4. Environment Variables

Create a `.env` file inside the `backend/` folder:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

> **Note:** Never commit `.env` to GitHub. It's already in `.gitignore`.

---

## 5. Project Structure

```
group7-financeflow/
├── backend/                  # Django project
│   ├── api/                  # REST API app
│   │   ├── views.py          # Upload, categorize, export endpoints
│   │   ├── models.py         # Transaction model
│   │   └── ml/               # ML pipeline (parsing + categorization)
│   │       ├── parser.py     # PDF/CSV parsing (pdfplumber, pandas)
│   │       └── categorizer.py # Scikit-learn transaction classifier
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                 # React project
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Landing.jsx
│   │   │   ├── Upload.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── Export.jsx
│   │   ├── components/       # Reusable UI components
│   │   └── App.jsx
│   └── package.json
│
├── PLAN.md
└── RUN.md
```

---

## 6. Key API Endpoints

| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| POST   | `/api/upload/`       | Upload a bank statement (PDF or CSV) |
| GET    | `/api/transactions/` | Get all parsed + categorized rows    |
| PATCH  | `/api/transactions/:id/` | Edit a transaction's category    |
| GET    | `/api/export/xlsx/`  | Download transactions as `.xlsx`     |

---

## 7. Running the ML Pipeline Manually (for ML team)

```bash
cd backend
source venv/bin/activate

# Test the parser on a sample file
python -c "from api.ml.parser import parse_statement; print(parse_statement('sample.pdf'))"

# Test the categorizer
python -c "from api.ml.categorizer import categorize; print(categorize('UBER TRIP'))"
```

Sample files for testing are in `backend/api/ml/samples/`.

---

## 8. Common Issues

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` on Django start | Make sure your virtualenv is activated |
| React can't reach backend | Check Django is running on port 8000, check CORS settings in `settings.py` |
| PDF parsing returns empty | Install `pdfplumber`: `pip install pdfplumber` |
| Port 3000 already in use | Kill the process: `lsof -ti:3000 | xargs kill` |

---

## 9. Git Workflow

```bash
# Always pull before starting work
git pull origin main

# Create a branch for your feature
git checkout -b feature/your-feature-name

# Stage and commit your changes
git add .
git commit -m "brief description of what you did"

# Push your branch
git push origin feature/your-feature-name

# Open a Pull Request on GitHub — don't push directly to main
```

---

*Last updated: Sprint 2 — local dev setup*
