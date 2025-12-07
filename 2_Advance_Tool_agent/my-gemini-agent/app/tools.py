"""
Gemini CLI Tool System

This module provides a comprehensive wrapper around Google's Gemini CLI,
enabling code generation and analysis through subprocess execution.

Key Components:
- GeminiCLIWrapper: Core class for CLI interaction
- generate_code_with_cli: Tool for generating code
- analyze_code_with_cli: Tool for analyzing code

Author: AI Agent Builder
License: MIT
"""

import subprocess
import json
import logging
import os
import sys
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ToolResult:
    """
    Structured result from tool execution.
    
    Attributes:
        success: Whether the tool executed successfully
        data: The main result data
        error: Error message if execution failed
        execution_time: Time taken to execute in seconds
        tool_name: Name of the tool that was executed
        metadata: Additional metadata about the execution
    """
    success: bool
    data: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    tool_name: str = ""
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary format."""
        return asdict(self)


class GeminiCLIWrapper:
    """
    Comprehensive wrapper for Google Gemini CLI interactions.
    
    This class handles all subprocess execution, error handling, timeout management,
    and logging for Gemini CLI commands. It ensures robust and reliable CLI operations
    with proper validation and error recovery.
    
    Features:
    - Automatic API key validation
    - Timeout protection (default 40 seconds)
    - Comprehensive error handling
    - Command logging for debugging
    - Cross-platform compatibility (Windows, Linux, macOS)
    - Structured response parsing
    
    Example:
        wrapper = GeminiCLIWrapper()
        result = wrapper.execute_prompt("Generate a Python function")
    """
    
    def __init__(self, api_key: Optional[str] = None, timeout: int = 40):
        """
        Initialize the Gemini CLI wrapper.
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            timeout: Maximum execution time in seconds (default: 40)
        
        Raises:
            ValueError: If API key is not provided or found in environment
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.timeout = timeout
        
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment")
            raise ValueError(
                "GEMINI_API_KEY must be set in environment or passed to constructor. "
                "Please set it in your .env file or environment variables."
            )
        
        # Set API key in environment for CLI to use
        os.environ['GEMINI_API_KEY'] = self.api_key
        
        # Detect operating system for command compatibility
        self.is_windows = sys.platform.startswith('win')
        self.gemini_command = self._get_gemini_command()
        
        logger.info(f"GeminiCLIWrapper initialized (OS: {sys.platform}, timeout: {timeout}s)")
    
    def _get_gemini_command(self) -> str:
        """
        Determine the correct Gemini CLI command for the current platform.
        
        Returns:
            Command string to execute Gemini CLI
        """
        # Try to find gemini in PATH
        if self.is_windows:
            # On Windows, try both 'gemini' and 'gemini.cmd'
            return 'gemini'
        else:
            # On Unix-like systems
            return 'gemini'
    
    def _validate_cli_installation(self) -> bool:
        """
        Validate that Gemini CLI is properly installed and accessible.
        
        Returns:
            True if CLI is installed, False otherwise
        """
        try:
            result = subprocess.run(
                [self.gemini_command, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"Gemini CLI version: {result.stdout.strip()}")
                return True
            return False
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.error(f"Gemini CLI validation failed: {e}")
            return False
    
    def execute_prompt(self, prompt: str, max_retries: int = 2) -> ToolResult:
        """
        Execute a prompt using Gemini CLI with retry logic.
        
        This method handles the core CLI execution with comprehensive error handling,
        timeout protection, and automatic retries on transient failures.
        
        Args:
            prompt: The prompt to send to Gemini
            max_retries: Maximum number of retry attempts (default: 2)
        
        Returns:
            ToolResult containing the CLI response or error information
        
        Example:
            result = wrapper.execute_prompt("Generate a Python function")
            if result.success:
                print(result.data)
        """
        start_time = time.time()
        
        # Log the command being executed (truncate long prompts)
        prompt_preview = prompt[:100] + "..." if len(prompt) > 100 else prompt
        logger.info(f"Executing Gemini CLI: gemini -p \"{prompt_preview}\"")
        
        for attempt in range(max_retries + 1):
            try:
                # Build the command
                command = [self.gemini_command, '-p', prompt]
                
                # Execute the CLI command
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    env=os.environ.copy()  # Pass environment variables
                )
                
                execution_time = time.time() - start_time
                
                # Check if command executed successfully
                if result.returncode == 0:
                    output = result.stdout.strip()
                    logger.info(f"CLI execution successful (took {execution_time:.2f}s)")
                    
                    return ToolResult(
                        success=True,
                        data=output,
                        execution_time=execution_time,
                        tool_name="gemini_cli",
                        metadata={
                            "prompt_length": len(prompt),
                            "response_length": len(output),
                            "attempt": attempt + 1
                        }
                    )
                else:
                    # Command failed, log error
                    error_msg = result.stderr.strip() or "Unknown error"
                    logger.warning(f"CLI returned error (attempt {attempt + 1}): {error_msg}")
                    
                    if attempt < max_retries:
                        logger.info(f"Retrying... ({attempt + 1}/{max_retries})")
                        time.sleep(1)  # Brief delay before retry
                        continue
                    
                    return ToolResult(
                        success=False,
                        data=None,
                        error=f"CLI execution failed: {error_msg}",
                        execution_time=time.time() - start_time,
                        tool_name="gemini_cli"
                    )
            
            except subprocess.TimeoutExpired:
                logger.error(f"CLI execution timed out after {self.timeout}s")
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Execution timed out after {self.timeout} seconds",
                    execution_time=self.timeout,
                    tool_name="gemini_cli"
                )
            
            except FileNotFoundError:
                logger.error("Gemini CLI not found. Is it installed?")
                return ToolResult(
                    success=False,
                    data=None,
                    error="Gemini CLI not found. Please install: npm install -g @google/generative-ai-cli",
                    execution_time=time.time() - start_time,
                    tool_name="gemini_cli"
                )
            
            except Exception as e:
                logger.error(f"Unexpected error during CLI execution: {e}")
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Unexpected error: {str(e)}",
                    execution_time=time.time() - start_time,
                    tool_name="gemini_cli"
                )
        
        # Should never reach here, but just in case
        return ToolResult(
            success=False,
            data=None,
            error="Maximum retries exceeded",
            execution_time=time.time() - start_time,
            tool_name="gemini_cli"
        )


