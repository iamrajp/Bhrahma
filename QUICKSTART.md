# Bhrahma - Quick Start Guide

Get Bhrahma up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- At least one LLM API key (Anthropic Claude, OpenAI, or Mixtral)

## Step 1: Setup

Run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Initialize the database
- Import default skills

## Step 2: Configure API Keys

Edit the `.env` file and add your API key(s):

```bash
nano .env
```

Add at least one API key:

```env
ANTHROPIC_API_KEY=sk-ant-...
# or
OPENAI_API_KEY=sk-...
# or
MIXTRAL_API_KEY=...
```

Set your default LLM:

```env
DEFAULT_LLM=anthropic  # or openai, or mixtral
```

Save and exit.

## Step 3: Run

Start both backend and frontend:

```bash
./run.sh
```

Or run them separately:

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
source venv/bin/activate
cd frontend
streamlit run app.py
```

## Step 4: Chat with Bhrahma

1. Open your browser to `http://localhost:8501`
2. Type a message: "Hello Bhrahma, what can you do?"
3. Watch Bhrahma respond!

## Try These Examples

### Ask a Question
```
"Explain how asyncio works in Python"
```

### Learn a New Skill
```
"Learn how to create FastAPI endpoints with authentication"
```

### Complex Task (Multi-Agent)
```
"Compare Python, JavaScript, and Go for building web APIs"
```

Bhrahma will automatically:
- Select relevant skills
- Spawn sub-agents if needed
- Search the web to learn new skills
- Provide comprehensive answers

## View Skills

Check the sidebar to see:
- Available skills
- Queue status
- Learn new skills

## API Access

Access the API directly:

```bash
# Check health
curl http://localhost:8000/health

# List skills
curl http://localhost:8000/skills

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello!"}'
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Create custom skills in the `skills/` directory
- Download Anthropic skills: `python backend/utils/import_skills.py --source anthropic`
- Explore the API docs at `http://localhost:8000/docs`

## Troubleshooting

**Backend won't start:**
- Check your API key is valid in `.env`
- Ensure port 8000 is not in use

**Frontend won't connect:**
- Make sure backend is running first
- Check `http://localhost:8000/health`

**No response from Bhrahma:**
- Check the queue status in the sidebar
- Look at backend logs for errors

## Need Help?

- Check [README.md](README.md) for full documentation
- Review error messages in the terminal
- Ensure all dependencies are installed

Enjoy using Bhrahma! 🧠
