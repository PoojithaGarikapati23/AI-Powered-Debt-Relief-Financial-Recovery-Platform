# AI Powered Debt Relief & Financial Recovery Platform

An AI-powered web application that helps borrowers manage loan details, analyze
financial health, and generate AI-driven negotiation strategies and settlement
recommendations.

## Tech Stack
- **Backend:** Python, FastAPI
- **Database:** SQLite (via built-in `sqlite3`)
- **AI:** Google Gemini API (`gemini-1.5-flash`) for negotiation letter generation
- **Frontend:** HTML + Jinja2 templates (server-rendered)

## Features
1. **AI-Powered Settlement Recommendation** — analyzes outstanding amount, EMI,
   overdue duration, and income to generate a settlement percentage and debt
   stress level.
2. **Intelligent Negotiation Letter Generation** — uses Google Gemini AI to
   draft a professional, lender-specific settlement negotiation email.
3. **Financial Health Dashboard** — tracks EMI ratio, monthly surplus, debt
   stress level, and negotiation history across all analyzed loans.

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Set your Gemini API key for real AI-generated letters
#    Without this, the app falls back to a smart rule-based letter template.
export GEMINI_API_KEY="your_api_key_here"      # Windows: set GEMINI_API_KEY=your_key

# 3. Run the app
uvicorn main:app --reload

# 4. Open in browser
http://localhost:8000
```

## Project Structure
```
debt-relief-platform/
├── main.py                 # FastAPI app, routes, AI + analysis logic
├── requirements.txt
├── templates/
│   ├── index.html           # Loan input form
│   ├── result.html          # Settlement recommendation + negotiation letter
│   └── dashboard.html       # Financial health & history dashboard
└── debt_relief.db           # Auto-created SQLite database
```

## Demo Video
📹 [Watch the demo here](https://drive.google.com/file/d/1OE5PPYnmXsopkf_1EK8_hMi-8upI4z5A/view?usp=drive_link)

## Skills Applied
Python, FastAPI, SQLite, Generative AI, Responsible AI, LLMs, Prompt
Engineering, Gemini AI, API Integration, Cloud Computing

## Smartbridge Project — Team
- Naredla Greeshma Reddy (Team Lead)
- Poojitha Garikapati
- Donthagani Srikanth
- Kongitala Harshitha
- Kadiyala Madhuri
- Vanamadi Srilekhya
