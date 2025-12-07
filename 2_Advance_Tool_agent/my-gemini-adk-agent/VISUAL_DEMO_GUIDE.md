# 📺 Visual Demo Guide - What to Show on Screen

## 🎬 Scene-by-Scene Breakdown

---

### **SCENE 1: Introduction (0:00 - 0:30)**

#### Screen Layout:
```
┌─────────────────────────────────────────┐
│  File Explorer                          │
│  my-gemini-adk-agent/                   │
│    ├── app/                             │
│    ├── tests/                           │
│    ├── deployment/                      │
│    ├── START_HERE.md                    │
│    ├── README.md                        │
│    ├── tool_agent.py                    │
│    └── ... (26 files total)            │
└─────────────────────────────────────────┘
```

#### What to Say:
"Hi! This is the Advanced Tool Agent - an AI system that generates and analyzes code using Google's Gemini CLI. It's a complete project with 26 files."

#### Actions:
1. Show folder in File Explorer
2. Scroll slowly through files
3. Highlight folder structure

---

### **SCENE 2: Project Structure (0:30 - 1:30)**

#### Screen Layout:
```
┌─────────────────────────────────────────┐
│  VS Code - START_HERE.md                │
│                                         │
│  # START HERE                           │
│                                         │
│  ## Quick Start (5 Minutes)            │
│                                         │
│  my-gemini-adk-agent/                   │
│  ├── app/              ← Core code      │
│  │   ├── agent.py                      │
│  │   ├── tools.py                      │
│  │   └── server.py                     │
│  ├── tests/            ← Test suite    │
│  ├── deployment/       ← Docker/Cloud  │
│  └── [docs]            ← 10 doc files  │
└─────────────────────────────────────────┘
```

#### What to Say:
"The project has a clean structure: app folder for core logic, tests folder for comprehensive testing, deployment folder for Docker and Cloud Run, plus 10 documentation files."

#### Actions:
1. Open `START_HERE.md` in VS Code
2. Scroll to project structure section
3. Point out key folders with mouse

---

### **SCENE 3: Core Code - Agent (1:30 - 2:00)**

#### Screen Layout:
```
┌─────────────────────────────────────────┐
│  VS Code - app/agent.py                 │
│                                         │
│  class AdvancedToolAgent:               │
│                                         │
│    def parse_intent(self, request):     │
│        """Parse user intent"""          │
│        # Detect action type             │
│        # Extract language               │
│        # Determine complexity           │
│                                         │
│    def process_request(self, request):  │
│        """Process end-to-end"""         │
│        # Parse intent                   │
│        # Select tool                    │
│        # Execute tool                   │
│        # Format response                │
└─────────────────────────────────────────┘
```

#### What to Say:
"Here's the core agent logic. It has four main steps: parse intent from natural language, select the right tool, execute it, and format the response."

#### Actions:
1. Open `app/agent.py`
2. Scroll to `parse_intent()` function (line ~30)
3. Scroll to `process_request()` function (line ~100)
4. Highlight key sections with mouse

---

### **SCENE 4: Core Code - Tools (2:00 - 2:30)**

#### Screen Layout:
```
┌─────────────────────────────────────────┐
│  VS Code - app/tools.py                 │
│                                         │
│  def generate_code_with_cli(            │
│      task: str,                         │
│      language: str = "python",          │
│      complexity: str = "medium"         │
│  ) -> Dict[str, Any]:                   │
│      """Generate code using Gemini"""   │
│                                         │
│  def analyze_code_with_cli(             │
│      code: str,                         │
│      analysis_type: str = "security"    │
│  ) -> Dict[str, Any]:                   │
│      """Analyze code using Gemini"""    │
└─────────────────────────────────────────┘
```

#### What to Say:
"These are the tool wrappers. One generates code, the other analyzes it. Both use the Gemini CLI through subprocess calls."

#### Actions:
1. Open `app/tools.py`
2. Show `generate_code_with_cli()` function
3. Show `analyze_code_with_cli()` function
4. Briefly show `GeminiCLIWrapper` class

---

### **SCENE 5: Live Demo (2:30 - 4:00)**

#### Screen Layout - Terminal:
```
┌─────────────────────────────────────────┐
│  Terminal                               │
│                                         │
│  PS> python simple_demo_auto.py         │
│                                         │
│  🤖 ADVANCED TOOL AGENT - SIMPLE DEMO   │
│                                         │
│  🎬 SCENARIO 1: Generate a REST API     │
│                                         │
│  👤 User Request:                       │
│     "Generate a Python REST API..."     │
│                                         │
│  🤖 Agent Processing...                 │
│     ✓ Action detected: generate         │
│     ✓ Language detected: python         │
│     ✓ Complexity: medium                │
│                                         │
│  📊 RESULT:                             │
│  ✅ Generated Python REST API...        │
│                                         │
│  [Shows generated code]                 │
└─────────────────────────────────────────┘
```

#### What to Say:
"Now let's see it in action. I'll run the demo that shows three scenarios: generating a REST API, analyzing code for security, and a combined workflow."

#### Actions:
1. Open terminal
2. Type: `python simple_demo_auto.py`
3. Let it run through all 3 scenarios
4. Don't interrupt - let viewers see the output
5. Highlight key parts:
   - Intent parsing results
   - Generated code
   - Security vulnerabilities found
   - Combined workflow

