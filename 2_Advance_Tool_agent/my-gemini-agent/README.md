# Gemini CLI Agent - Production-Ready AI Code Assistant

## 🎯 What This Project Is

A production-ready AI agent that integrates Google's Gemini CLI with Python to provide intelligent code generation and analysis capabilities. The agent automatically decides when to generate code, analyze existing code, or perform both operations based on natural language requests.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│              (CLI / FastAPI Server / Tests)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Agent Core (agent.py)                   │
│  • Intent Recognition                                        │
│  • Tool Selection Logic                                      │
│  • Response Formatting                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Tool System (tools.py)                     │
│  • GeminiCLIWrapper                                          │
│  • generate_code_with_cli()                                  │
│  • analyze_code_with_cli()                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Gemini CLI (subprocess)                   │
│  • Executes: gemini -p "prompt"                              │
│  • Returns: AI-generated responses                           │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 How Gemini CLI Is Used

The agent uses Google's Gemini CLI as its core AI engine through subprocess execution:

1. **Code Generation**: `gemini -p "Generate <complexity> <language> code for: <task>"`
2. **Code Analysis**: `gemini -p "Analyze this code for <analysis_type>: <snippet>"`

Each CLI call is:
- Wrapped with timeout protection (40 seconds)
- Logged for debugging
- Error-handled with fallback responses
- Validated for API key presence

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+ (for Gemini CLI)
- Google Cloud account with Gemini API access
- Gemini API key

## 🚀 Setup Instructions

### 1. Install Gemini CLI

```bash
# Install globally via npm
npm install -g @google/generative-ai-cli

# Verify installation
gemini --version
```

### 2. Clone and Setup Project

```bash
cd my-gemini-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

## 💻 Running Locally

### Interactive Mode

```bash
python app/agent.py --interactive
```

Example session:
```
> Generate a Python REST API with JWT authentication
[Agent generates complete Flask/FastAPI code with JWT]

> Analyze this: def login(u): exec(u)
[Agent detects security vulnerability and provides report]

> Generate an email validator, then analyze it
[Agent generates code AND analyzes it automatically]
```

### Single Request Mode

```bash
python app/agent.py --request "Generate a data processing pipeline in Python"
```

### Server Mode (FastAPI)

```bash
python app/server.py
```

Then access:
- API: http://localhost:8080
- Docs: http://localhost:8080/docs
- Health: http://localhost:8080/health

Example API call:
```bash
curl -X POST http://localhost:8080/agent \
  -H "Content-Type: application/json" \
  -d '{"message": "Generate a Python REST API"}'
```

## 🧪 Running Tests

### Quick Test (Validates Everything)

```bash
python tests/quick_test.py
```

### Full Test Suite

```bash
pytest tests/ -v
```

## ☁️ Deploying to Cloud Run

### Prerequisites

1. Install Google Cloud SDK
2. Authenticate: `gcloud auth login`
3. Set project: `gcloud config set project YOUR_PROJECT_ID`

### Deploy Steps

```bash
# Build and deploy using Cloud Build
gcloud builds submit --config deployment/cloudbuild.yaml

# Or deploy directly with Docker
docker build -t gcr.io/YOUR_PROJECT_ID/gemini-agent -f deployment/Dockerfile .
docker push gcr.io/YOUR_PROJECT_ID/gemini-agent
gcloud run deploy gemini-agent \
  --image gcr.io/YOUR_PROJECT_ID/gemini-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key_here
```

### Verify Deployment

```bash
# Get service URL
gcloud run services describe gemini-agent --region us-central1 --format 'value(status.url)'

# Test endpoint
curl https://your-service-url.run.app/health
```

## 📝 Example Usage Prompts

### Code Generation Examples

```
"Generate a Python REST API with JWT authentication"
"Create a TypeScript React component for user login"
"Build a data processing pipeline with error handling"
"Generate a Flask API with SQLAlchemy models"
"Create a FastAPI service with async endpoints"
```

### Code Analysis Examples

```
"Analyze this code for security issues: def login(u): exec(u)"
"Check this function for performance problems: [paste code]"
"Review this API endpoint for vulnerabilities"
"Analyze naming conventions in this module"
```

### Combined Operations

```
"Generate an email validator, then analyze it for edge cases"
"Create a password hasher and check its security"
"Build a file uploader and analyze for vulnerabilities"
```

## 🔍 How It Works

### 1. Intent Recognition

The agent analyzes your message to determine intent:
- **Generate**: Keywords like "generate", "create", "build", "write"
- **Analyze**: Keywords like "analyze", "check", "review", "security"
- **Combined**: Both patterns detected

### 2. Tool Selection

Based on intent, the agent selects appropriate tools:
- `generate_code_with_cli()` for code generation
- `analyze_code_with_cli()` for code analysis
- Both tools for combined operations

### 3. Gemini CLI Execution

Tools execute Gemini CLI commands:
```python
subprocess.run(
    ["gemini", "-p", prompt],
    capture_output=True,
    text=True,
    timeout=40
)
```

### 4. Response Processing

The agent:
- Parses CLI output
- Formats as structured JSON
- Adds metadata (execution time, tool used)
- Returns clean, readable response

## 🛠️ Troubleshooting

### Issue: "gemini: command not found"

**Solution**: Install Gemini CLI globally
```bash
npm install -g @google/generative-ai-cli
```

### Issue: "API key not found"

**Solution**: Set GEMINI_API_KEY in .env file
```bash
echo GEMINI_API_KEY=your_key_here > .env
```

### Issue: "Timeout error"

**Solution**: Increase timeout in tools.py
```python
timeout=60  # Increase from 40 to 60 seconds
```

### Issue: "Module not found"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Docker build fails

**Solution**: Ensure Node.js is installed in Dockerfile
```dockerfile
RUN apt-get update && apt-get install -y nodejs npm
```

## 📊 Project Structure

```
my-gemini-agent/
├── app/
│   ├── agent.py          # Core agent logic and orchestration
│   ├── tools.py          # Gemini CLI wrapper and tool implementations
│   ├── server.py         # FastAPI server for HTTP access
│   └── utils/
│       └── helpers.py    # Utility functions and helpers
├── tests/
│   ├── quick_test.py     # Quick validation tests
│   └── test_agent.py     # Comprehensive test suite
├── deployment/
│   ├── Dockerfile        # Container definition
│   └── cloudbuild.yaml   # Cloud Build configuration
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── test_prompts.md       # Example prompts for testing
├── pyproject.toml        # Project metadata
└── .env.example          # Environment template
```

## 🔐 Security Considerations

- Never commit .env file with real API keys
- Use environment variables for sensitive data
- Validate all user inputs before CLI execution
- Implement rate limiting in production
- Use HTTPS for all API communications
- Regularly update dependencies

## 📈 Performance Tips

- Use async operations for concurrent requests
- Cache frequent CLI responses
- Implement request queuing for high load
- Monitor Cloud Run metrics
- Set appropriate timeout values
- Use connection pooling

## 🤝 Contributing

This is a production-ready template. Customize as needed:
- Add more tools in tools.py
- Extend agent logic in agent.py
- Add authentication to server.py
- Implement caching layer
- Add monitoring and logging

## 📄 License

MIT License - Feel free to use in your projects

## 🆘 Support

For issues or questions:
1. Check troubleshooting section above
2. Review test files for examples
3. Check Gemini CLI documentation
4. Review Cloud Run documentation

---

**Built with ❤️ using Google Gemini CLI and Python**
