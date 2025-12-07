# Advanced Tool Agent

An AI-powered agent that generates and analyzes code using Google's Gemini CLI. This agent can create REST APIs, data pipelines, scripts, and perform comprehensive code analysis for security, performance, and style issues.

## Features

- **Code Generation**: Generate production-ready code in Python, JavaScript, and Go
- **Code Analysis**: Analyze code for security vulnerabilities, performance issues, and style problems
- **Combined Workflows**: Generate code and automatically analyze it
- **Multiple Interfaces**: CLI, interactive mode, and REST API
- **Cloud Ready**: Deploy to Cloud Run with Docker support
- **Real Gemini CLI Integration**: Uses actual Gemini CLI commands in non-interactive mode

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Advanced Tool Agent                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌─────────────────┐              │
│  │   User       │────────▶│  Agent Logic    │              │
│  │  Interface   │         │  (Intent Parser)│              │
│  └──────────────┘         └────────┬────────┘              │
│                                     │                        │
│                          ┌──────────▼──────────┐            │
│                          │   Tool Executor     │            │
│                          └──────────┬──────────┘            │
│                                     │                        │
│              ┌──────────────────────┴──────────────────┐    │
│              │                                          │    │
│     ┌────────▼────────┐                    ┌───────────▼────┐
│     │  generate_code  │                    │  analyze_code  │
│     │     _with_cli   │                    │    _with_cli   │
│     └────────┬────────┘                    └───────────┬────┘
│              │                                          │    │
│              └──────────────────┬───────────────────────┘    │
│                                 │                            │
│                      ┌──────────▼──────────┐                │
│                      │  Gemini CLI Wrapper │                │
│                      │  (subprocess calls) │                │
│                      └──────────┬──────────┘                │
│                                 │                            │
└─────────────────────────────────┼────────────────────────────┘
                                  │
                         ┌────────▼────────┐
                         │   Gemini CLI    │
                         │  (Node.js CLI)  │
                         └─────────────────┘
```

## Installation

### Prerequisites

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Node.js 18+** (for Gemini CLI)
   ```bash
   node --version
   npm --version
   ```

3. **Gemini CLI**
   ```bash
   npm install -g @google/generative-ai-cli
   ```

4. **Gemini API Key**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Setup

1. **Clone or download the project**
   ```bash
   cd my-gemini-adk-agent
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Verify installation**
   ```bash
   python tests/quick_test.py
   ```

## Usage

### Interactive Mode (Recommended)

```bash
python tool_agent.py --interactive
```

Example session:
```
💬 You: Generate a Python REST API with authentication

🤖 Processing your request...

✅ Code Generated Successfully

Language: python
Complexity: medium

Generated Code:
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
...
```

### Single Request Mode

```bash
python tool_agent.py --request "Generate a Python REST API with authentication"
```

### REST API Server

Start the server:
```bash
python -m uvicorn app.server:app --host 0.0.0.0 --port 8080
```

Test endpoints:
```bash
# Health check
curl http://localhost:8080/health

# Generate code
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a user authentication system",
    "language": "python",
    "complexity": "medium"
  }'

# Analyze code
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "import os\nos.system(user_input)",
    "analysis_type": "security"
  }'

# Agent endpoint (natural language)
curl -X POST http://localhost:8080/agent \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Generate and analyze a Python REST API"
  }'
```

## Example Prompts

### Code Generation

```
Generate a Python REST API with authentication using FastAPI
```

```
Create a data pipeline in Python that processes CSV files
```

```
Build a Node.js Express API with CRUD operations
```

### Code Analysis

```
Analyze this code for security issues:

import os
def run_command(cmd):
    os.system(cmd)
```

```
Check this code for performance problems:

def find_duplicates(items):
    result = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                result.append(items[i])
    return result
```

### Combined Workflows

```
Generate a Python REST API and analyze it for security vulnerabilities
```

```
Create a data processing script and check for performance issues
```

See [test_prompts.md](test_prompts.md) for more examples.

## Testing

### Quick Test Suite

```bash
python tests/quick_test.py
```

This runs three comprehensive tests:
1. REST API generation
2. Security analysis
3. Combined workflow (generate + analyze)

### Unit Tests

```bash
python -m unittest tests/test_agent.py
```

## Deployment

### Docker

Build the image:
```bash
docker build -f deployment/Dockerfile -t advanced-tool-agent .
```

