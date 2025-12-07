"""Gemini CLI wrapper tools for code generation and analysis."""

import subprocess
import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class GeminiCLIWrapper:
    """Wrapper for Gemini CLI commands with proper error handling."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash-exp"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
    
    def execute_cli_command(self, prompt: str, timeout: int = 60) -> Dict[str, Any]:
        """
        Execute Gemini CLI command in non-interactive mode.
        
        Args:
            prompt: The prompt to send to Gemini
            timeout: Command timeout in seconds
            
        Returns:
            Dict with 'success', 'output', and 'error' keys
        """
        try:
            # Construct the Gemini CLI command
            cmd = [
                "gemini",
                "--model", self.model,
                "think",
                "-p", prompt
            ]
            
            logger.info(f"Executing Gemini CLI: {' '.join(cmd[:4])}...")
            
            # Set environment with API key
            env = os.environ.copy()
            env["GEMINI_API_KEY"] = self.api_key
            
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "output": result.stdout.strip(),
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "output": None,
                    "error": result.stderr.strip() or "Command failed with no error message"
                }
                
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout} seconds")
            return {
                "success": False,
                "output": None,
                "error": f"Command timed out after {timeout} seconds"
            }
        except FileNotFoundError:
            logger.error("Gemini CLI not found. Please install it first.")
            return {
                "success": False,
                "output": None,
                "error": "Gemini CLI not found. Install with: npm install -g @google/generative-ai-cli"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "output": None,
                "error": f"Unexpected error: {str(e)}"
            }


def generate_code_with_cli(task: str, language: str = "python", complexity: str = "medium") -> Dict[str, Any]:
    """
    Generate code using Gemini CLI.
    
    Args:
        task: Description of what code to generate
        language: Programming language (python, javascript, go)
        complexity: Complexity level (simple, medium, complex)
        
    Returns:
        Dict with generated code and metadata
    """
    logger.info(f"Generating {language} code for: {task}")
    
    # Detect if this is a REST API request
    is_api = any(keyword in task.lower() for keyword in ["api", "rest", "endpoint", "flask", "fastapi", "express"])
    
    # Build the prompt based on task type
    if is_api and language == "python":
        prompt = f"""Generate a complete Python REST API using FastAPI for the following requirement:

{task}

Requirements:
- Use FastAPI framework
- Include proper error handling
- Add input validation with Pydantic models
- Include authentication if mentioned
- Add docstrings and comments
- Make it production-ready

Provide only the complete, runnable code without explanations."""
    
    elif is_api and language == "javascript":
        prompt = f"""Generate a complete Node.js REST API using Express for the following requirement:

{task}

Requirements:
- Use Express framework
- Include proper error handling
- Add input validation
- Include authentication if mentioned
- Add comments
- Make it production-ready

Provide only the complete, runnable code without explanations."""
    
    else:
        prompt = f"""Generate {complexity} {language} code for the following task:

{task}

Requirements:
- Write clean, well-documented code
- Include error handling
- Add comments explaining key logic
- Follow best practices for {language}
- Make it production-ready

Provide only the complete, runnable code without explanations."""
    
    # Execute CLI command
    cli = GeminiCLIWrapper()
    result = cli.execute_cli_command(prompt)
    
    if result["success"]:
        return {
            "success": True,
            "code": result["output"],
            "language": language,
            "task": task,
            "complexity": complexity
        }
    else:
        return {
            "success": False,
            "error": result["error"],
            "task": task
        }



def analyze_code_with_cli(code: str, analysis_type: str = "security") -> Dict[str, Any]:
    """
    Analyze code using Gemini CLI.
    
    Args:
        code: Code snippet to analyze
        analysis_type: Type of analysis (security, performance, style, all)
        
    Returns:
        Dict with analysis results in JSON format
    """
    logger.info(f"Analyzing code for: {analysis_type}")
    
    # Build analysis prompt
    if analysis_type == "security":
        prompt = f"""Analyze this code for security vulnerabilities:

```
{code}
```

Look for:
- Use of dangerous functions (exec, eval, etc.)
- SQL injection vulnerabilities
- Command injection risks
- Insecure deserialization
- Hardcoded credentials
- Path traversal issues
- XSS vulnerabilities

Return your findings as JSON with this structure:
{{
  "severity": "high|medium|low",
  "vulnerabilities": [
    {{
      "type": "vulnerability type",
      "line": "line number or range",
      "description": "detailed description",
      "recommendation": "how to fix"
    }}
  ],
  "summary": "overall security assessment"
}}"""
    
    elif analysis_type == "performance":
        prompt = f"""Analyze this code for performance issues:

```
{code}
```

Look for:
- Inefficient algorithms
- Memory leaks
- Unnecessary loops
- Database query optimization
- Caching opportunities
- Resource management

Return your findings as JSON with this structure:
{{
  "performance_score": "1-10",
  "issues": [
    {{
      "type": "issue type",
      "line": "line number or range",
      "description": "detailed description",
      "recommendation": "how to optimize"
    }}
  ],
  "summary": "overall performance assessment"
}}"""
    
    elif analysis_type == "style":
        prompt = f"""Analyze this code for style and best practices:

```
{code}
```

Look for:
- Code formatting issues
- Naming conventions
- Documentation quality
- Code organization
- Best practice violations

Return your findings as JSON with this structure:
{{
  "style_score": "1-10",
  "issues": [
    {{
      "type": "issue type",
      "line": "line number or range",
      "description": "detailed description",
      "recommendation": "how to improve"
    }}
  ],
  "summary": "overall style assessment"
}}"""
    
    else:  # all
        prompt = f"""Perform a comprehensive code analysis covering security, performance, and style:

```
{code}
```

Return your findings as JSON with this structure:
{{
  "security": {{"severity": "...", "issues": [...]}},
  "performance": {{"score": "...", "issues": [...]}},
  "style": {{"score": "...", "issues": [...]}},
  "overall_summary": "comprehensive assessment"
}}"""
    
    # Execute CLI command
    cli = GeminiCLIWrapper()
    result = cli.execute_cli_command(prompt)
    
    if result["success"]:
        # Try to parse JSON from output
        try:
            # Extract JSON from markdown code blocks if present
            output = result["output"]
            if "```json" in output:
                output = output.split("```json")[1].split("```")[0].strip()
            elif "```" in output:
                output = output.split("```")[1].split("```")[0].strip()
            
            analysis_result = json.loads(output)
            return {
                "success": True,
                "analysis": analysis_result,
                "analysis_type": analysis_type,
                "raw_output": result["output"]
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw output
            return {
                "success": True,
                "analysis": {"raw": result["output"]},
                "analysis_type": analysis_type,
                "raw_output": result["output"]
            }
    else:
        return {
            "success": False,
            "error": result["error"],
            "analysis_type": analysis_type
        }
