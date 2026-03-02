#!/bin/bash

echo "🚂 Bhrahma Railway Deployment Script"
echo "======================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI is installed"
echo ""

# Check if logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    echo "This will open a browser window for authentication."
    echo ""
    railway login

    if [ $? -ne 0 ]; then
        echo "❌ Login failed. Please try again."
        exit 1
    fi
fi

echo "✅ Logged in to Railway"
echo ""

# Initialize Railway project
echo "📦 Initializing Railway project..."
if [ ! -f ".railway/config.json" ]; then
    railway init

    if [ $? -ne 0 ]; then
        echo "❌ Failed to initialize Railway project"
        exit 1
    fi
fi

echo "✅ Railway project initialized"
echo ""

# Deploy backend
echo "🚀 Deploying backend service..."
echo "This will use Dockerfile.backend"
echo ""

railway up -d Dockerfile.backend

if [ $? -eq 0 ]; then
    echo "✅ Backend deployed successfully!"
else
    echo "❌ Backend deployment failed"
    exit 1
fi

echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Set environment variables in Railway dashboard:"
echo "   - ANTHROPIC_API_KEY"
echo "   - OPENAI_API_KEY"
echo "   - MIXTRAL_API_KEY"
echo "   - DEFAULT_LLM=anthropic"
echo ""
echo "2. Create a second service for the frontend:"
echo "   - Go to Railway dashboard"
echo "   - Click 'New Service'"
echo "   - Select your GitHub repo"
echo "   - Set Dockerfile path to 'Dockerfile.frontend'"
echo "   - Add environment variable: API_URL=<your-backend-url>"
echo ""
echo "3. Get your deployment URLs:"
echo "   railway status"
echo ""
echo "🎉 Backend deployment complete!"
echo ""
echo "Visit Railway dashboard: https://railway.app/dashboard"
