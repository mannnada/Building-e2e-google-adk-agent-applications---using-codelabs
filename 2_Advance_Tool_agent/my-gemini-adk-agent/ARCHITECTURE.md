# Advanced Tool Agent - Architecture Documentation

## System Overview

The Advanced Tool Agent is a sophisticated AI system that bridges natural language requests with code generation and analysis capabilities through Google's Gemini CLI.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Interactive  │  │   Single     │  │  REST API    │         │
│  │     CLI      │  │   Request    │  │   Server     │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
│         └──────────────────┴──────────────────┘                 │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    AGENT ORCHESTRATION LAYER                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              AdvancedToolAgent                         │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  1. Intent Parser                            │     │    │
│  │  │     - Detect action (generate/analyze/both)  │     │    │
│  │  │     - Extract language                       │     │    │
│  │  │     - Determine complexity                   │     │    │
│  │  │     - Identify analysis type                 │     │    │
│  │  └──────────────────┬───────────────────────────┘     │    │
│  │                     │                                  │    │
│  │  ┌──────────────────▼───────────────────────────┐     │    │
│  │  │  2. Tool Selector                            │     │    │
│  │  │     - Choose appropriate tool(s)             │     │    │
│  │  │     - Prepare parameters                     │     │    │
│  │  │     - Plan execution order                   │     │    │
│  │  └──────────────────┬───────────────────────────┘     │    │
│  │                     │                                  │    │
│  │  ┌──────────────────▼───────────────────────────┐     │    │
│  │  │  3. Tool Executor                            │     │    │
│  │  │     - Execute tool(s)                        │     │    │
│  │  │     - Handle errors                          │     │    │
│  │  │     - Chain operations                       │     │    │
│  │  └──────────────────┬───────────────────────────┘     │    │
│  │                     │                                  │    │
│  │  ┌──────────────────▼───────────────────────────┐     │    │
│  │  │  4. Response Formatter                       │     │    │
│  │  │     - Format results                         │     │    │
│  │  │     - Add metadata                           │     │    │
│  │  │     - Create user-friendly output            │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                         TOOL LAYER                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────┐    ┌─────────────────────────┐    │
│  │  generate_code_with_cli │    │  analyze_code_with_cli  │    │
│  ├─────────────────────────┤    ├─────────────────────────┤    │
│  │ • Detect API requests   │    │ • Security analysis     │    │
│  │ • Build prompts         │    │ • Performance analysis  │    │
│  │ • Call CLI wrapper      │    │ • Style analysis        │    │
│  │ • Parse responses       │    │ • Parse JSON results    │    │
│  └───────────┬─────────────┘    └───────────┬─────────────┘    │
│              │                               │                   │
│              └───────────────┬───────────────┘                   │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                    GEMINI CLI WRAPPER                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              GeminiCLIWrapper                          │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  • Validate API key                          │     │    │
│  │  │  • Build CLI command                         │     │    │
│  │  │  • Execute subprocess                        │     │    │
│  │  │  • Capture stdout/stderr                     │     │    │
│  │  │  • Handle timeouts                           │     │    │
│  │  │  • Return structured results                 │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               │ subprocess.run()
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                        GEMINI CLI                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Command: gemini --model=gemini-2.0-flash-exp think -p "..."    │
│                                                                  │
│  • Node.js CLI tool                                              │
│  • Communicates with Gemini API                                  │
│  • Returns AI-generated responses                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interfaces

#### Interactive CLI
- **Purpose**: Conversational interface for exploration
- **Entry Point**: `tool_agent.py --interactive`
- **Features**: 
  - Continuous conversation loop
  - Context preservation
  - User-friendly prompts

#### Single Request Mode
- **Purpose**: One-off command execution
- **Entry Point**: `tool_agent.py --request "..."`
- **Features**:
  - Quick execution
  - Scriptable
  - Exit after completion

#### REST API Server
- **Purpose**: Integration with other systems
- **Entry Point**: `app/server.py`
- **Endpoints**:
  - `POST /generate` - Code generation
  - `POST /analyze` - Code analysis
  - `POST /agent` - Natural language processing
  - `GET /health` - Health check

### 2. Agent Orchestration Layer

#### Intent Parser
```python
def parse_intent(user_request: str) -> Dict[str, Any]:
    """
    Analyzes user request to determine:
    - Action type (generate/analyze/both)
    - Programming language
    - Complexity level
    - Analysis type
    """
```

**Detection Logic**:
- Keywords: "generate", "create", "analyze", "check"
- Language: "python", "javascript", "go"
- Complexity: "simple", "medium", "complex"
- Analysis: "security", "performance", "style"

#### Tool Selector
```python
def execute_tool(tool_name: str, params: Dict) -> Dict:
    """
    Selects and executes appropriate tool(s)
    Handles chaining for combined operations
    """
```

#### Response Formatter
```python
def _format_*_response(result: Dict) -> str:
    """
    Formats results for user consumption
    Adds metadata and structure
    """
```

### 3. Tool Layer

#### generate_code_with_cli
```python
def generate_code_with_cli(
    task: str,
    language: str = "python",
    complexity: str = "medium"
) -> Dict[str, Any]:
```

**Capabilities**:
- REST API detection
- Framework selection (FastAPI, Express)
- Prompt engineering
- Code extraction

**Prompt Structure**:
```
Generate {complexity} {language} code for:
{task}

Requirements:
- Clean, documented code
- Error handling
- Best practices
- Production-ready
```

#### analyze_code_with_cli
```python
def analyze_code_with_cli(
    code: str,
    analysis_type: str = "security"
) -> Dict[str, Any]:
```

