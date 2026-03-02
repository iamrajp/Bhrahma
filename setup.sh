#!/bin/bash

# Bhrahma Setup Script

echo "🧠 Setting up Bhrahma Agentic System..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
else
    echo ".env file already exists"
fi

# Initialize database
echo "Initializing database..."
cd backend
python -c "from models.database import init_database; init_database()"
cd ..

# Import default skills
echo "Importing default skills..."
cd backend
python utils/import_skills.py --source local
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Run ./run.sh to start the application"
echo "3. Or run backend and frontend separately:"
echo "   - Backend: cd backend && python main.py"
echo "   - Frontend: cd frontend && streamlit run app.py"
