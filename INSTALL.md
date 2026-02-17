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

## Deployment

### Manual Deployment on DigitalOcean (Ubuntu)

This guide assumes you have a DigitalOcean Droplet running Ubuntu (22.04 or 24.04).

#### 1. System Setup
SSH into your droplet and install necessary system dependencies:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git
```

#### 2. Clone Repository
Clone your repository to the server (e.g., to `/var/www/ecommerce-scanner`):

```bash
cd /var/www
git clone <YOUR_REPO_URL> ecommerce-scanner
cd ecommerce-scanner
```

#### 3. Install Dependencies
Create a virtual environment and verify python version (must be 3.12+):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**CRITICAL STEP**: Install Playwright browsers and system dependencies:

```bash
playwright install
sudo playwright install-deps
```
*Note: `install-deps` requires sudo and installs libraries needed for Chromium to run.*

#### 4. Configuration
Create your `.env` file with your production API keys and password:

```bash
cp .env.example .env
nano .env
# Set GOOGLE_API_KEY and ACCESS_PASSWORD
```

#### 5. Setup Systemd Service
To keep the app running in the background and restart on reboot:

1.  Edit the service file `service/ecommerce-scanner.service` to match your actual paths (if different from `/var/www/ecommerce-scanner`).
2.  Copy it to the systemd directory:

```bash
sudo cp service/ecommerce-scanner.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start ecommerce-scanner
sudo systemctl enable ecommerce-scanner
```

#### 6. Access
The application will be running on port 8000.
You can access it at `http://<YOUR_DROPLET_IP>:8000`.

*(Optional) To serve on port 80/443, set up Nginx as a reverse proxy.*