**Analysis Types**:
1. **Security**: SQL injection, XSS, dangerous functions
2. **Performance**: Algorithm efficiency, memory leaks
3. **Style**: Best practices, formatting
4. **All**: Comprehensive analysis

**Output Format**:
```json
{
  "severity": "high|medium|low",
  "vulnerabilities": [...],
  "summary": "..."
}
```

### 4. Gemini CLI Wrapper

#### GeminiCLIWrapper
```python
class GeminiCLIWrapper:
    def execute_cli_command(
        self,
        prompt: str,
        timeout: int = 60
    ) -> Dict[str, Any]:
```

**Features**:
- API key validation
- Subprocess management
- Timeout protection
- Error handling
- Cross-platform support

**Command Structure**:
```bash
gemini --model=gemini-2.0-flash-exp think -p "<prompt>"
```

## Data Flow

### Code Generation Flow
```
User Request
    ↓
"Generate a Python REST API"
    ↓
Intent Parser
    ↓
{action: "generate", language: "python", ...}
    ↓
Tool Selector
    ↓
generate_code_with_cli()
    ↓
GeminiCLIWrapper
    ↓
gemini CLI command
    ↓
Gemini API
    ↓
Generated Code
    ↓
Response Formatter
    ↓
Formatted Output to User
```

### Code Analysis Flow
```
User Request + Code
    ↓
"Analyze for security issues"
    ↓
Intent Parser
    ↓
{action: "analyze", type: "security", ...}
    ↓
Tool Selector
    ↓
analyze_code_with_cli()
    ↓
GeminiCLIWrapper
    ↓
gemini CLI command
    ↓
Gemini API
    ↓
Analysis Results (JSON)
    ↓
JSON Parser
    ↓
Response Formatter
    ↓
Formatted Analysis to User
```

### Combined Workflow
```
User Request
    ↓
"Generate and analyze a Python script"
    ↓
Intent Parser
    ↓
{action: "both", ...}
    ↓
Tool Selector
    ↓
Step 1: generate_code_with_cli()
    ↓
Generated Code
    ↓
Step 2: analyze_code_with_cli(generated_code)
    ↓
Analysis Results
    ↓
Response Formatter (both results)
    ↓
Complete Workflow Output to User
```

## Error Handling Strategy

### Levels of Error Handling

1. **CLI Wrapper Level**
   - Timeout errors
   - CLI not found
   - API key missing
   - Subprocess failures

2. **Tool Level**
   - Invalid parameters
   - JSON parsing errors
   - Empty responses

3. **Agent Level**
   - Intent parsing failures
   - Tool execution errors
   - Response formatting issues

4. **Interface Level**
   - User input validation
   - HTTP errors (API server)
   - Connection issues

### Error Response Format
```python
{
    "success": False,
    "error": "Descriptive error message",
    "stage": "generation|analysis|parsing",
    "details": {...}
}
```

## Security Architecture

### API Key Management
- Environment variables only
- Never logged or exposed
- Validated before use

### Input Validation
- Pydantic models for API
- Type checking
- Length limits

### Subprocess Security
- Timeout protection
- No shell=True
- Controlled environment

### Output Sanitization
- Error message filtering
- No sensitive data in logs
- Structured responses

## Performance Considerations

### Optimization Strategies
1. **Timeout Management**: 60-second default
2. **Subprocess Efficiency**: Direct command execution
3. **Response Streaming**: Capture output efficiently
4. **Error Fast-Fail**: Quick error detection

### Resource Usage
- **Memory**: ~500MB (Docker)
- **CPU**: 1 core recommended
- **Network**: Depends on Gemini API
- **Disk**: Minimal (logs only)

## Deployment Architecture

### Local Development
```
Developer Machine
    ↓
Python Environment
    ↓
tool_agent.py
    ↓
Gemini CLI (Node.js)
    ↓
Internet → Gemini API
```

### Docker Container
```
Docker Container
├── Python 3.11
├── Node.js 20
├── Gemini CLI
├── Application Code
└── FastAPI Server (port 8080)
```

### Cloud Run
```
Cloud Run Service
├── Container (from GCR)
├── Environment Variables
├── Auto-scaling (0-10 instances)
├── HTTPS Endpoint
└── Health Checks
```

## Extension Points

### Adding New Tools
```python
# In app/tools.py
def new_tool_with_cli(params) -> Dict:
    """New tool implementation"""
    pass

# In app/agent.py
self.tools["new_tool"] = new_tool_with_cli
```

### Adding New Languages
```python
# In parse_intent()
if "rust" in request_lower:
    language = "rust"
```

### Custom Analysis Types
```python
# In analyze_code_with_cli()
elif analysis_type == "custom":
    prompt = f"Custom analysis: {code}"
```

## Testing Architecture

### Unit Tests
- Mock CLI wrapper
- Test intent parsing
- Test tool execution
- Test response formatting

### Integration Tests
- Real CLI calls (with API key)
- End-to-end workflows
- Error scenarios
- Performance tests

### Test Coverage
- Agent logic: 100%
- Tools: 100%
- CLI wrapper: 90%
- Server endpoints: 100%

## Monitoring and Logging

### Log Levels
- **INFO**: Normal operations
- **WARNING**: Recoverable issues
- **ERROR**: Failures

### Logged Events
- Tool execution start/end
- CLI command execution
- Errors and exceptions
- Response times

### Health Checks
- API key validation
- CLI availability
- Server responsiveness

## Conclusion

The Advanced Tool Agent uses a layered architecture that separates concerns:
- **Interface Layer**: User interaction
- **Orchestration Layer**: Intent and workflow
- **Tool Layer**: Specific capabilities
- **Wrapper Layer**: External system integration

This design enables:
- Easy testing and maintenance
- Simple extension with new features
- Robust error handling
- Multiple deployment options
