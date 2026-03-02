# Bhrahma Agentic System

An advanced AI agent system capable of learning new skills from the internet, spawning multiple sub-agents for parallel task execution, and integrating with multiple LLM providers.

## 📚 Documentation

- **[Technical Highlights](TECHNICAL_HIGHLIGHTS.md)** - Deep dive into architecture, design patterns, and innovations
- **[Tech Stack Overview](TECH_STACK.md)** - Quick reference for technologies and data flows
- **[Demo Script](DEMO_SCRIPT.md)** - Complete demo screenplay for presentations
- **[Demo Recording Guide](DEMO_RECORDING_GUIDE.md)** - How to record a professional demo video
- **[Railway Deployment](RAILWAY_DEPLOYMENT.md)** - Production deployment guide
- **[Quick Deploy Guide](DEPLOY_NOW.md)** - 5-minute deployment to Railway

## ✨ Key Features

- 🧠 **Self-Learning Agent**: Autonomously learns new skills from web documentation
- 🔀 **Multi-LLM Support**: Integrate with Anthropic Claude, OpenAI GPT-4, and Mixtral
- ⚡ **Parallel Execution**: Spawn multiple sub-agents for complex tasks
- 📚 **Agent Skills Format**: Uses Anthropic's SKILL.md specification
- 💬 **Real-time Chat**: Interactive Streamlit web interface
- 🔄 **Message Queue**: Asynchronous task processing
- 🌐 **Web Intelligence**: Deep documentation crawling and extraction
- 💾 **Persistent Storage**: Skills are saved and reusable across sessions

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/iamrajp/Bhrahma.git
cd Bhrahma
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Configure (add your API keys)
cp .env.example .env
nano .env

# 3. Run
python backend/main.py &           # Backend on :8000
streamlit run frontend/app.py      # Frontend on :8501
```

## 🎯 What Makes Bhrahma Special

1. **Dynamic Skill Learning**: Ask "Learn pytest from https://docs.pytest.org" and Bhrahma will:
   - Crawl the documentation
   - Extract key information
   - Generate a reusable skill
   - Store it for future use

2. **Intelligent Orchestration**: For complex queries like "Compare Python, JavaScript, and Go", Bhrahma will:
   - Decompose into subtasks
   - Spawn parallel agents
   - Synthesize results

3. **Production Ready**: Docker containers, Railway deployment, proper error handling, logging, and monitoring

## Architecture

```
Bhrahma/
├── backend/              # FastAPI backend
│   ├── models/          # Database models and schemas
│   ├── services/        # LLM clients, skill manager, web search
│   ├── agents/          # Bhrahma agent and skill creator
│   ├── api/             # API routes
│   ├── utils/           # Utility scripts
│   └── main.py          # FastAPI application
├── frontend/            # Streamlit chat interface
│   └── app.py
├── skills/              # Agent skills directory
│   └── skill-creator/   # Default skill-creator skill
├── database/            # SQLite database
└── logs/                # Application logs
```

## Prerequisites

- Python 3.9+
- Git (for downloading Anthropic skills)
- API keys for at least one LLM provider

## Installation

### 1. Clone the Repository

```bash
cd Bhrahma
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required: At least one LLM API key
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
MIXTRAL_API_KEY=your_mixtral_api_key_here

# Default LLM (anthropic, openai, or mixtral)
DEFAULT_LLM=anthropic

# Optional: Web search API keys for skill learning
GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
BRAVE_SEARCH_API_KEY=your_brave_search_api_key_here
```

### 5. Initialize Database

```bash
cd backend
python -c "from models.database import init_database; init_database()"
```

### 6. Import Default Skills

Import the built-in skill-creator skill:

```bash
python utils/import_skills.py --source local
```

Optionally, download and import skills from Anthropic's repository:

```bash
python utils/import_skills.py --source anthropic
```

## Running the Application

### Start the Backend Server

In one terminal:

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### Start the Frontend

In another terminal:

```bash
cd frontend
streamlit run app.py
```

The chat interface will open in your browser at `http://localhost:8501`

## Usage

### Basic Chat

1. Open the Streamlit interface in your browser
2. Type your message in the chat input
3. Bhrahma will process your request and respond
4. Messages are queued and processed asynchronously

### Learning New Skills

#### Via Chat Interface

Simply ask Bhrahma to learn something:

```
"Learn how to generate Python unit tests with pytest"
```

#### Via Sidebar

1. Click "Learn New Skill" in the sidebar
2. Enter the topic (e.g., "Python testing with pytest")
3. Enter what the skill should do
4. Click "Learn Skill"

#### Via API

