#!/bin/bash
# Complete production deployment script for IRIS Task Management System

echo "🚀 Starting IRIS Task Management System Production Deployment..."

# Setup PostgreSQL
echo "📊 Setting up PostgreSQL..."
chmod +x setup_postgres_ec2.sh
./setup_postgres_ec2.sh

# Setup Django
echo "🐍 Setting up Django application..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Database setup
echo "🗄️ Setting up database..."
python manage.py migrate
python manage.py loaddata ~/user_data_backup.json
python manage.py collectstatic --noinput

# Setup Gunicorn service
echo "⚙️ Setting up Gunicorn service..."
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Setup Nginx
echo "🌐 Setting up Nginx..."
sudo yum install -y nginx
sudo cp iris-task.conf /etc/nginx/conf.d/
sudo systemctl start nginx
sudo systemctl enable nginx

# Setup SSL (requires domain name)
echo "🔒 Setting up SSL certificate..."
echo "Please run the following command manually with your domain:"
echo "sudo certbot --nginx -d your-domain.com"

echo "✅ Production deployment completed!"
echo ""
echo "🎯 Next steps:"
echo "1. Point your domain to this EC2 instance"
echo "2. Run: sudo certbot --nginx -d your-domain.com"
echo "3. Update your Firebase frontend to use: https://your-domain.com"
echo "4. Test your API endpoints"
echo ""
echo "📋 Service status:"
echo "PostgreSQL: $(sudo systemctl is-active postgresql)"
echo "Gunicorn: $(sudo systemctl is-active gunicorn)"
echo "Nginx: $(sudo systemctl is-active nginx)"