---

### **SCENE 6: Features Overview (4:00 - 4:45)**

#### Screen Layout:
```
┌─────────────────────────────────────────┐
│  VS Code - PROJECT_SUMMARY.md           │
│                                         │
│  ## Key Features                        │
│                                         │
│  ### Code Generation                    │
│  - Python (FastAPI, Flask)              │
│  - JavaScript (Express, Node.js)        │
│  - Go                                   │
│  - REST APIs, data pipelines, scripts   │
│                                         │
│  ### Code Analysis                      │
│  - Security vulnerabilities             │
│  - Performance issues                   │
│  - Style and best practices             │
│                                         │
│  ### Deployment                         │
│  - Local execution                      │
│  - Docker container                     │
│  - Google Cloud Run                     │
└─────────────────────────────────────────┘
```

#### What to Say:
"The agent supports Python, JavaScript, and Go. It can generate REST APIs, analyze security vulnerabilities, check performance, and deploy to Docker or Cloud Run."

#### Actions:
1. Open `PROJECT_SUMMARY.md`
2. Scroll to features section
3. Briefly show `deployment/Dockerfile`

---

### **SCENE 7: Conclusion (4:45 - 5:00)**

#### Screen Layout:
```
┌─────────────────────────────────────────┐
│  VS Code - QUICKSTART.md                │
│                                         │
│  # Quick Start Guide                    │
│                                         │
│  ## Step 1: Install Gemini CLI          │
│  npm install -g @google/...             │
│                                         │
│  ## Step 2: Install Dependencies        │
│  pip install -r requirements.txt        │
│                                         │
│  ## Step 3: Setup API Key               │
│  cp .env.example .env                   │
│                                         │
│  ## Step 4: Run the Agent               │
│  python tool_agent.py --interactive     │
│                                         │
│  That's it! You're ready to go! 🎉      │
└─────────────────────────────────────────┘
```

#### What to Say:
"Everything you need is included: complete documentation, tests, deployment configs, and example prompts. Check out the QUICKSTART guide to get started in 5 minutes. Thanks for watching!"

#### Actions:
1. Open `QUICKSTART.md`
2. Show the 4-step setup
3. End with folder view showing all files

---

## 🎨 Visual Tips

### **Color Coding (if possible):**
- 🟢 Green: Success messages, checkmarks
- 🔴 Red: Security vulnerabilities, errors
- 🔵 Blue: Information, file names
- 🟡 Yellow: Warnings, important notes

### **Mouse Highlighting:**
- Circle important text with mouse
- Underline key function names
- Point to specific lines of code

### **Zoom In:**
- Zoom in on important code sections
- Zoom out to show full structure
- Use Ctrl/Cmd + Mouse Wheel

### **Transitions:**
- Smooth scrolling (not too fast)
- Clear transitions between files
- Pause briefly when switching files

---

## 📸 Screenshot Moments

Take screenshots or pause at these moments:

1. **Project folder structure** (0:30)
2. **parse_intent() function** (1:45)
3. **Demo output - Generated API** (3:00)
4. **Demo output - Security analysis** (3:30)
5. **Features list** (4:15)

---

## 🎯 What NOT to Show

❌ Don't show:
- Your personal information
- API keys or credentials
- Unrelated browser tabs
- Desktop clutter
- Error messages (unless intentional)
- Long loading times (edit them out)

---

## 📱 Screen Recording Layout Options

### **Option 1: Split Screen**
```
┌──────────────┬──────────────┐
│              │              │
│   VS Code    │   Terminal   │
│   (Editor)   │   (Output)   │
│              │              │
└──────────────┴──────────────┘
```

### **Option 2: Full Screen (Switch)**
```
┌────────────────────────────┐
│                            │
│      VS Code               │
│      (Full Screen)         │
│                            │
└────────────────────────────┘
        ↓ Switch ↓
┌────────────────────────────┐
│                            │
│      Terminal              │
│      (Full Screen)         │
│                            │
└────────────────────────────┘
```

### **Option 3: Picture-in-Picture**
```
┌────────────────────────────┐
│                            │
│      VS Code               │
│      (Main)                │
│                            │
│              ┌──────────┐  │
│              │ Terminal │  │
│              │  (Small) │  │
│              └──────────┘  │
└────────────────────────────┘
```

**Recommended:** Option 2 (Full Screen Switch) for clarity

---

## ✅ Final Checklist

Before recording:
- [ ] Clear terminal history
- [ ] Close unnecessary apps
- [ ] Set terminal font to 14-16pt
- [ ] Test audio levels
- [ ] Disable notifications
- [ ] Have all files ready to open
- [ ] Practice once without recording

During recording:
- [ ] Speak clearly
- [ ] Don't rush
- [ ] Pause between sections
- [ ] Highlight important parts
- [ ] Show, don't just tell

After recording:
- [ ] Review for clarity
- [ ] Check audio quality
- [ ] Trim any mistakes
- [ ] Add title/end cards (optional)

---

## 🎬 You're Ready to Record!

Follow this guide and you'll have a professional 5-minute demo that clearly shows:
- What the project is
- How it's structured
- How it works
- What it can do
- How to get started

Good luck! 🎥✨
