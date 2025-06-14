# IRIS Task Management System - Backend

A Django-based task management system with PostgreSQL database support.

## 🚀 Quick Start - Local Development

### Prerequisites
- Python 3.11+
- PostgreSQL
- Git

### Local Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd IRIs_task_backend_revised

# Setup PostgreSQL (macOS)
./setup_postgres_local.sh

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load sample data (if available)
python manage.py loaddata user_data_backup.json

# Start development server
python manage.py runserver
```

## 🌐 EC2 Deployment Guide

### Step 1: Prepare Your EC2 Instance

**Launch EC2 Instance:**
- AMI: Amazon Linux 2
- Instance Type: t3.micro or larger
- Security Group: Allow ports 22 (SSH), 8000 (Django), 3000 (React)

**Connect to EC2:**
```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

### Step 2: Upload Project Files

**Option A: Using SCP (from your local machine):**
```bash
# Upload backend
scp -i your-key.pem -r IRIs_task_backend_revised ec2-user@your-ec2-ip:~/

# Upload data backup
scp -i your-key.pem IRIs_task_backend_revised/user_data_backup.json ec2-user@your-ec2-ip:~/
```

**Option B: Using Git (recommended):**
```bash
# On EC2 instance
sudo yum install -y git
git clone your-repository-url
cd your-repository-name
```

### Step 3: Setup PostgreSQL on EC2

```bash
# Make setup script executable
chmod +x IRIs_task_backend_revised/setup_postgres_ec2.sh

# Run PostgreSQL setup
./IRIs_task_backend_revised/setup_postgres_ec2.sh
```

This script will:
- Install PostgreSQL
- Create database `iris_db`
- Create user `iris_user` with password `iris_password`
- Configure PostgreSQL for local connections

### Step 4: Setup Django Application

```bash
# Navigate to project directory
cd IRIs_task_backend_revised

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Load your data backup
python manage.py loaddata ~/user_data_backup.json

# Create superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver 0.0.0.0:8000
```

### Step 5: Configure Security Groups

In AWS Console, ensure your security group allows:
- **Port 22**: SSH (source: your IP)
- **Port 8000**: Django backend (source: 0.0.0.0/0 or your IP)
- **Port 3000**: React frontend (source: 0.0.0.0/0 or your IP)

### Step 6: Test Your Deployment

```bash
# Check if Django is running
curl http://localhost:8000

# Check from external browser
http://your-ec2-public-ip:8000
```

## 📁 Project Structure

```
IRIs_task_backend_revised/
├── irisbackend/           # Django project settings
│   ├── settings.py        # Database & app configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── tasks/                 # Main application
│   ├── models.py         # Database models
│   ├── views.py          # API views
│   ├── urls.py           # App URLs
│   └── serializers.py    # DRF serializers
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
├── setup_postgres_ec2.sh # EC2 PostgreSQL setup
├── setup_postgres_local.sh # Local PostgreSQL setup
└── user_data_backup.json # Data backup file
```

## 🗄️ Database Configuration

**PostgreSQL Settings:**
- Database: `iris_db`
- User: `iris_user`
- Password: `iris_password`
- Host: `localhost`
- Port: `5432`

## 🔧 Production Considerations

### Setup Gunicorn (WSGI Server)
```bash
# Install Gunicorn
pip install gunicorn

# Test Gunicorn
gunicorn --bind 0.0.0.0:8000 irisbackend.wsgi:application

# Create Gunicorn service file
sudo nano /etc/systemd/system/gunicorn.service
```

**Gunicorn Service Configuration:**
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/IRIs_task_backend_revised
ExecStart=/home/ec2-user/IRIs_task_backend_revised/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ec2-user/IRIs_task_backend_revised/irisbackend.sock irisbackend.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Start Gunicorn Service:**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

### Setup Nginx (Reverse Proxy)
```bash
# Install Nginx
sudo yum install -y nginx

# Create Nginx configuration
sudo nano /etc/nginx/conf.d/iris-task.conf
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com your-ec2-public-ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ec2-user/IRIs_task_backend_revised;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ec2-user/IRIs_task_backend_revised/irisbackend.sock;
        
        # CORS headers for Firebase frontend
        add_header 'Access-Control-Allow-Origin' 'https://iris-task.web.app' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Accept, Authorization, Cache-Control, Content-Type, DNT, If-Modified-Since, Keep-Alive, Origin, User-Agent, X-Requested-With, X-CSRFToken' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;
        
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }
}
```