def generate_code_with_cli(
    task: str,
    language: str = "Python",
    complexity: str = "intermediate"
) -> Dict[str, Any]:
    """
    Generate code using Gemini CLI based on task description.
    
    This tool constructs an optimized prompt for code generation and executes
    it through the Gemini CLI. It handles REST API requests specially and
    ensures generated code includes descriptive comments.
    
    Args:
        task: Description of what code to generate
        language: Programming language (default: "Python")
        complexity: Code complexity level - "simple", "intermediate", or "advanced"
    
    Returns:
        Dictionary containing:
            - success: bool
            - code: Generated code string
            - language: Programming language used
            - description: Description of generated code
            - error: Error message if failed
            - execution_time: Time taken
    
    Example:
        result = generate_code_with_cli(
            task="REST API with JWT authentication",
            language="Python",
            complexity="advanced"
        )
        print(result['code'])
    """
    logger.info(f"Generating {complexity} {language} code for: {task}")
    
    # Detect if this is a REST API request
    is_rest_api = any(keyword in task.lower() for keyword in [
        'rest', 'api', 'endpoint', 'flask', 'fastapi', 'express', 'route'
    ])
    
    # Construct optimized prompt
    if is_rest_api:
        prompt = f"""Generate a complete, production-ready {complexity} {language} REST API for: {task}

Requirements:
- Include all necessary imports
- Add comprehensive error handling
- Include input validation
- Add descriptive comments explaining each section
- Use best practices for {language}
- Include example usage in comments
- Make it ready to run immediately

Return ONLY the code, no explanations before or after."""
    else:
        prompt = f"""Generate {complexity} {language} code for: {task}

Requirements:
- Include all necessary imports and dependencies
- Add descriptive comments explaining the logic
- Include error handling where appropriate
- Follow {language} best practices and conventions
- Make the code production-ready
- Include example usage if applicable

Return ONLY the code, no explanations before or after."""
    
    # Execute through CLI wrapper
    try:
        wrapper = GeminiCLIWrapper()
        result = wrapper.execute_prompt(prompt)
        
        if result.success:
            generated_code = result.data
            
            # Extract code if wrapped in markdown code blocks
            if '```' in generated_code:
                # Find code between triple backticks
                parts = generated_code.split('```')
                if len(parts) >= 3:
                    # Get the code block (usually the second part)
                    code_block = parts[1]
                    # Remove language identifier if present
                    lines = code_block.split('\n')
                    if lines[0].strip().lower() in ['python', 'javascript', 'typescript', 'java', 'go', 'rust']:
                        generated_code = '\n'.join(lines[1:])
                    else:
                        generated_code = code_block
            
            return {
                "success": True,
                "code": generated_code.strip(),
                "language": language,
                "complexity": complexity,
                "description": f"Generated {complexity} {language} code for: {task}",
                "execution_time": result.execution_time,
                "metadata": result.metadata
            }
        else:
            return {
                "success": False,
                "code": None,
                "language": language,
                "error": result.error,
                "execution_time": result.execution_time
            }
    
    except Exception as e:
        logger.error(f"Error in generate_code_with_cli: {e}")
        return {
            "success": False,
            "code": None,
            "language": language,
            "error": f"Code generation failed: {str(e)}",
            "execution_time": 0.0
        }


