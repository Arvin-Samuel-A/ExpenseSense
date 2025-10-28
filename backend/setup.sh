#!/bin/bash

# ExpenseSense Backend Setup Script
# This script automates the backend setup process

set -e  # Exit on error

echo "========================================"
echo "🚀 ExpenseSense Backend Setup"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.10+${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python found: $(python3 --version)${NC}"

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo -e "${YELLOW}⚠️  MySQL not found. Please install MySQL 8.0+${NC}"
    echo "   Installation: brew install mysql (macOS) or apt install mysql-server (Linux)"
    exit 1
fi

echo -e "${GREEN}✅ MySQL found${NC}"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Setup environment file
echo ""
if [ ! -f ".env" ]; then
    echo "🔐 Setting up environment file..."
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env file with your configuration${NC}"
    echo ""
    read -p "Press Enter to edit .env file or Ctrl+C to exit..."
    ${EDITOR:-nano} .env
else
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
fi

# Database setup
echo ""
echo "💾 Database Setup"
echo "Please provide MySQL credentials:"
read -p "MySQL root password: " -s MYSQL_PASSWORD
echo ""

# Create database
echo ""
echo "🗄️  Creating database..."
mysql -u root -p${MYSQL_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS expensesense_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || {
    echo -e "${RED}❌ Failed to create database. Please check your MySQL password.${NC}"
    exit 1
}
echo -e "${GREEN}✅ Database created${NC}"

# Run migrations
echo ""
echo "🔄 Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✅ Migrations completed${NC}"

# Create superuser
echo ""
echo "👤 Create superuser account"
python manage.py createsuperuser

# Collect static files
echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput
echo -e "${GREEN}✅ Static files collected${NC}"

# Train ML model (optional)
echo ""
read -p "🤖 Do you want to train the ML model now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧠 Training ML model (this may take 2-3 minutes)..."
    cd ml_model
    python train_model.py
    cd ..
    echo -e "${GREEN}✅ ML model trained${NC}"
else
    echo -e "${YELLOW}⚠️  Skipped ML model training. You can train later with: cd ml_model && python train_model.py${NC}"
fi

# Final message
echo ""
echo "========================================"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "========================================"
echo ""
echo "To start the development server:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run server: python manage.py runserver"
echo ""
echo "Admin panel: http://localhost:8000/admin/"
echo "API base URL: http://localhost:8000/"
echo ""
echo "Test the API with: python test_api.py"
echo ""
echo "To use Docker instead:"
echo "  1. Edit .env file"
echo "  2. Run: docker-compose up --build"
echo ""
echo -e "${GREEN}Happy coding! 💻${NC}"