**Start Nginx:**
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

### Setup HTTPS with Let's Encrypt
```bash
# Install Certbot
sudo yum install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

**Updated Nginx Configuration with HTTPS:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ec2-user/IRIs_task_backend_revised;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ec2-user/IRIs_task_backend_revised/irisbackend.sock;
        
        # CORS headers for Firebase frontend
        add_header 'Access-Control-Allow-Origin' 'https://iris-task.web.app' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Accept, Authorization, Cache-Control, Content-Type, DNT, If-Modified-Since, Keep-Alive, Origin, User-Agent, X-Requested-With, X-CSRFToken' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;
        
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }
}
```

### Update Django Settings for Production
```python
# Add to settings.py
import os

# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings for Firebase
CORS_ALLOWED_ORIGINS = [
    "https://iris-task.web.app",
    "https://iris-task.firebaseapp.com",
]

CORS_ALLOW_CREDENTIALS = True

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Allowed hosts
ALLOWED_HOSTS = ['your-domain.com', 'your-ec2-public-ip']
```

### Collect Static Files
```bash
# Collect static files for Nginx to serve
python manage.py collectstatic --noinput
```

### Firebase Frontend Configuration
Update your Firebase frontend to use the HTTPS API:

**In your React .env file:**
```bash
REACT_APP_API_BASE_URL=https://your-domain.com
```

**Update axios configuration:**
```javascript
// In your React app
const axiosInstance = axios.create({
  baseURL: 'https://your-domain.com',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
});
```

### Complete Production Deployment Script
```bash
#!/bin/bash
# production_deploy.sh

# Setup PostgreSQL
./setup_postgres_ec2.sh

# Setup Django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Database setup
python manage.py migrate
python manage.py loaddata ~/user_data_backup.json
python manage.py collectstatic --noinput

# Setup Gunicorn service
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Setup Nginx
sudo cp iris-task.conf /etc/nginx/conf.d/
sudo systemctl start nginx
sudo systemctl enable nginx

# Setup SSL
sudo certbot --nginx -d your-domain.com

echo "Production deployment completed!"
echo "Your API is now available at: https://your-domain.com"
echo "Configure your Firebase frontend to use this URL"
```

### Use Process Manager (PM2) - Alternative to Systemd
```bash
# Install PM2
npm install -g pm2

# Start Django with PM2 and Gunicorn
pm2 start gunicorn --name "iris-backend" -- --bind 0.0.0.0:8000 irisbackend.wsgi:application

# Save PM2 configuration
pm2 save
pm2 startup
```

### Environment Variables
Create `.env` file for production:
```bash
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-public-ip
DATABASE_URL=postgresql://iris_user:iris_password@localhost:5432/iris_db
SECRET_KEY=your-secret-key-here
CORS_ALLOWED_ORIGINS=https://iris-task.web.app,https://iris-task.firebaseapp.com
```

## 🐛 Troubleshooting

### Common Issues:

1. **Database Connection Error:**
   ```bash
   sudo systemctl status postgresql
   sudo systemctl start postgresql
   ```

2. **Port Already in Use:**
   ```bash
   netstat -tlnp | grep :8000
   kill -9 <process-id>
   ```

3. **Permission Denied:**
   ```bash
   chown -R ec2-user:ec2-user ~/IRIs_task_backend_revised
   ```

4. **Virtual Environment Issues:**
   ```bash
   deactivate
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   ```

### Useful Commands:
```bash
# Check running processes
ps aux | grep python

# View Django logs
tail -f /var/log/django.log

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log

# Test database connection
python manage.py dbshell
```

## 📊 API Endpoints

- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get specific task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

## 🔐 Authentication

The system uses Django's session-based authentication. Make sure to:
1. Create a superuser: `python manage.py createsuperuser`
2. Login via Django admin: `http://your-server:8000/admin/`
3. Use session cookies for API authentication

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all services are running
3. Check security group configurations
4. Review Django and PostgreSQL logs

## 🎯 Next Steps

1. Set up SSL certificates (Let's Encrypt)
2. Configure automatic backups
3. Set up monitoring and logging
4. Configure domain name
5. Set up CI/CD pipeline

Your IRIS Task Management System backend is now ready for production! 🎉
