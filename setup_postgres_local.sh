#!/bin/bash

# Setup PostgreSQL for local development on macOS
echo "Setting up PostgreSQL for local development..."

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL not found. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Homebrew first."
        exit 1
    fi
    brew install postgresql
    brew services start postgresql
else
    echo "PostgreSQL is already installed."
fi

# Create database and user
echo "Creating database and user..."

# Create user and database
createuser -s iris_user 2>/dev/null || echo "User iris_user already exists"
createdb iris_db -O iris_user 2>/dev/null || echo "Database iris_db already exists"

# Set password for user
psql -d postgres -c "ALTER USER iris_user WITH PASSWORD 'iris_password';" 2>/dev/null

echo "PostgreSQL setup completed!"
echo "Database: iris_db"
echo "User: iris_user"
echo "Password: iris_password"
echo "Host: localhost"
echo "Port: 5432"

# Test connection
echo "Testing connection..."
if psql -h localhost -U iris_user -d iris_db -c "SELECT version();" &>/dev/null; then
    echo "✅ Connection successful!"
else
    echo "❌ Connection failed. Please check your PostgreSQL installation."
fi
