# Railway Deployment Guide for Bhrahma

This guide will help you deploy the Bhrahma Agentic System to Railway.

## Prerequisites

- Railway account (sign up at https://railway.app)
- Railway CLI installed (already done)
- GitHub repository (already created at https://github.com/iamrajp/Bhrahma)

## Deployment Steps

### Option 1: Deploy via Railway Dashboard (Recommended - Easiest)

1. **Go to Railway Dashboard**
   - Visit: https://railway.app/new
   - Click "Deploy from GitHub repo"

2. **Connect GitHub Repository**
   - Select your repository: `iamrajp/Bhrahma`
   - Railway will automatically detect the project

3. **Deploy Backend Service**
   - Click "Add Service" → "GitHub Repo"
   - Select `Bhrahma` repository
   - Railway will auto-detect Python and use `Dockerfile.backend`
   - Under "Settings" → "Dockerfile Path", set: `Dockerfile.backend`
   - Under "Variables", add:
     - `ANTHROPIC_API_KEY` = your_anthropic_key
     - `OPENAI_API_KEY` = your_openai_key
     - `MIXTRAL_API_KEY` = your_mixtral_key
     - `DEFAULT_LLM` = anthropic
     - `PORT` = 8000
   - Click "Deploy"

4. **Deploy Frontend Service**
   - Click "New Service" → "GitHub Repo"
   - Select `Bhrahma` repository again
   - Under "Settings" → "Dockerfile Path", set: `Dockerfile.frontend`
   - Under "Variables", add:
     - `PORT` = 8501
   - Update `frontend/app.py` line 12 to use backend URL:
     - `API_URL = "https://your-backend-url.railway.app"`
   - Click "Deploy"

5. **Access Your App**
   - Backend API: `https://your-backend-service.railway.app`
   - Frontend UI: `https://your-frontend-service.railway.app`

### Option 2: Deploy via Railway CLI

1. **Login to Railway**
   ```bash
   railway login
   ```
   This will open a browser for authentication.

2. **Initialize Project**
   ```bash
   railway init
   ```
   - Enter project name: `Bhrahma`
   - This creates a new Railway project

3. **Link to GitHub (Optional)**
   ```bash
   railway link
   ```

4. **Deploy Backend**
   ```bash
   # Create backend service
   railway up -d Dockerfile.backend
   ```

5. **Add Environment Variables**
   ```bash
   railway variables set ANTHROPIC_API_KEY=your_key
   railway variables set OPENAI_API_KEY=your_key
   railway variables set MIXTRAL_API_KEY=your_key
   railway variables set DEFAULT_LLM=anthropic
   ```

6. **Deploy Frontend**
   - Create a second service in Railway dashboard
   - Deploy using `Dockerfile.frontend`

## Configuration Details

### Backend Service
- **Dockerfile**: `Dockerfile.backend`
- **Port**: 8000
- **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- **Health Check**: `/health`

### Frontend Service
- **Dockerfile**: `Dockerfile.frontend`
- **Port**: 8501
- **Start Command**: `streamlit run frontend/app.py --server.port=$PORT`

## Post-Deployment

1. **Update Frontend API URL**
   - Get your backend URL from Railway dashboard
   - Update `frontend/app.py` line 12:
     ```python
     API_URL = "https://your-backend-url.railway.app"
     ```
   - Commit and push to trigger redeployment

2. **Enable Persistence (Optional)**
   - Add Railway Volume for SQLite database
   - Mount at `/app/database`

3. **Monitor Logs**
   ```bash
   railway logs
   ```

## Troubleshooting

### Database Issues
- Railway provides ephemeral storage by default
- For persistence, add a Volume in Settings → Storage
- Mount path: `/app/database`

### Port Issues
- Make sure to use `$PORT` environment variable
- Railway assigns ports dynamically

### Environment Variables
- Verify all API keys are set correctly
- Check Railway dashboard → Variables tab

## Estimated Costs

- **Starter Plan**: $5/month
  - 512 MB RAM
  - 1 GB Disk
  - 100 GB Egress
  - Perfect for development/testing

- **Developer Plan**: $20/month
  - More resources for production use

## Next Steps

After deployment:
1. Test the API endpoint: `https://your-backend.railway.app/health`
2. Open the frontend: `https://your-frontend.railway.app`
3. Start chatting with Bhrahma!

---

**Quick Deploy Button** (Coming soon)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)
