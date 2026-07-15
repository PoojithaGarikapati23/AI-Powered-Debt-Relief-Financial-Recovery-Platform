"""
AI Powered Debt Relief & Financial Recovery Platform
Smartbridge Project

Run with: uvicorn main:app --reload
Open: http://localhost:8000
"""

import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Optional: Google Gemini AI (falls back to rule-based text if no API key set)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = False
if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        USE_GEMINI = True
    except Exception:
        USE_GEMINI = False

app = FastAPI(title="AI Powered Debt Relief & Financial Recovery Platform")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

DB_FILE = "debt_relief.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outstanding_amount REAL,
            emi REAL,
            overdue_days INTEGER,
            monthly_income REAL,
            emi_ratio REAL,
            monthly_surplus REAL,
            debt_stress_level TEXT,
            settlement_percentage REAL,
            settlement_amount REAL,
            negotiation_letter TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------------------------
# Core AI / analysis logic
# ---------------------------
def analyze_financial_health(outstanding_amount, emi, overdue_days, monthly_income):
    """Rule-based financial health + settlement recommendation engine."""
    emi_ratio = round((emi / monthly_income) * 100, 2) if monthly_income > 0 else 0
    monthly_surplus = round(monthly_income - emi, 2)

    # Debt stress scoring
    if emi_ratio >= 60 or overdue_days >= 90:
        debt_stress_level = "High"
        settlement_percentage = 45
    elif emi_ratio >= 35 or overdue_days >= 30:
        debt_stress_level = "Moderate"
        settlement_percentage = 65
    else:
        debt_stress_level = "Low"
        settlement_percentage = 85

    # Adjust settlement based on surplus capacity
    if monthly_surplus < 0:
        settlement_percentage -= 10
    settlement_percentage = max(30, min(settlement_percentage, 90))

    settlement_amount = round(outstanding_amount * (settlement_percentage / 100), 2)

    return {
        "emi_ratio": emi_ratio,
        "monthly_surplus": monthly_surplus,
        "debt_stress_level": debt_stress_level,
        "settlement_percentage": settlement_percentage,
        "settlement_amount": settlement_amount,
    }


def generate_negotiation_letter(outstanding_amount, emi, overdue_days, monthly_income, analysis, lender_name="the Lender"):
    """Generates a negotiation/settlement letter using Gemini AI if available, else a smart template."""
    prompt = f"""
    Write a professional, polite loan settlement negotiation email from a borrower to {lender_name}.
    Details:
    - Outstanding amount: Rs.{outstanding_amount}
    - Current EMI: Rs.{emi}
    - Overdue days: {overdue_days}
    - Monthly income: Rs.{monthly_income}
    - Debt stress level: {analysis['debt_stress_level']}
    - Proposed settlement: Rs.{analysis['settlement_amount']} ({analysis['settlement_percentage']}% of outstanding)
    Keep it concise, respectful, and highlight genuine financial hardship with a realistic repayment proposal.
    """

    if USE_GEMINI:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            pass  # fall through to template below

    # Fallback template-based letter (used if no Gemini key / API fails)
    letter = f"""Subject: Request for Loan Settlement – Financial Hardship

Dear {lender_name} Team,

I am writing regarding my outstanding loan of Rs.{outstanding_amount:,.2f}, currently overdue by {overdue_days} days.

Due to a temporary financial hardship, my monthly EMI of Rs.{emi:,.2f} against an income of Rs.{monthly_income:,.2f}
has become difficult to sustain (EMI ratio: {analysis['emi_ratio']}%, debt stress level: {analysis['debt_stress_level']}).

I would like to propose a one-time settlement of Rs.{analysis['settlement_amount']:,.2f}
({analysis['settlement_percentage']}% of the outstanding amount) to fully close this account.

I request you to kindly review my proposal and share a settlement agreement at the earliest.
I am committed to resolving this matter promptly and appreciate your understanding.

Regards,
Borrower
"""
    return letter


# ---------------------------
# Routes
# ---------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/recommend", response_class=HTMLResponse)
def recommend(
    request: Request,
    outstanding_amount: float = Form(...),
    emi: float = Form(...),
    overdue_days: int = Form(...),
    monthly_income: float = Form(...),
    lender_name: str = Form("the Lender"),
):
    analysis = analyze_financial_health(outstanding_amount, emi, overdue_days, monthly_income)
    letter = generate_negotiation_letter(outstanding_amount, emi, overdue_days, monthly_income, analysis, lender_name)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO loans (outstanding_amount, emi, overdue_days, monthly_income, emi_ratio,
                            monthly_surplus, debt_stress_level, settlement_percentage,
                            settlement_amount, negotiation_letter, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (outstanding_amount, emi, overdue_days, monthly_income, analysis["emi_ratio"],
          analysis["monthly_surplus"], analysis["debt_stress_level"], analysis["settlement_percentage"],
          analysis["settlement_amount"], letter, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "outstanding_amount": outstanding_amount,
        "emi": emi,
        "overdue_days": overdue_days,
        "monthly_income": monthly_income,
        "lender_name": lender_name,
        "analysis": analysis,
        "letter": letter,
    })


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM loans ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return templates.TemplateResponse("dashboard.html", {"request": request, "loans": rows})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
