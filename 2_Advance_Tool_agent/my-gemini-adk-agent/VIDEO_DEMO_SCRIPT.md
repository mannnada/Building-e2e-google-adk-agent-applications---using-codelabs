# 🎥 5-Minute Video Demo Script

## 📋 Pre-Recording Checklist

- [ ] Open VS Code or your preferred editor
- [ ] Have terminal ready
- [ ] Clear terminal history
- [ ] Close unnecessary applications
- [ ] Test screen recording software
- [ ] Prepare browser with documentation open

---

## 🎬 Video Timeline (5 Minutes)

### **[0:00 - 0:30] Introduction (30 seconds)**

**What to show:**
- Project folder in file explorer
- Quick overview of folder structure

**What to say:**
```
"Hi! Today I'm showing you the Advanced Tool Agent - an AI-powered system 
that generates and analyzes code using Google's Gemini CLI. This is a 
complete, production-ready project with 26 files, comprehensive documentation, 
and deployment configurations."
```

**Actions:**
1. Show `my-gemini-adk-agent` folder
2. Briefly scroll through files

---

### **[0:30 - 1:30] Project Structure (1 minute)**

**What to show:**
- Open `START_HERE.md` in editor
- Scroll through to show structure

**What to say:**
```
"The project has a clean structure:
- app/ folder contains the core agent logic
- tests/ folder has comprehensive test suites
- deployment/ folder has Docker and Cloud Run configs
- Plus 10 documentation files covering everything"
```

**Actions:**
1. Open `START_HERE.md`
2. Show the folder structure diagram
3. Briefly mention key files

**Key Files to Highlight:**
- `app/agent.py` - "Main agent with intent parsing"
- `app/tools.py` - "Gemini CLI wrappers"
- `app/server.py` - "FastAPI REST API"
- `tests/quick_test.py` - "Integration tests"

---

### **[1:30 - 2:30] Code Walkthrough (1 minute)**

**What to show:**
- Open `app/agent.py`
- Scroll through key functions

**What to say:**
```
"Let me show you the core agent logic. The agent has four main components:
1. Intent Parser - understands natural language requests
2. Tool Selector - chooses the right tool
3. Tool Executor - runs the selected tool
4. Response Formatter - creates user-friendly output"
```

**Actions:**
1. Open `app/agent.py`
2. Show `parse_intent()` function (line ~30)
3. Show `process_request()` function (line ~100)
4. Briefly show `app/tools.py`
5. Point out `generate_code_with_cli()` and `analyze_code_with_cli()`

---

### **[2:30 - 4:00] Live Demo (1.5 minutes)**

**What to show:**
- Run the automated demo
- Show real output

**What to say:**
```
"Now let's see it in action. I'll run the demo that shows three scenarios:
generating code, analyzing code, and a combined workflow."
```

**Actions:**
1. Open terminal in project folder
2. Run: `python simple_demo_auto.py`
3. Let it run through all 3 scenarios
4. Highlight key outputs:
   - Intent parsing results
   - Generated REST API code
   - Security vulnerability detection
   - Combined workflow

**Terminal Commands:**
```bash
cd my-gemini-adk-agent
python simple_demo_auto.py
```

---

### **[4:00 - 4:45] Features & Capabilities (45 seconds)**

**What to show:**
- Open `README.md` or `PROJECT_SUMMARY.md`
- Scroll through features section

**What to say:**
```
"This agent can:
- Generate code in Python, JavaScript, and Go
- Create REST APIs with FastAPI or Express
- Analyze code for security vulnerabilities, performance issues, and style
- Run locally, in Docker, or deploy to Google Cloud Run
- It has multiple interfaces: CLI, interactive mode, and REST API"
```

**Actions:**
1. Open `PROJECT_SUMMARY.md`
2. Show features section
3. Briefly show `deployment/Dockerfile`

---

### **[4:45 - 5:00] Conclusion (15 seconds)**

**What to show:**
- Show `QUICKSTART.md` or `README.md`

**What to say:**
```
"Everything you need is included: complete documentation, tests, 
deployment configs, and example prompts. Check out the README 
to get started. Thanks for watching!"
```

**Actions:**
1. Show `QUICKSTART.md`
2. End with project folder view

---

## 📁 Important Files to Show (Priority Order)

### **MUST SHOW (Core Files)**

1. **START_HERE.md**
   - Description: "Quick overview and 5-minute setup guide"
   - Why: Entry point for new users
   - Show: 10 seconds

2. **app/agent.py** (200+ lines)
   - Description: "Main agent with intent parsing and orchestration"
   - Why: Core logic of the system
   - Show: 20 seconds
   - Highlight: `parse_intent()`, `process_request()` functions

3. **app/tools.py** (150+ lines)
   - Description: "Gemini CLI wrappers for code generation and analysis"
   - Why: Shows how it integrates with Gemini
   - Show: 15 seconds
   - Highlight: `generate_code_with_cli()`, `analyze_code_with_cli()`

4. **simple_demo_auto.py**
   - Description: "Automated demo showing all capabilities"
   - Why: Visual proof it works
   - Show: 90 seconds (running)

### **SHOULD SHOW (Supporting Files)**

5. **README.md**
   - Description: "Complete documentation with setup, usage, and deployment"
   - Why: Main reference document
   - Show: 10 seconds