```bash
curl -X POST "http://localhost:8000/skills/learn" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Python testing with pytest",
    "description": "Generate unit tests for Python code",
    "search_web": true,
    "auto_test": true
  }'
```

### Viewing Skills

- **In Chat Interface**: Check the sidebar under "Available Skills"
- **Via API**:

```bash
curl http://localhost:8000/skills
```

### Multi-Agent Execution

Bhrahma automatically spawns sub-agents for complex tasks. Try asking:

```
"Compare the differences between React, Vue, and Svelte frameworks"
```

Bhrahma will:
1. Decompose the task into subtasks
2. Spawn multiple sub-agents
3. Execute them in parallel
4. Synthesize the results

### Queue Status

Monitor the message queue in the sidebar:
- **Ready**: No messages being processed
- **Processing**: Currently handling a message
- **Queue Size**: Number of pending messages

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /chat` - Send a message to Bhrahma
- `GET /chat/{session_id}/messages` - Get conversation history
- `GET /queue/status` - Get queue status
- `GET /skills` - List all skills
- `GET /skills/{skill_name}` - Get specific skill
- `POST /skills/learn` - Learn a new skill
- `GET /llm/providers` - List available LLM providers

## Agent Skills Format

Skills follow the SKILL.md format from [agentskills.io](https://agentskills.io):

```markdown
---
name: skill-name
description: What the skill does and when to use it
category: general
tags: relevant, tags
---

# Skill Instructions

Clear, step-by-step instructions on how to use this skill.

## When to Use

- Specific trigger condition 1
- Specific trigger condition 2

## Examples

...
```

### Creating Custom Skills

1. Create a directory in `skills/`:

```bash
mkdir skills/my-custom-skill
```

2. Create `SKILL.md`:

```bash
touch skills/my-custom-skill/SKILL.md
```

3. Write your skill following the format above

4. Import the skill:

```bash
python backend/utils/import_skills.py --dir skills/my-custom-skill
```

## Configuration

### LLM Settings

Change the default LLM in `.env`:

```env
DEFAULT_LLM=anthropic  # or openai, mixtral
```

### Queue Settings

Adjust the maximum number of parallel agents in `.env`:

```env
MAX_PARALLEL_AGENTS=5
```

### Database Location

Change database path in `.env`:

```env
DATABASE_PATH=database/bhrahma.db
```

## Troubleshooting

### Database Issues

Reset the database:

```bash
rm database/bhrahma.db
python -c "from models.database import init_database; init_database()"
```

### API Key Errors

Verify your API keys are correctly set in `.env`:

```bash
cat .env | grep API_KEY
```

### Import Errors

If you get import errors, ensure you're running from the correct directory:

```bash
# For backend
cd backend
python main.py

# For frontend
cd frontend
streamlit run app.py
```

### Port Conflicts

Change ports if 8000 or 8501 are in use:

**Backend** (`backend/main.py`):
```python
uvicorn.run("main:app", host="0.0.0.0", port=8001)
```

**Frontend** (`frontend/app.py`):
```python
API_URL = "http://localhost:8001"  # Update to match backend
```

Then run Streamlit on a different port:
```bash
streamlit run app.py --server.port 8502
```

## Development

### Project Structure

- `backend/models/` - SQLAlchemy models and Pydantic schemas
- `backend/services/` - Core services (LLM clients, skills, search)
- `backend/agents/` - Agent implementations
- `backend/utils/` - Utility scripts
- `frontend/app.py` - Streamlit chat interface
- `skills/` - Agent skills directory

### Adding New LLM Providers

1. Create a new client class in `backend/services/llm_client.py`
2. Inherit from `LLMClient` abstract base class
3. Implement `generate()` and `generate_sync()` methods
4. Add to `LLMFactory.create_client()`

### Extending Skills

Skills can include bundled resources:

```
skill-name/
├── SKILL.md
├── scripts/
│   └── helper.py
├── references/
│   └── documentation.md
└── assets/
    └── template.txt
```

Resources are stored in the database and accessible to the agent.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [Anthropic](https://anthropic.com) for Claude and the Agent Skills format
- [agentskills.io](https://agentskills.io) for the skills specification
- OpenAI for GPT-4
- Together AI for Mixtral hosting

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/bhrahma/issues)
- Documentation: [agentskills.io](https://agentskills.io)

## Roadmap

- [ ] Add more default skills
- [ ] Implement skill versioning
- [ ] Add semantic search for skills
- [ ] Support for more LLM providers
- [ ] Multi-user support with authentication
- [ ] Skill marketplace
- [ ] Advanced agent orchestration
- [ ] Real-time collaboration
