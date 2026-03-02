# 🚀 Deploy Bhrahma to Railway NOW

## Quick Start (5 minutes)

### Option 1: Deploy from GitHub (Recommended - No CLI needed!)

1. **Open Railway Dashboard**
   - Visit: https://railway.app/new
   - Sign in with your GitHub account

2. **Deploy Backend Service**
   - Click "Deploy from GitHub repo"
   - Select: `iamrajp/Bhrahma`
   - Railway will automatically detect the project
   - Under "Settings" tab:
     - Set "Root Directory": leave blank
     - Set "Dockerfile Path": `Dockerfile.backend`
   - Under "Variables" tab, add:
     ```
     ANTHROPIC_API_KEY = <your_key_from_.env>
     OPENAI_API_KEY = <your_key_from_.env>
     MIXTRAL_API_KEY = <your_key_from_.env>
     DEFAULT_LLM = anthropic
     PORT = 8000
     ```
   - Click "Deploy"
   - Wait for deployment (2-3 minutes)
   - Copy the backend URL (e.g., `https://bhrahma-backend.railway.app`)

3. **Deploy Frontend Service**
   - In the same Railway project, click "New Service"
   - Click "GitHub Repo"
   - Select: `iamrajp/Bhrahma` (same repo)
   - Under "Settings" tab:
     - Set "Root Directory": leave blank
     - Set "Dockerfile Path": `Dockerfile.frontend`
   - Under "Variables" tab, add:
     ```
     API_URL = <paste_your_backend_url_from_step_2>
     PORT = 8501
     ```
   - Click "Deploy"
   - Wait for deployment (2-3 minutes)
   - Copy the frontend URL (e.g., `https://bhrahma-frontend.railway.app`)

4. **Done! 🎉**
   - Open the frontend URL in your browser
   - Start chatting with Bhrahma!

### Option 2: Deploy via CLI

1. **Login to Railway**
   ```bash
   railway login
   ```
   This opens a browser for authentication.

2. **Run the deployment script**
   ```bash
   cd /Users/priyanksharma/Desktop/Bhrahma/Bhrahma
   ./deploy_railway.sh
   ```

3. **Follow the prompts**
   - The script will guide you through the deployment
   - Add environment variables in Railway dashboard
   - Create frontend service manually

## Your API Keys

Copy these from your `.env` file:

```bash
# Backend will need these
ANTHROPIC_API_KEY=<from your .env>
OPENAI_API_KEY=<from your .env>
MIXTRAL_API_KEY=<from your .env>
DEFAULT_LLM=anthropic
```

## Expected Timeline

- Backend deployment: ~3 minutes
- Frontend deployment: ~3 minutes
- Total time: ~5-8 minutes

## Cost

- **Starter Plan**: $5/month (enough for development)
- **Free Trial**: Available for new users

## Verify Deployment

After deployment:

1. **Test Backend**
   ```bash
   curl https://your-backend.railway.app/health
   ```
   Should return:
   ```json
   {
     "status": "healthy",
     "database": "connected",
     "queue": "running",
     "available_llms": ["anthropic", "openai", "mixtral"]
   }
   ```

2. **Test Frontend**
   - Open: `https://your-frontend.railway.app`
   - You should see the Bhrahma chat interface
   - Try sending a message

## Troubleshooting

### Backend Issues
- Check logs: Railway Dashboard → Backend Service → Logs
- Verify all environment variables are set
- Ensure health endpoint returns 200 OK

### Frontend Issues
- Check logs: Railway Dashboard → Frontend Service → Logs
- Verify `API_URL` points to your backend (with https://)
- Ensure backend is deployed first

### Database Issues
- Railway provides ephemeral storage by default
- For persistence, add a Volume:
  - Settings → Storage → Add Volume
  - Mount path: `/app/database`

## Post-Deployment

Once deployed, you can:

1. **Ask Bhrahma to learn new skills**
   ```
   "Learn about pytest from https://docs.pytest.org"
   ```

2. **Use existing skills**
   - skill-creator is pre-loaded
   - Skills appear in the sidebar

3. **Monitor usage**
   - Railway Dashboard shows metrics
   - CPU, memory, and network usage

## Need Help?

- Railway Docs: https://docs.railway.app
- Bhrahma GitHub: https://github.com/iamrajp/Bhrahma
- Deployment Guide: `RAILWAY_DEPLOYMENT.md`

---

**Ready?** Start here: https://railway.app/new

Select "Deploy from GitHub repo" → `iamrajp/Bhrahma`
