# E-Commerce Scanner Installation Guide

## Prerequisites
- Python 3.12+
- Google API Key (for Gemini Pro)

## Setup

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

4. **Environment Variables:**
   Copy `.env.example` to `.env` and set your `GOOGLE_API_KEY`.
   ```bash
   cp .env.example .env
   # Edit .env with your key
   ```

## Running the Application

Start the server:
```bash
uvicorn app.main:app --reload
```

Access the application at `http://localhost:8000`.
To scan a product, enter the URL in the input field and click "Scan Product".
API documentation is available at `http://localhost:8000/docs`.
