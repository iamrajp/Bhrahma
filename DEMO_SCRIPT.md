# Bhrahma Demo Script

## Demo Video Guide (5-7 minutes)

### Pre-Demo Setup
1. Have both backend and frontend running (locally or Railway)
2. Clear browser cache/use incognito mode for fresh session
3. Have these URLs ready in browser tabs:
   - Documentation: https://docs.pytest.org
   - Frontend: http://localhost:8501 or Railway URL

---

## Scene 1: Introduction (30 seconds)

**Voiceover:**
> "Welcome to Bhrahma - an advanced AI agentic system that can learn new skills from the internet and use them to solve complex tasks."

**Show:**
- Landing page with Bhrahma logo
- Overview of the architecture diagram

---

## Scene 2: System Overview (1 minute)

**Voiceover:**
> "Bhrahma features:
> - Multi-LLM support (Anthropic Claude, OpenAI, Mixtral)
> - Dynamic skill learning from documentation
> - Parallel task execution with sub-agents
> - Persistent skill storage and reuse"

**Show:**
- Backend running logs showing:
  ```
  INFO: Bhrahma system initialized
  INFO: Database initialized
  INFO: Message queue processor started
  ```
- Frontend interface showing:
  - Session ID
  - Queue status
  - Skills panel (showing "skill-creator")

---

## Scene 3: Basic Interaction (1 minute)

**Action:**
Type in chat: "Hello, what can you do?"

**Expected Response:**
> "I'm Bhrahma, an advanced AI agent. I can:
> 1. Use specialized skills to solve problems
> 2. Learn new skills from the internet when needed
> 3. Coordinate multiple sub-agents for parallel execution
> 4. Adapt to different types of tasks"

**Show:**
- Message appearing in chat
- Queue status updating
- Response streaming in

---

## Scene 4: Learning a New Skill (2-3 minutes)

### 4A: Skill Learning Request

**Action:**
Type: "Learn about pytest from https://docs.pytest.org"

**Show:**
- Backend logs:
  ```
  INFO: Detected skill learning request: {'topic': 'pytest', ...}
  INFO: Triggering skill-creator to learn: pytest testing
  INFO: Crawling documentation: https://docs.pytest.org
  INFO: Successfully learned skill: pytest-testing
  ```

**Expected Response:**
> "✅ I've learned a new skill: **pytest-testing**
>
> This skill helps with writing and running Python tests using pytest framework.
>
> Now I can help you with tasks related to this skill. What would you like me to do?"

**Show:**
- Skills sidebar updating with new "pytest-testing" skill
- Skill description and category

### 4B: Using the Learned Skill

**Action:**
Type: "Create a test for a function that adds two numbers"

**Expected Response:**
Shows pytest test code:
```python
import pytest

def add(a, b):
    return a + b

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(5, 0) == 5
```

**Show:**
- Skills used indicator showing "pytest-testing"
- Backend logs showing skill selection

---

## Scene 5: Multi-Agent Execution (1-2 minutes)

**Action:**
Type: "Compare Python, JavaScript, and Go for building web APIs"

**Show:**
- Backend logs:
  ```
  INFO: Task requires parallel execution
  INFO: Decomposed into 3 subtasks
  INFO: Sub-agent 0 processing: Analyze Python for web APIs
  INFO: Sub-agent 1 processing: Analyze JavaScript for web APIs
  INFO: Sub-agent 2 processing: Analyze Go for web APIs
  ```

**Expected Response:**
Comprehensive comparison with sections for each language

**Show:**
- Multiple sub-agent sessions in database
- Results being synthesized

---

## Scene 6: Skill Reusability (1 minute)

**Action:**
1. Start new session (click "New Session")
2. Type: "Write a pytest test for a calculator class"

**Show:**
- Skills panel showing "pytest-testing" still available
- Bhrahma using the previously learned skill
- Skills used: "pytest-testing"

**Voiceover:**
> "Notice how the skill we learned earlier is now permanently available and can be reused across sessions."

---

## Scene 7: Technical Deep Dive (30 seconds)

**Show (split screen):**

**Left side - Frontend:**
- Streamlit interface
- Real-time updates
- Skills panel

**Right side - Backend:**
- Terminal with logs
- Database file
- Skills directory structure

**Voiceover:**
> "Under the hood, Bhrahma uses:
> - FastAPI for the backend API
> - Streamlit for the frontend
> - SQLite for persistence
> - Message queue for async processing
> - Agent Skills format for skill storage"

---

## Scene 8: Deployment (30 seconds)

**Show:**
- Railway dashboard
- Deployed services (backend + frontend)
- Public URLs
- Environment variables

**Voiceover:**
> "Bhrahma can be deployed to Railway, Render, or any Docker-compatible platform with a single click."

---

## Scene 9: Conclusion (30 seconds)

**Show:**
- GitHub repository: https://github.com/iamrajp/Bhrahma
- README with installation instructions
- Documentation links

**Voiceover:**
> "Bhrahma is open source and ready to deploy. Get started at github.com/iamrajp/Bhrahma
>
> Thank you for watching!"

---

## Recording Tips

### Software Recommendations:
- **Screen Recording:** OBS Studio (free), Loom, or QuickTime
- **Video Editing:** DaVinci Resolve (free), iMovie, or Camtasia
- **Audio:** Use a good microphone or record voiceover separately

### Recording Setup:
1. **Resolution:** 1920x1080 (1080p)
2. **Frame Rate:** 30fps or 60fps
3. **Browser Zoom:** 100% or 110% for better visibility
4. **Terminal Font Size:** Increase to 14-16pt
5. **Hide:** Bookmarks bar, personal info

### Post-Production:
1. Add intro/outro graphics
2. Add text overlays for key points
3. Speed up slow parts (e.g., waiting for responses)
4. Add background music (low volume)
5. Add captions/subtitles

---

## Quick Demo Commands

Copy-paste these into chat during recording:

```
1. Hello, what can you do?

2. Learn about pytest from https://docs.pytest.org

3. Create a test for a function that calculates the factorial of a number

4. Compare Python, JavaScript, and Go for building web APIs

5. Write a pytest test for a calculator class with add, subtract, multiply, and divide methods
```

---

## Troubleshooting During Recording

**If response is slow:**
- Pause recording, wait for response, resume
- Speed up in post-production

**If error occurs:**
- Stop recording
- Fix issue
- Start fresh scene

**If UI looks cluttered:**
- Use browser zoom
- Collapse browser DevTools
- Use "New Session" to reset chat

---

## Export Settings

**For YouTube:**
- Format: MP4 (H.264)
- Resolution: 1920x1080
- Bitrate: 8-10 Mbps
- Audio: AAC, 192 kbps

**For Social Media:**
- Also export 1080x1080 (square) for Instagram
- 1920x1080 for Twitter/LinkedIn
- Add subtitles for silent viewing

---

Good luck with your demo video! 🎥
