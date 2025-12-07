# Test Prompts for Advanced Tool Agent

This document contains example prompts to test the agent's capabilities.

## Code Generation Prompts

### REST API Generation

```
Generate a Python REST API with authentication using FastAPI
```

```
Create a Node.js Express API with user registration and login endpoints
```

```
Build a Python FastAPI service with CRUD operations for a blog system
```

### Data Pipeline Generation

```
Generate a Python data pipeline that reads CSV files and processes them
```

```
Create a Python script that fetches data from an API and stores it in a database
```

### Script Generation

```
Write a Python script to monitor system resources and send alerts
```

```
Generate a JavaScript function to validate email addresses with regex
```

```
Create a Go program that reads environment variables and starts a web server
```

## Code Analysis Prompts

### Security Analysis

```
Analyze this code for security vulnerabilities:

import os
import pickle

def process_data(user_input):
    result = eval(user_input)
    os.system(f"echo {user_input}")
    data = pickle.loads(user_input)
    return result
```

```
Check this code for SQL injection risks:

def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)
```

### Performance Analysis

```
Analyze this code for performance issues:

def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates
```

### Style Analysis

```
Analyze this code for style and best practices:

def calc(x,y,op):
    if op=="add":
        return x+y
    elif op=="sub":
        return x-y
    else:
        return None
```

## Combined Workflow Prompts

### Generate + Analyze

```
Generate a Python REST API with authentication and analyze it for security issues
```

```
Create a data processing script in Python and check it for performance problems
```

```
Build a JavaScript API endpoint and analyze it for security vulnerabilities
```

```
Generate a Python function to parse JSON and analyze it for error handling
```

## Complex Prompts

### Advanced REST API

```
Generate a complex Python FastAPI application with:
- User authentication (JWT)
- CRUD operations for products
- Database integration
- Input validation
- Error handling
- API documentation
```

### Data Pipeline with Analysis

```
Create a Python data pipeline that:
1. Fetches data from multiple APIs
2. Transforms and validates the data
3. Stores results in a database
Then analyze it for performance and security issues
```

### Microservice

```
Generate a simple microservice in Python that:
- Accepts webhook events
- Validates payloads
- Processes events asynchronously
- Logs all activities
Then check for security vulnerabilities
```

## Language-Specific Prompts

### Python

```
Generate a Python class for managing a connection pool with context managers
```

### JavaScript

```
Create a JavaScript module for handling async operations with promises and error handling
```

### Go

```
Write a Go program with goroutines for concurrent file processing
```

## Testing the Agent

To test these prompts:

1. **Interactive Mode:**
   ```bash
   python tool_agent.py --interactive
   ```
   Then paste any prompt from above.

2. **Single Request Mode:**
   ```bash
   python tool_agent.py --request "Generate a Python REST API"
   ```

3. **Quick Test Suite:**
   ```bash
   python tests/quick_test.py
   ```

4. **API Mode:**
   ```bash
   # Start server
   python -m uvicorn app.server:app --host 0.0.0.0 --port 8080
   
   # Test with curl
   curl -X POST http://localhost:8080/agent \
     -H "Content-Type: application/json" \
     -d '{"request": "Generate a Python REST API"}'
   ```

## Expected Behaviors

### For Generation Prompts:
- Agent should detect the language (Python, JavaScript, Go)
- Agent should identify if it's an API request
- Agent should generate complete, runnable code
- Output should include proper error handling and comments

### For Analysis Prompts:
- Agent should detect the analysis type (security, performance, style)
- Agent should identify specific issues in the code
- Output should be in JSON format with detailed findings
- Should highlight dangerous patterns (eval, exec, SQL injection, etc.)

### For Combined Prompts:
- Agent should execute generation first
- Then automatically analyze the generated code
- Should provide both code and analysis results
- Should show the complete workflow

## Notes

- All prompts require `GEMINI_API_KEY` to be set in `.env`
- Gemini CLI must be installed: `npm install -g @google/generative-ai-cli`
- Some prompts may take 30-60 seconds to complete
- Complex prompts may require higher timeout values