6. **PROJECT_SUMMARY.md**
   - Description: "Project overview with features and architecture"
   - Why: Quick understanding of capabilities
   - Show: 10 seconds

7. **deployment/Dockerfile**
   - Description: "Multi-stage Docker build for containerization"
   - Why: Shows production-ready deployment
   - Show: 5 seconds

8. **tests/quick_test.py**
   - Description: "Integration test suite with 3 comprehensive tests"
   - Why: Shows quality and testing
   - Show: 5 seconds

### **NICE TO SHOW (If Time Permits)**

9. **app/server.py**
   - Description: "FastAPI REST API server with endpoints"
   - Why: Shows API interface

10. **test_prompts.md**
    - Description: "Example prompts and use cases"
    - Why: Helps users understand what to try

11. **ARCHITECTURE.md**
    - Description: "System architecture with diagrams"
    - Why: Technical depth

---

## 🎯 Key Points to Emphasize

### **1. Completeness**
- "26 files, fully documented, production-ready"
- "Everything included: code, tests, docs, deployment"

### **2. Intelligence**
- "Understands natural language requests"
- "Automatically selects the right tool"
- "Detects language, complexity, and analysis type"

### **3. Capabilities**
- "Generates REST APIs, data pipelines, scripts"
- "Analyzes security, performance, style"
- "Combined workflows: generate then analyze"

### **4. Deployment**
- "Run locally, Docker, or Cloud Run"
- "Complete CI/CD with Cloud Build"

### **5. Quality**
- "Comprehensive test suite"
- "No syntax errors"
- "Production-ready code"

---

## 🎬 Recording Tips

### **Before Recording:**
1. Close all unnecessary applications
2. Clear terminal history: `cls` or `clear`
3. Set terminal font size to 14-16pt for readability
4. Use a clean VS Code theme (Dark+ or Light+)
5. Disable notifications
6. Test audio levels

### **During Recording:**
1. Speak clearly and at moderate pace
2. Pause briefly between sections
3. Use mouse to highlight important parts
4. Don't rush through code - let viewers see it
5. If you make a mistake, pause and continue

### **Screen Layout:**
- **Left side:** Editor (VS Code)
- **Right side:** Terminal
- Or use full screen and switch between them

### **Terminal Settings:**
- Font: Consolas or Fira Code
- Size: 14-16pt
- Theme: High contrast
- Clear before each command

---

## 📝 Quick Reference Script

### **Opening (10 seconds)**
"Hi! This is the Advanced Tool Agent - an AI system that generates and analyzes code using Gemini CLI."

### **Structure (20 seconds)**
"It has 26 files organized in app, tests, and deployment folders, plus comprehensive documentation."

### **Code (30 seconds)**
"The agent parses natural language, selects tools, executes them, and formats results. Here's the core logic..."

### **Demo (90 seconds)**
"Let's see it in action. Watch how it generates a REST API, analyzes code for security, and runs combined workflows."

### **Features (30 seconds)**
"It supports Python, JavaScript, Go. Generates APIs, analyzes security, performance, style. Deploys to Docker and Cloud Run."

### **Closing (10 seconds)**
"Everything's included and documented. Check the README to get started. Thanks!"

---

## 🎥 Alternative: Quick 2-Minute Version

If you need a shorter version:

1. **[0:00-0:15]** Introduction + folder structure
2. **[0:15-0:45]** Show `app/agent.py` briefly
3. **[0:45-1:45]** Run `python simple_demo_auto.py`
4. **[1:45-2:00]** Conclusion

---

## 📊 File Descriptions (Copy-Paste Ready)

Use these when showing files:

| File | One-Line Description |
|------|---------------------|
| `START_HERE.md` | Quick overview and 5-minute setup guide |
| `README.md` | Complete documentation with setup and deployment |
| `app/agent.py` | Main agent with intent parsing and orchestration |
| `app/tools.py` | Gemini CLI wrappers for generation and analysis |
| `app/server.py` | FastAPI REST API server with endpoints |
| `tests/quick_test.py` | Integration test suite with 3 tests |
| `tests/test_agent.py` | Comprehensive unit tests |
| `deployment/Dockerfile` | Multi-stage Docker build configuration |
| `deployment/cloudbuild.yaml` | Google Cloud Build CI/CD pipeline |
| `tool_agent.py` | Main CLI entry point for interactive mode |
| `simple_demo_auto.py` | Automated demo showing all capabilities |
| `PROJECT_SUMMARY.md` | Project overview with features and stats |
| `ARCHITECTURE.md` | System architecture with detailed diagrams |
| `test_prompts.md` | Example prompts and use cases |
| `QUICKSTART.md` | 5-minute setup guide |

---

## ✅ Post-Recording Checklist

- [ ] Video is 5 minutes or less
- [ ] Audio is clear
- [ ] All key files shown
- [ ] Demo ran successfully
- [ ] No sensitive information visible
- [ ] Good pacing (not too fast/slow)
- [ ] Clear conclusion

---

## 🎬 Ready to Record!

**Recommended Recording Software:**
- **Windows:** OBS Studio, Camtasia, or Windows Game Bar
- **Mac:** QuickTime, ScreenFlow, or OBS Studio
- **Linux:** OBS Studio, SimpleScreenRecorder

**Resolution:** 1920x1080 (1080p)
**Frame Rate:** 30 FPS
**Audio:** Clear microphone, no background noise

Good luck with your recording! 🎥✨