Run locally:
```bash
docker run -p 8080:8080 \
  -e GEMINI_API_KEY=your_api_key \
  advanced-tool-agent
```

### Cloud Run

1. **Set up Google Cloud**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth configure-docker
   ```

2. **Build and push**
   ```bash
   docker build -f deployment/Dockerfile -t gcr.io/YOUR_PROJECT_ID/advanced-tool-agent .
   docker push gcr.io/YOUR_PROJECT_ID/advanced-tool-agent
   ```

3. **Deploy**
   ```bash
   gcloud run deploy advanced-tool-agent \
     --image gcr.io/YOUR_PROJECT_ID/advanced-tool-agent \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GEMINI_API_KEY=your_api_key \
     --memory 1Gi \
     --timeout 300
   ```

### Cloud Build (Automated)

```bash
gcloud builds submit --config deployment/cloudbuild.yaml \
  --substitutions _GEMINI_API_KEY=your_api_key
```

## Project Structure

```
my-gemini-adk-agent/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # Main agent logic with intent parsing
│   ├── tools.py             # Gemini CLI wrappers
│   ├── server.py            # FastAPI server
│   └── utils/               # Helper modules
├── tests/
│   ├── test_agent.py        # Unit tests
│   └── quick_test.py        # Integration tests
├── deployment/
│   ├── Dockerfile           # Multi-stage Docker build
│   ├── cloudbuild.yaml      # Cloud Build configuration
│   └── .dockerignore        # Docker ignore patterns
├── tool_agent.py            # CLI entry point
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project metadata
├── .env.example             # Environment template
├── test_prompts.md          # Example prompts
└── README.md                # This file
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY` (required): Your Gemini API key
- `GEMINI_MODEL` (optional): Model to use (default: `gemini-2.0-flash-exp`)

### Tool Parameters

**generate_code_with_cli:**
- `task` (str): Description of code to generate
- `language` (str): `python`, `javascript`, or `go`
- `complexity` (str): `simple`, `medium`, or `complex`

**analyze_code_with_cli:**
- `code` (str): Code snippet to analyze
- `analysis_type` (str): `security`, `performance`, `style`, or `all`

## How It Works

1. **Intent Parsing**: Agent analyzes the user request to determine:
   - Action type (generate, analyze, or both)
   - Programming language
   - Complexity level
   - Analysis type

2. **Tool Selection**: Based on intent, agent selects appropriate tool(s)

3. **CLI Execution**: Tools invoke Gemini CLI with structured prompts:
   ```bash
   gemini --model=gemini-2.0-flash-exp think -p "<prompt>"
   ```

4. **Result Processing**: Agent processes CLI output and formats response

5. **Chained Operations**: For combined workflows, generation output feeds into analysis

## Security Considerations

- API keys are loaded from environment variables
- Never commit `.env` files to version control
- Use Cloud Secret Manager for production deployments
- Implement rate limiting for public APIs
- Validate all user inputs before processing

## Troubleshooting

### Gemini CLI Not Found

```bash
npm install -g @google/generative-ai-cli
```

### API Key Issues

```bash
# Verify API key is set
echo $GEMINI_API_KEY

# Test Gemini CLI directly
gemini --model=gemini-2.0-flash-exp think -p "Hello"
```

### Timeout Errors

Increase timeout in `tools.py`:
```python
result = cli.execute_cli_command(prompt, timeout=120)  # 2 minutes
```

### Import Errors

```bash
# Ensure you're in the project root
cd my-gemini-adk-agent

# Reinstall dependencies
pip install -r requirements.txt
```

## Performance

- Average generation time: 10-30 seconds
- Average analysis time: 15-40 seconds
- Combined workflow: 30-60 seconds
- Timeout: 60 seconds (configurable)

## Limitations

- Requires active internet connection
- Depends on Gemini CLI availability
- Rate limited by Gemini API quotas
- Code generation quality depends on prompt clarity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check [test_prompts.md](test_prompts.md) for examples
- Review error messages in logs
- Verify Gemini CLI installation
- Ensure API key is valid

## Roadmap

- [ ] Support for more programming languages
- [ ] Code refactoring suggestions
- [ ] Integration with version control
- [ ] Batch processing mode
- [ ] Web UI interface
- [ ] Code diff analysis
- [ ] Custom prompt templates
- [ ] Result caching

## Acknowledgments

- Built with Google Gemini AI
- Uses FastAPI for REST API
- Deployed on Google Cloud Run
