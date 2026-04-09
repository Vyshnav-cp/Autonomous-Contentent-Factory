# Deployment Guide

Complete guide for deploying the Autonomous Content Factory API to production.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Checklist](#production-checklist)
5. [Monitoring & Maintenance](#monitoring--maintenance)

## Local Development

### Setup

```bash
# Clone repository
git clone <repo>
cd Autonomous-Contentent-Factory

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="sk-your-key"

# Run API
python api.py
```

### Access API
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API**: http://localhost:8000

## Docker Deployment

### Build Image

```bash
docker build -t content-factory-api:latest .
```

### Run Container

```bash
docker run -d \
  --name content-factory-api \
  -p 8000:8000 \
  -e OPENAI_API_KEY="sk-your-key" \
  content-factory-api:latest
```

### Using Docker Compose

```bash
# Set API key
export OPENAI_API_KEY="sk-your-key"

# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Verify Container

```bash
# Check if running
docker ps

# View logs
docker logs content-factory-api

# Test health
curl http://localhost:8000/health
```

## Cloud Deployment

### Option 1: Heroku

#### Setup

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY="sk-your-key"

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

#### Procfile

Create `Procfile` in root directory:

```
web: cd backend && python api.py --host 0.0.0.0 --port $PORT
```

### Option 2: AWS EC2

#### Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repository
git clone <repo>
cd Autonomous-Contentent-Factory

# Set API key
export OPENAI_API_KEY="sk-your-key"

# Start with Docker Compose
docker-compose up -d
```

#### Security Groups

Configure inbound rules:
- Port 80 (HTTP)
- Port 443 (HTTPS)
- Port 8000 (API)

#### Nginx Reverse Proxy

```bash
sudo apt install nginx

# Create config
sudo nano /etc/nginx/sites-available/default
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
```

### Option 3: Google Cloud Run

#### Setup

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Create artifact registry
gcloud artifacts repositories create content-factory --repository-format=docker

# Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/content-factory-api:latest

# Deploy to Cloud Run
gcloud run deploy content-factory-api \
  --image gcr.io/YOUR_PROJECT_ID/content-factory-api:latest \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --timeout 600 \
  --set-env-vars OPENAI_API_KEY=sk-your-key \
  --allow-unauthenticated
```

### Option 4: DigitalOcean App Platform

1. Connect GitHub repository
2. Configure app spec:

```yaml
name: content-factory-api
services:
  - name: api
    github:
      branch: main
      repo: your-repo
    build_command: pip install -r backend/requirements.txt
    run_command: python backend/api.py --host 0.0.0.0 --port 8080
    envs:
      - key: OPENAI_API_KEY
        scope: RUN_AND_BUILD_TIME
        value: ${OPENAI_API_KEY}
    http_port: 8080
```

3. Deploy

### Option 5: Railway

1. Login at https://railway.app
2. Import from GitHub
3. Set environment variables
4. Deploy

## Production Checklist

### Security

- [ ] Enable HTTPS with Let's Encrypt
- [ ] Add API authentication (OAuth2/JWT)
- [ ] Enable CORS for specific domains
- [ ] Add rate limiting
- [ ] Use secrets manager for API keys
- [ ] Enable request logging
- [ ] Set up DDoS protection (CloudFlare)

### Performance

- [ ] Enable caching
- [ ] Use CDN for static assets
- [ ] Configure database indexing
- [ ] Set up load balancing
- [ ] Monitor response times
- [ ] Optimize database queries

### Monitoring

- [ ] Set up error tracking (Sentry)
- [ ] Configure log aggregation (ELK/Datadog)
- [ ] Monitor API metrics (New Relic)
- [ ] Set up uptime monitoring
- [ ] Configure alerting

### Maintenance

- [ ] Set up automated backups
- [ ] Configure zero-downtime deployments
- [ ] Document disaster recovery
- [ ] Set up version control
- [ ] Plan regular updates

### Compliance

- [ ] GDPR compliance
- [ ] Data encryption
- [ ] Privacy policy
- [ ] Terms of service
- [ ] Data retention policies

## HTTPS Setup

### Using Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Configure Nginx
sudo nano /etc/nginx/sites-available/default
```

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

```bash
# Restart Nginx
sudo systemctl restart nginx

# Auto-renewal
sudo systemctl enable certbot.timer
```

## Environment Variables

### Required

```bash
OPENAI_API_KEY=sk-...              # OpenAI API key
```

### Optional

```bash
API_HOST=0.0.0.0                   # API host
API_PORT=8000                      # API port
LOG_LEVEL=info                     # Logging level
WORKERS=4                          # Number of workers
DATABASE_URL=postgresql://...      # Database URL
REDIS_URL=redis://...              # Redis URL
```

## Monitoring & Maintenance

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check logs
docker logs content-factory-api

# Monitor performance
docker stats content-factory-api
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Database Backups

```bash
# Monthly backup
0 2 * * * pg_dump dbname > /backups/backup_$(date +%Y%m%d).sql
```

### Updates

```bash
# Pull latest code
git pull origin main

# Rebuild Docker image
docker-compose down
docker-compose up -d --build

# Run migrations (if applicable)
docker-compose exec api python manage.py migrate
```

## Troubleshooting

### High Memory Usage

```bash
# Check memory
docker stats

# Reduce workers
export WORKERS=2

# Restart
docker-compose restart
```

### Slow Response Times

```bash
# Check CPU
docker stats

# Add caching
# See API_DOCUMENTATION.md for caching options

# Scale horizontally
# Deploy multiple instances with load balancer
```

### Database Connection Issues

```bash
# Check connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Restart database service
docker-compose restart db
```

## Scaling

### Horizontal Scaling

```bash
# Using Docker Compose with load balancer
version: '3.8'
services:
  lb:
    image: nginx
    ports:
      - "80:80"
    
  api1:
    build: .
  
  api2:
    build: .
  
  api3:
    build: .
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: content-factory-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: content-factory-api
  template:
    metadata:
      labels:
        app: content-factory-api
    spec:
      containers:
      - name: api
        image: content-factory-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: openai-key
```

## Support & Resources

- **Documentation**: See API_README.md
- **Quick Start**: See API_QUICKSTART.md
- **Examples**: See api_examples.py
- **Issues**: Check troubleshooting section

## Next Steps

1. **Choose deployment platform** (Docker, Cloud, etc.)
2. **Follow platform-specific guide** above
3. **Run production checklist**
4. **Set up monitoring**
5. **Plan maintenance schedule**
6. **Document your setup**

---

**Deploy with confidence!** 🚀
