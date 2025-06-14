#!/bin/bash

# Setup PostgreSQL for EC2 Amazon Linux deployment
echo "Setting up PostgreSQL on EC2 Amazon Linux..."

# Update system packages
sudo yum update -y

# Install PostgreSQL
echo "Installing PostgreSQL..."
sudo yum install -y postgresql postgresql-server postgresql-devel

# Initialize PostgreSQL database
echo "Initializing PostgreSQL database..."
sudo postgresql-setup initdb

# Start and enable PostgreSQL service
echo "Starting PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Configure PostgreSQL for local connections
echo "Configuring PostgreSQL..."

# Update pg_hba.conf to allow local connections
sudo sed -i "s/#local   all             all                                     peer/local   all             all                                     md5/" /var/lib/pgsql/data/pg_hba.conf
sudo sed -i "s/local   all             all                                     peer/local   all             all                                     md5/" /var/lib/pgsql/data/pg_hba.conf

# Update postgresql.conf to listen on localhost
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" /var/lib/pgsql/data/postgresql.conf

# Restart PostgreSQL to apply configuration changes
sudo systemctl restart postgresql

# Create database and user
echo "Creating database and user..."
sudo -u postgres psql -c "CREATE DATABASE iris_db;"
sudo -u postgres psql -c "CREATE USER iris_user WITH PASSWORD 'iris_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE iris_db TO iris_user;"
sudo -u postgres psql -c "ALTER USER iris_user CREATEDB;"

# Test connection
echo "Testing PostgreSQL connection..."
if sudo -u postgres psql -h localhost -U iris_user -d iris_db -c "SELECT version();" &>/dev/null; then
    echo "✅ PostgreSQL setup completed successfully!"
    echo "Database: iris_db"
    echo "User: iris_user"
    echo "Password: iris_password"
    echo "Host: localhost"
    echo "Port: 5432"
else
    echo "❌ PostgreSQL setup failed. Please check the installation."
    exit 1
fi

# Install Python development packages
echo "Installing Python development packages..."
sudo yum groupinstall -y "Development Tools"
sudo yum install -y python3-devel python3-pip

echo "PostgreSQL setup for EC2 completed!"
echo "Next steps:"
echo "1. Navigate to your project directory: cd IRIs_task_backend_revised"
echo "2. Create virtual environment: python3 -m venv venv"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Install requirements: pip install -r requirements.txt"
echo "5. Run migrations: python manage.py migrate"
echo "6. Load your data: python manage.py loaddata ~/user_data_backup.json"
echo "7. Start server: python manage.py runserver 0.0.0.0:8000"