def analyze_code_with_cli(
    code: str,
    analysis_type: str = "security"
) -> Dict[str, Any]:
    """
    Analyze code using Gemini CLI for various issues.
    
    This tool performs comprehensive code analysis including security vulnerabilities,
    performance issues, naming conventions, and best practices violations.
    
    Args:
        code: The code snippet to analyze
        analysis_type: Type of analysis - "security", "performance", "quality", or "all"
    
    Returns:
        Dictionary containing:
            - success: bool
            - findings: List of issues found
            - risk_level: Overall risk level (low, medium, high, critical)
            - suggestions: List of suggested fixes
            - analysis_type: Type of analysis performed
            - error: Error message if failed
    
    Example:
        result = analyze_code_with_cli(
            code="def login(u): exec(u)",
            analysis_type="security"
        )
        print(result['findings'])
    """
    logger.info(f"Analyzing code for {analysis_type} issues")
    
    # Define analysis focus based on type
    analysis_focuses = {
        "security": [
            "SQL injection vulnerabilities",
            "Command injection (exec, eval, system calls)",
            "Path traversal vulnerabilities",
            "Insecure deserialization",
            "Hardcoded credentials or secrets",
            "Insufficient input validation",
            "Authentication and authorization issues"
        ],
        "performance": [
            "Inefficient algorithms or data structures",
            "Unnecessary loops or iterations",
            "Memory leaks or excessive memory usage",
            "Blocking operations that should be async",
            "Database query optimization opportunities",
            "Caching opportunities"
        ],
        "quality": [
            "Poor naming conventions",
            "Missing error handling",
            "Code duplication",
            "Overly complex functions",
            "Missing documentation",
            "Violation of SOLID principles"
        ],
        "all": [
            "Security vulnerabilities",
            "Performance issues",
            "Code quality problems",
            "Best practices violations"
        ]
    }
    
    focus_items = analysis_focuses.get(analysis_type, analysis_focuses["all"])
    focus_text = "\n".join(f"- {item}" for item in focus_items)
    
    # Construct analysis prompt
    prompt = f"""Analyze the following code for {analysis_type} issues:

```
{code}
```

Focus on detecting:
{focus_text}

Provide a structured analysis with:
1. List of specific issues found (be concrete and specific)
2. Risk level for each issue (low, medium, high, critical)
3. Suggested fixes for each issue
4. Overall risk assessment

Format your response as a clear, structured analysis."""
    
    # Execute through CLI wrapper
    try:
        wrapper = GeminiCLIWrapper()
        result = wrapper.execute_prompt(prompt)
        
        if result.success:
            analysis_text = result.data
            
            # Parse the analysis to extract structured information
            findings = []
            risk_level = "low"
            suggestions = []
            
            # Simple parsing logic (can be enhanced with more sophisticated NLP)
            lines = analysis_text.split('\n')
            current_section = None
            
            for line in lines:
                line_lower = line.lower().strip()
                
                # Detect risk levels
                if any(word in line_lower for word in ['critical', 'severe', 'dangerous']):
                    risk_level = "critical"
                elif risk_level != "critical" and any(word in line_lower for word in ['high', 'major']):
                    risk_level = "high"
                elif risk_level not in ["critical", "high"] and any(word in line_lower for word in ['medium', 'moderate']):
                    risk_level = "medium"
                
                # Extract findings (lines that mention issues)
                if any(word in line_lower for word in ['vulnerability', 'issue', 'problem', 'risk', 'exec', 'eval', 'injection']):
                    if line.strip() and not line.strip().startswith('#'):
                        findings.append(line.strip())
                
                # Extract suggestions (lines that mention fixes or recommendations)
                if any(word in line_lower for word in ['fix', 'recommend', 'should', 'use', 'replace', 'instead']):
                    if line.strip() and not line.strip().startswith('#'):
                        suggestions.append(line.strip())
            
            # Ensure we have at least some findings
            if not findings:
                findings = ["Analysis completed - see full report for details"]
            
            if not suggestions:
                suggestions = ["Review the code against best practices"]
            
            return {
                "success": True,
                "findings": findings[:10],  # Limit to top 10 findings
                "risk_level": risk_level,
                "suggestions": suggestions[:10],  # Limit to top 10 suggestions
                "analysis_type": analysis_type,
                "full_analysis": analysis_text,
                "execution_time": result.execution_time,
                "metadata": result.metadata
            }
        else:
            return {
                "success": False,
                "findings": [],
                "risk_level": "unknown",
                "suggestions": [],
                "analysis_type": analysis_type,
                "error": result.error,
                "execution_time": result.execution_time
            }
    
    except Exception as e:
        logger.error(f"Error in analyze_code_with_cli: {e}")
        return {
            "success": False,
            "findings": [],
            "risk_level": "unknown",
            "suggestions": [],
            "analysis_type": analysis_type,
            "error": f"Code analysis failed: {str(e)}",
            "execution_time": 0.0
        }


