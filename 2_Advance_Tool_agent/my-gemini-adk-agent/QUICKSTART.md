# Quick Start Guide

Get up and running with the Advanced Tool Agent in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:

- [ ] Python 3.8 or higher
- [ ] Node.js 18 or higher
- [ ] npm (comes with Node.js)
- [ ] A Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Step 1: Install Gemini CLI

```bash
npm install -g @google/generative-ai-cli
```

Verify installation:
```bash
gemini --version
```

## Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Configure API Key

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## Step 4: Test the Agent

Run the quick test suite:
```bash
python tests/quick_test.py
```

If all tests pass, you're ready to go! ✅

## Step 5: Start Using the Agent

### Interactive Mode (Recommended for First Time)

```bash
python tool_agent.py --interactive
```

Try these example prompts:

1. **Generate a REST API:**
   ```
   Generate a Python REST API with authentication using FastAPI
   ```

2. **Analyze code for security:**
   ```
   Analyze this code for security issues:
   
   import os
   def run_cmd(user_input):
       os.system(user_input)
   ```

3. **Combined workflow:**
   ```
   Generate a Python data processing script and analyze it for performance
   ```

### Single Request Mode

```bash
python tool_agent.py --request "Generate a Python REST API"
```

### API Server Mode

Start the server:
```bash
python -m uvicorn app.server:app --host 0.0.0.0 --port 8080
```

Test with curl:
```bash
curl -X POST http://localhost:8080/agent \
  -H "Content-Type: application/json" \
  -d '{"request": "Generate a Python REST API"}'
```

## Common Issues

### "Gemini CLI not found"

Install it:
```bash
npm install -g @google/generative-ai-cli
```

### "GEMINI_API_KEY not found"

Make sure you created `.env` file with your API key:
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

### "Module not found"

Install dependencies:
```bash
pip install -r requirements.txt
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [test_prompts.md](test_prompts.md) for more example prompts
- Explore the code in `app/` directory
- Try deploying to Cloud Run (see README.md)

## Getting Help

If you encounter issues:

1. Check that Gemini CLI works directly:
   ```bash
   gemini --model=gemini-2.0-flash-exp think -p "Hello"
   ```

2. Verify your API key is valid

3. Check the logs for error messages

4. Review the troubleshooting section in README.md

## What's Next?

Now that you have the agent running, you can:

- Generate production-ready code in Python, JavaScript, or Go
- Analyze code for security vulnerabilities
- Check code for performance issues
- Review code style and best practices
- Chain operations (generate + analyze)
- Deploy to Cloud Run for production use

Happy coding! 🚀
