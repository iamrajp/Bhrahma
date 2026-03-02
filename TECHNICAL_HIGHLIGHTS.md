# Bhrahma - Technical Highlights

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                      │
│              (Real-time Chat Interface)                     │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Message    │  │   Bhrahma    │  │    Skill        │  │
│  │    Queue     │→ │    Agent     │→ │   Manager       │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│         ↓                 ↓                    ↓            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Sub-Agent  │  │ Skill Creator│  │   Web Search    │  │
│  │  Orchestrator│  │    Agent     │  │    Service      │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Multi-LLM Gateway (Factory Pattern)            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Anthropic   │  │    OpenAI    │  │    Mixtral      │  │
│  │   Claude     │  │   GPT-4/3.5  │  │   (Mistral AI)  │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              SQLite Database (Persistence Layer)            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Skills     │  │   Messages   │  │  Agent Sessions │  │
│  │   Storage    │  │   History    │  │     Tracking    │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Core Technologies

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core language |
| **FastAPI** | 0.104+ | Async REST API framework |
| **SQLAlchemy** | 2.0+ | ORM for database operations |
| **Pydantic** | 2.5+ | Data validation and settings |
| **Anthropic SDK** | Latest | Claude API integration |
| **OpenAI SDK** | Latest | GPT models integration |
| **Uvicorn** | Latest | ASGI server |
| **BeautifulSoup4** | Latest | Web scraping |
| **Requests** | Latest | HTTP client |
| **Loguru** | Latest | Advanced logging |

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Streamlit** | 1.29+ | Interactive web UI |
| **Python Requests** | Latest | API communication |

### Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Containerization** | Docker | Multi-stage builds |
| **Deployment** | Railway, Render | Cloud platforms |
| **Database** | SQLite | Embedded relational DB |
| **Queue** | In-memory FIFO | Async task processing |

---

## 🎯 Key Technical Features

### 1. Multi-LLM Architecture with Factory Pattern

**Design Pattern:** Abstract Factory + Strategy Pattern

```python
# Abstract base class for LLM clients
class LLMClient(ABC):
    @abstractmethod
    async def generate(self, messages, system_prompt, **kwargs):
        pass

# Concrete implementations
class AnthropicClient(LLMClient):
    # Claude-specific implementation

class OpenAIClient(LLMClient):
    # OpenAI-specific implementation

class MixtralClient(LLMClient):
    # Mixtral-specific implementation

# Factory for runtime selection
class LLMFactory:
    @staticmethod
    def create_client(provider: str) -> LLMClient:
        # Returns appropriate client based on provider
```

**Benefits:**
- ✅ Swap LLM providers without code changes
- ✅ Easy to add new providers
- ✅ Centralized configuration
- ✅ Provider-agnostic codebase

**Technical Achievement:**
- Unified interface across 3 different LLM APIs
- Runtime provider selection via environment variables
- Graceful fallback handling

---

### 2. Dynamic Skill Learning System

