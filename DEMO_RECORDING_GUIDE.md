# How to Record a Demo Video

## Quick Start (3 Steps)

### 1. Start the System
```bash
# Terminal 1 - Backend
cd /Users/priyanksharma/Desktop/Bhrahma/Bhrahma
source venv/bin/activate
cd backend
python main.py

# Terminal 2 - Frontend
cd /Users/priyanksharma/Desktop/Bhrahma/Bhrahma
source venv/bin/activate
cd frontend
streamlit run app.py
```

### 2. Open Recording Software

**Mac (Built-in):**
- Press `Cmd + Shift + 5`
- Select "Record Selected Portion" or "Record Entire Screen"
- Click "Options" → Check "Show Mouse Clicks"

**Windows (Built-in):**
- Press `Win + G` (Xbox Game Bar)
- Click "Capture" → Record

**Professional (Free):**
- Download OBS Studio: https://obsproject.com
- Create new scene with browser window
- Start recording

### 3. Follow the Demo Script

Open `DEMO_SCRIPT.md` and follow along!

---

## Option A: Manual Demo (Recommended)

**Best for:** Natural presentation, flexibility

1. **Prepare:**
   - Read through `DEMO_SCRIPT.md`
   - Practice the flow once without recording
   - Have the demo commands ready to copy-paste

2. **Record:**
   - Start recording
   - Follow the script
   - Type/paste commands from the script
   - Show responses and UI updates

3. **Edit:**
   - Speed up slow parts
   - Add voiceover/music
   - Add text overlays

**Time needed:** 30 min recording + 1 hour editing

---

## Option B: Automated Demo (Quick)

**Best for:** Quick testing, showcasing API

1. **Run the automation script:**
```bash
cd /Users/priyanksharma/Desktop/Bhrahma/Bhrahma
source venv/bin/activate
python demo_automation.py
```

2. **Record while it runs:**
   - Split screen: Terminal (left) + Browser (right)
   - Terminal shows: API interactions and logs
   - Browser shows: Frontend UI updating in real-time

3. **What you'll see:**
   - ✅ System health check
   - ✅ Skills list
   - ✅ Introduction message
   - ✅ Learning pytest skill
   - ✅ Using the learned skill
   - ✅ Parallel task execution
   - ✅ Skill reusability

**Time needed:** 10 min recording + 30 min editing

---

## Recording Setup Checklist

### Before Recording:

