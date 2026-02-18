# Deployment Guide - E-Commerce Scanner (Docker)

This guide explains how to deploy the E-Commerce Scanner application directly on a DigitalOcean Droplet (or any Linux server) using Docker.

## Prerequisites

1.  **Server**: A DigitalOcean Droplet (or compatible Linux server) with at least 2GB RAM.
2.  **Git**: Installed on the server to clone the repo (optional but recommended).

## Method: Build on Server
This method involves copying your project to the server and building the Docker image there.

### Step 1: Install Docker
SSH into your server and run:
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker && sudo systemctl enable docker
```

### Step 2: Transfer Project Files
You can clone your repository or copy files manually.

**Option A: Git Clone (Recommended)**
```bash
git clone <your-repository-url>
cd ecommerce-scanner
```

**Option B: Copy Files Manually**
Ensure these files are on the server:
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `requirements.txt`
- `app/` & `static/` directories
- `.env` (create manually, see below)

### Step 3: Configure Environment
Create a `.env` file in the project directory:

```bash
nano .env
```

Paste your environment variables:
```env
GOOGLE_API_KEY=your_key
ACCESS_PASSWORD=your_password
HOST=0.0.0.0
# Port config (Change this if running multiple apps)
HOST_PORT=8000
```

### Step 4: Build and Run
Run the application using Docker Compose:

```bash
# Build and start in background
sudo docker-compose up -d --build
```

## Multi-App Hosting
If hosting multiple projects on this server, ensure each project has a unique `HOST_PORT` in its `.env` file.

### 1. Assign Unique Ports
For a second app, edit its `.env` file:
```env
...
HOST_PORT=8001
```

Then run:
```bash
# Run with a unique project name (-p) to avoid checking existing containers
sudo docker-compose -p scanner_app_2 up -d --build
```

### 2. Set up Nginx Reverse Proxy (On Host)
To access apps via domains (e.g., `scanner.com` -> 8001), install Nginx on the server.

1.  **Install Nginx**: `sudo apt install -y nginx`
2.  **Create Config**: `sudo nano /etc/nginx/sites-available/scanner.com`
    ```nginx
    server {
        listen 80;
        server_name scanner.com;

        location / {
            proxy_pass http://localhost:8001; # Match your HOST_PORT
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```
3.  **Enable**: `sudo ln -s /etc/nginx/sites-available/scanner.com /etc/nginx/sites-enabled/`
4.  **Restart**: `sudo systemctl restart nginx`

## Common Commands
- **Logs**: `sudo docker-compose logs -f`
- **Stop**: `sudo docker-compose down`
- **Rebuild**: `sudo docker-compose up -d --build`