**Innovation:** Agent Skills Format (Anthropic's specification)

**Architecture:**
```
User Request → Intent Detection → Documentation Crawling →
Skill Generation → Validation → Storage → Availability
```

**Technical Implementation:**

1. **Intent Detection (NLP-based):**
   ```python
   async def _needs_new_skill(self, message: str) -> (bool, dict):
       # Uses LLM to extract:
       # - Topic
       # - Description
       # - Documentation URLs (regex + LLM)
       # Returns: (needs_learning, skill_info)
   ```

2. **Documentation Crawling:**
   ```python
   async def _research_topic(self, topic: str, urls: list):
       # Multi-level crawling:
       # - Main documentation page (15,000 chars)
       # - Linked pages from same domain (5,000 chars each, up to 10)
       # - Web search results (fallback)
       # Returns: Consolidated documentation text
   ```

3. **Skill Generation (LLM-based):**
   ```python
   async def _generate_skill(self, topic, description, research_data):
       # Uses LLM with structured prompt
       # Generates SKILL.md format:
       # - YAML frontmatter (metadata)
       # - Markdown instructions
       # - Examples and best practices
   ```

4. **Storage (SQLAlchemy ORM):**
   ```python
   class Skill(Base):
       id: int (PK)
       name: str (unique, indexed)
       description: str (optimized for matching)
       content: text (full SKILL.md)
       category: str (indexed)
       tags: str (comma-separated)
       embedding: vector (future: semantic search)
   ```

**Technical Achievements:**
- ✅ Autonomous learning from web documentation
- ✅ Deep crawling of documentation sites (multi-page)
- ✅ Self-healing (automatically fixes malformed skills)
- ✅ Description optimization for better triggering
- ✅ Persistent storage with fast retrieval

---

### 3. Parallel Multi-Agent Orchestration

**Concurrency Pattern:** AsyncIO with Task Groups

**Architecture:**
```python
async def _execute_with_subagents(self, message, system_prompt, skills):
    # 1. Task Decomposition (LLM-based)
    subtasks = await self._decompose_task(message)

    # 2. Parallel Execution (AsyncIO gather)
    tasks = [
        self._execute_subagent(subtask, system_prompt, i)
        for i, subtask in enumerate(subtasks[:MAX_PARALLEL_AGENTS])
    ]
    results = await asyncio.gather(*tasks)

    # 3. Result Synthesis (LLM-based)
    final_response = await self._synthesize_results(message, results)
    return final_response
```

**Technical Features:**

1. **Automatic Task Decomposition:**
   - Heuristic detection (keywords: "multiple", "compare", "various")
   - LLM-based decomposition into 2-5 subtasks
   - Fallback to single execution if decomposition fails

2. **Concurrent Execution:**
   - AsyncIO gather for true parallelism
   - Per-agent database sessions
   - Independent error handling
   - Session tracking in database

3. **Result Aggregation:**
   - Structured result formatting
   - LLM-based synthesis
   - Context preservation

**Technical Achievements:**
- ✅ True async/await parallelism (not threading)
- ✅ Configurable parallelism limit (MAX_PARALLEL_AGENTS)
- ✅ Fault-tolerant (one agent failure doesn't crash others)
- ✅ Database transaction isolation per agent

---

### 4. Asynchronous Message Queue

**Pattern:** Producer-Consumer with Async Processing

**Implementation:**
```python
class MessageQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.is_processing = False
        self.current_task = None

    async def enqueue(self, message, session_id, metadata):
        task = QueueTask(
            task_id=str(uuid.uuid4()),
            message=message,
            session_id=session_id,
            metadata=metadata,
            timestamp=datetime.utcnow()
        )
        await self.queue.put(task)
        return task.task_id

    async def process_queue(self, processor_func):
        while True:
            task = await self.queue.get()
            self.is_processing = True
            self.current_task = task
            try:
                await processor_func(task)
            finally:
                self.is_processing = False
                self.current_task = None
                self.queue.task_done()
```

**Technical Features:**
- ✅ FIFO ordering guaranteed
- ✅ Non-blocking enqueue
- ✅ Status tracking (queue size, current task)
- ✅ Graceful error handling
- ✅ Auto-restart on failure

**Benefits:**
- User gets immediate response (task queued)
- Backend processes tasks sequentially
- No dropped messages
- Easy to monitor

---

### 5. Database Design

**ORM:** SQLAlchemy 2.0 (modern async-ready API)

**Schema:**

```sql
-- Skills table (optimized for search)
CREATE TABLE skills (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50),
    tags VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_category (category),
    FULLTEXT idx_description (description)
);

-- Chat messages (with metadata for analytics)
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    meta_data JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id)
);

-- Agent sessions (for tracking and debugging)
CREATE TABLE agent_sessions (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    agent_type VARCHAR(50),
    parent_session_id VARCHAR(100),
    status VARCHAR(20),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    skills_used TEXT,
    llm_provider VARCHAR(50),
    meta_data JSON
);
```

**Advanced Features:**
- JSON columns for flexible metadata
- Indexes on frequently queried fields
- Soft deletes (is_active flag)
- Timestamp tracking for all operations
- Parent-child relationships for sub-agents

---

### 6. Web Search & Scraping Service

**Multi-Provider Strategy:**

```python
class WebSearchService:
    def __init__(self):
        self.brave_search = BraveSearchAPI()
        self.google_search = GoogleSearchAPI()
        # Fallback chain: Brave → Google → DuckDuckGo

    async def search_and_scrape(self, query, num_results=3):
        # 1. Search
        search_results = await self._search(query)

        # 2. Scrape in parallel
        scrape_tasks = [
            self.scrape_page(url)
            for url in search_results[:num_results]
        ]
        pages = await asyncio.gather(*scrape_tasks)

        # 3. Extract and clean
        return self.extract_documentation(pages)
```

**Features:**
- ✅ Multi-provider fallback
- ✅ Parallel scraping (AsyncIO)
- ✅ HTML parsing with BeautifulSoup4
- ✅ Text extraction and cleaning
- ✅ Link discovery and crawling
- ✅ Rate limiting and retry logic

**Technical Achievement:**
- Deep documentation crawling (main page + linked pages)
- Intelligent text extraction (removes nav, footer, ads)
- Domain-restricted crawling for security

---

### 7. Configuration Management

**Pattern:** Pydantic Settings with Environment Variables

```python
class Settings(BaseSettings):
    # LLM Configuration
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str
    MIXTRAL_API_KEY: str
    DEFAULT_LLM: str = "anthropic"

    # Database
    DATABASE_PATH: str = "database/bhrahma.db"

    # Search
    BRAVE_SEARCH_API_KEY: Optional[str] = None
    GOOGLE_SEARCH_API_KEY: Optional[str] = None

    # Agent Settings
    MAX_PARALLEL_AGENTS: int = 5
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
```

**Benefits:**
- ✅ Type validation at startup
- ✅ Environment variable overrides
- ✅ Default values
- ✅ IDE autocomplete
- ✅ Documentation via type hints

---

## 🚀 Performance Optimizations

### 1. Async/Await Throughout
- All I/O operations are async
- No blocking calls in request handlers
- Concurrent execution where possible

### 2. Database Optimizations
- Indexed columns for fast lookups
- Connection pooling (SQLAlchemy)
- Lazy loading of relationships
- Batched inserts where applicable

### 3. Caching Strategy
- LLM responses cached in database
- Skills cached in memory after first load
- Web search results deduplicated

### 4. Resource Management
- Configurable parallel agent limit
- Request timeouts
- Graceful degradation on errors
- Memory-efficient streaming

---

## 🔒 Security Features

### 1. Input Validation
- Pydantic models for all API inputs
- SQL injection prevention (ORM)
- XSS protection (Streamlit auto-escapes)

### 2. API Key Management
- Environment variables (never committed)
- Separate keys per provider
- Easy rotation

### 3. Rate Limiting Ready
- Queue-based processing (natural rate limit)
- Easy to add middleware for API rate limiting

### 4. CORS Configuration
- Configurable origins
- Credentials handling
- Preflight requests supported

---

## 🧪 Testing & Quality

### Code Quality Tools
- **Type Hints:** Full typing coverage
- **Docstrings:** Google-style docstrings
- **Logging:** Structured logging with Loguru
- **Error Handling:** Try-except at all I/O boundaries

### Testing Strategy
```
backend/
├── tests/
│   ├── test_agents.py          # Agent logic tests
│   ├── test_skills.py          # Skill management tests
│   ├── test_llm_clients.py     # LLM integration tests
│   ├── test_web_search.py      # Web scraping tests
│   └── test_api.py             # API endpoint tests
```

---

## 📊 Observability

### Logging
```python
# Structured logging with context
logger.info(
    f"Bhrahma processing message in session {self.session_id}",
    extra={"session_id": self.session_id, "llm": self.llm_provider}
)
```

### Monitoring Points
- Queue status endpoint (`/queue/status`)
- Health check endpoint (`/health`)
- Database session tracking
- Per-agent performance metrics

---

## 🐳 Docker & Deployment

### Multi-Stage Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Dependency layer (cached)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application layer
COPY backend/ ./backend/
COPY skills/ ./skills/

# Startup script (handles PORT properly)
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
```

**Optimizations:**
- ✅ Layer caching for faster builds
- ✅ Minimal base image (slim)
- ✅ No cache for pip (smaller image)
- ✅ Proper signal handling (exec in start.sh)

---

## 📈 Scalability Considerations

### Current Architecture (Single Instance)
- ✅ Async processing (high concurrency)
- ✅ Queue-based (handles bursts)
- ✅ SQLite (fast for read-heavy workloads)

### Future Scaling Path
1. **Database:** SQLite → PostgreSQL (for multi-instance)
2. **Queue:** In-memory → Redis/RabbitMQ
3. **Caching:** Add Redis for LLM response cache
4. **Load Balancing:** Multiple backend instances
5. **Storage:** Local → S3 for skills/assets

---

## 🎓 Design Patterns Used

| Pattern | Where | Why |
|---------|-------|-----|
| **Factory** | LLM clients | Runtime provider selection |
| **Strategy** | LLM execution | Swap algorithms |
| **Template Method** | Skill creation | Consistent workflow |
| **Observer** | Queue status | Real-time updates |
| **Repository** | Database access | Abstraction layer |
| **Singleton** | Queue, Config | Single instance |
| **Facade** | API endpoints | Simplified interface |
| **Builder** | Skill generation | Complex object creation |

---

## 🏆 Technical Achievements Summary

1. **✅ Multi-LLM Support** - Unified interface for 3 providers
2. **✅ Dynamic Skill Learning** - First-of-its-kind autonomous skill acquisition
3. **✅ Parallel Execution** - True async multi-agent orchestration
4. **✅ Web Intelligence** - Deep documentation crawling and extraction
5. **✅ Production Ready** - Docker, Railway, proper error handling
6. **✅ Scalable Architecture** - Async, queued, modular design
7. **✅ Developer Friendly** - Type hints, docs, clear structure
8. **✅ Observable** - Logging, monitoring, session tracking

---

## 📚 Code Statistics

```
Backend:
  - Python Files: 15
  - Lines of Code: ~2,500
  - Functions/Methods: 80+
  - Classes: 20+

Frontend:
  - Python Files: 1
  - Lines of Code: ~300

Configuration:
  - Dockerfiles: 2
  - Scripts: 2
  - Documentation: 8 files

Total Project:
  - Files: 30+
  - Lines: ~4,200
  - Dependencies: 20+
```

---

## 🔬 Innovation Highlights

### 1. Self-Improving Agent
Unlike traditional chatbots, Bhrahma can:
- Learn new capabilities from documentation
- Store learned skills permanently
- Apply learned skills to future tasks
- Optimize skill descriptions for better triggering

### 2. Agent Skills Format Integration
One of the first implementations of Anthropic's Agent Skills specification:
- SKILL.md format with YAML frontmatter
- Structured instructions for LLMs
- Reusable, shareable skill definitions

### 3. Intelligent Web Research
- Multi-page documentation crawling
- Same-domain link following
- Content extraction and cleaning
- Structured knowledge aggregation

---

## 🎯 Use Cases

**Demonstrated:**
1. Learning pytest from docs and generating tests
2. Comparing programming languages in parallel
3. Creating specialized testing frameworks
4. Building domain-specific knowledge bases

**Potential:**
1. Customer support automation (learn from help docs)
2. Code generation (learn framework-specific patterns)
3. Research assistance (learn from papers/docs)
4. DevOps automation (learn from runbooks)

---

**Built with:** Python, FastAPI, Anthropic Claude, OpenAI GPT, Streamlit, SQLAlchemy, Docker

**Repository:** https://github.com/iamrajp/Bhrahma

**License:** MIT (Open Source)