- [ ] Backend is running (check http://localhost:8000/health)
- [ ] Frontend is running (check http://localhost:8501)
- [ ] Browser is in incognito/private mode (clean session)
- [ ] Browser zoom is 100% or 110%
- [ ] Terminal font size is 14-16pt
- [ ] Hide personal info (bookmarks, emails, etc.)
- [ ] Close unnecessary applications
- [ ] Turn off notifications (Do Not Disturb mode)
- [ ] Check audio levels if recording voiceover

### Screen Layout Options:

**Option 1: Full Frontend**
```
┌─────────────────────────────┐
│                             │
│     Streamlit Frontend      │
│         (Fullscreen)        │
│                             │
└─────────────────────────────┘
```

**Option 2: Split Screen**
```
┌──────────────┬──────────────┐
│   Terminal   │   Browser    │
│   (Backend)  │  (Frontend)  │
│              │              │
└──────────────┴──────────────┘
```

**Option 3: Picture-in-Picture**
```
┌─────────────────────────────┐
│                             │
│       Main: Frontend        │
│                             │
│         ┌─────────┐         │
│         │Terminal │         │
│         └─────────┘         │
└─────────────────────────────┘
```

---

## Recording Software Settings

### OBS Studio (Recommended for Pro Quality)

**Scene Setup:**
1. Add Source → Display Capture (for full screen)
   OR
2. Add Source → Window Capture (for specific window)

**Settings:**
- Output → Recording Quality: "High Quality, Medium File Size"
- Video → Base Resolution: 1920x1080
- Video → Output Resolution: 1920x1080
- Video → FPS: 30 or 60

**Audio:**
- Desktop Audio: Enabled (for system sounds)
- Microphone: Enabled (for voiceover)
- Audio Bitrate: 192 kbps

### QuickTime (Mac - Simple)

1. Open QuickTime Player
2. File → New Screen Recording
3. Click options arrow:
   - Quality: Maximum
   - Show Mouse Clicks: Yes
   - Microphone: Built-in or external

---

## Demo Commands (Copy-Paste Ready)

```
Hello! What can you do?
```

```
Learn about pytest testing framework from https://docs.pytest.org
```

```
Create a pytest test for a function that calculates the factorial of a number
```

```
Compare Python, JavaScript, and Go for building REST APIs. Include performance, ease of use, and ecosystem.
```

```
Write comprehensive pytest tests for a Calculator class with add, subtract, multiply, and divide methods. Include edge cases.
```

---

## Post-Production Editing

### Free Tools:

**DaVinci Resolve** (Professional, Free)
- Download: https://www.blackmagicdesign.com/products/davinciresolve
- Best for: Color grading, advanced editing

**iMovie** (Mac Only, Free)
- Built-in on Mac
- Best for: Quick, simple edits

**Shotcut** (Windows/Mac/Linux, Free)
- Download: https://shotcut.org
- Best for: Cross-platform, simple UI

### Editing Checklist:

- [ ] Cut out mistakes/pauses
- [ ] Speed up slow parts (1.5x - 2x)
- [ ] Add intro title (3-5 seconds)
- [ ] Add section titles/transitions
- [ ] Add text overlays for key features
- [ ] Add background music (low volume, 10-20%)
- [ ] Add outro with links
- [ ] Export at 1080p, 30fps

### Suggested Music:

Free music from YouTube Audio Library:
- Category: "Ambient" or "Electronic"
- Mood: "Bright" or "Inspirational"
- Keep volume at 10-20% so voiceover is clear

---

## Example Timeline (5-7 min video)

```
00:00 - 00:10  Intro with logo/title
00:10 - 00:40  System overview & features
00:40 - 01:10  Basic interaction demo
01:10 - 03:00  Learning a skill (main feature)
03:00 - 04:30  Using learned skill
04:30 - 05:30  Parallel execution demo
05:30 - 06:30  Skill reusability
06:30 - 07:00  Outro with links
```

---

## Voiceover Script Template

**Intro (10 sec):**
> "Welcome to Bhrahma, an advanced AI agentic system that can learn new skills from the internet and solve complex tasks autonomously."

**Features (30 sec):**
> "Bhrahma features multi-LLM support, dynamic skill learning from documentation, parallel task execution with sub-agents, and persistent skill storage. Let's see it in action."

**Skill Learning (90 sec):**
> "Watch as Bhrahma learns about the pytest testing framework by crawling the official documentation. It extracts key information, generates a skill definition, and stores it for future use. Now Bhrahma can help us write pytest tests."

**Using Skill (60 sec):**
> "Let's ask Bhrahma to create a test. Notice how it automatically selects and uses the pytest skill it just learned. The generated tests follow pytest best practices."

**Parallel Execution (60 sec):**
> "For complex tasks, Bhrahma can spawn multiple sub-agents to work in parallel. Here it's comparing three programming languages, with each sub-agent analyzing one language simultaneously."

**Outro (30 sec):**
> "Bhrahma is open source and ready to deploy. Visit github.com/iamrajp/Bhrahma to get started. Thanks for watching!"

---

## Upload Checklist

### YouTube:
- [ ] Title: "Bhrahma AI Agent - Dynamic Skill Learning Demo"
- [ ] Description with links (GitHub, docs)
- [ ] Tags: AI, agent, LLM, automation, skills
- [ ] Thumbnail with logo and text
- [ ] Add to relevant playlists
- [ ] Enable comments
- [ ] Add chapter markers in description

### Social Media:
- [ ] Twitter: 30-60 sec clip with captions
- [ ] LinkedIn: Full video with professional description
- [ ] Reddit: r/MachineLearning, r/programming (check rules)

---

## Troubleshooting

**Browser lag during recording:**
- Close other tabs/apps
- Lower browser zoom to 90%
- Use hardware acceleration in browser settings

**Audio sync issues:**
- Record audio separately
- Sync in post-production using visual cues

**File too large:**
- Use H.264 codec for compression
- Export at lower bitrate (5-8 Mbps)
- Use HandBrake for re-compression

---

Ready to record? Start with the automated demo to test your setup, then do a manual recording following the script!

Good luck! 🎥🚀