# Tool registry for easy access
AVAILABLE_TOOLS = {
    "generate_code": generate_code_with_cli,
    "analyze_code": analyze_code_with_cli
}


def get_tool(tool_name: str):
    """
    Retrieve a tool by name from the registry.
    
    Args:
        tool_name: Name of the tool to retrieve
    
    Returns:
        Tool function or None if not found
    """
    return AVAILABLE_TOOLS.get(tool_name)


def list_available_tools() -> List[str]:
    """
    Get list of all available tool names.
    
    Returns:
        List of tool names
    """
    return list(AVAILABLE_TOOLS.keys())


if __name__ == "__main__":
    # Quick test of the tools
    print("Testing Gemini CLI Tools...")
    print("=" * 60)
    
    # Test code generation
    print("\n1. Testing Code Generation...")
    gen_result = generate_code_with_cli(
        task="a function to validate email addresses",
        language="Python",
        complexity="simple"
    )
    print(f"Success: {gen_result['success']}")
    if gen_result['success']:
        print(f"Generated code:\n{gen_result['code'][:200]}...")
    
    # Test code analysis
    print("\n2. Testing Code Analysis...")
    test_code = "def login(username): exec(username)"
    analysis_result = analyze_code_with_cli(test_code, "security")
    print(f"Success: {analysis_result['success']}")
    if analysis_result['success']:
        print(f"Risk Level: {analysis_result['risk_level']}")
        print(f"Findings: {len(analysis_result['findings'])}")
    
    print("\n" + "=" * 60)
    print("Tool testing complete!")
