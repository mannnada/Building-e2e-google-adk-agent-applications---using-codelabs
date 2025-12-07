"""Main agent with tool calling capabilities."""

import json
import logging
from typing import Dict, Any, List
from app.tools import generate_code_with_cli, analyze_code_with_cli

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AdvancedToolAgent:
    """Agent that can generate and analyze code using Gemini CLI."""
    
    def __init__(self):
        self.tools = {
            "generate_code": generate_code_with_cli,
            "analyze_code": analyze_code_with_cli
        }
        self.conversation_history: List[Dict[str, Any]] = []
    
    def parse_intent(self, user_request: str) -> Dict[str, Any]:
        """
        Parse user intent to determine which tool(s) to call.
        
        Returns:
            Dict with 'action', 'tool', and 'params'
        """
        request_lower = user_request.lower()
        
        # Check for generation keywords
        generate_keywords = ["generate", "create", "build", "write", "make", "develop"]
        analyze_keywords = ["analyze", "check", "review", "audit", "inspect", "scan", "find vulnerabilities"]
        
        has_generate = any(keyword in request_lower for keyword in generate_keywords)
        has_analyze = any(keyword in request_lower for keyword in analyze_keywords)
        
        # Detect language
        language = "python"  # default
        if "javascript" in request_lower or "js" in request_lower or "node" in request_lower:
            language = "javascript"
        elif "golang" in request_lower or " go " in request_lower:
            language = "go"
        
        # Detect complexity
        complexity = "medium"
        if "simple" in request_lower or "basic" in request_lower:
            complexity = "simple"
        elif "complex" in request_lower or "advanced" in request_lower:
            complexity = "complex"
        
        # Detect analysis type
        analysis_type = "security"
        if "performance" in request_lower:
            analysis_type = "performance"
        elif "style" in request_lower or "best practice" in request_lower:
            analysis_type = "style"
        elif "all" in request_lower or "comprehensive" in request_lower:
            analysis_type = "all"
        
        # Determine action
        if has_generate and has_analyze:
            return {
                "action": "both",
                "tools": ["generate_code", "analyze_code"],
                "params": {
                    "generate": {
                        "task": user_request,
                        "language": language,
                        "complexity": complexity
                    },
                    "analyze": {
                        "analysis_type": analysis_type
                    }
                }
            }
        elif has_generate:
            return {
                "action": "generate",
                "tool": "generate_code",
                "params": {
                    "task": user_request,
                    "language": language,
                    "complexity": complexity
                }
            }
        elif has_analyze:
            return {
                "action": "analyze",
                "tool": "analyze_code",
                "params": {
                    "code": user_request,  # Will be extracted from request
                    "analysis_type": analysis_type
                }
            }
        else:
            # Default to generation
            return {
                "action": "generate",
                "tool": "generate_code",
                "params": {
                    "task": user_request,
                    "language": language,
                    "complexity": complexity
                }
            }
    
    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with given parameters."""
        logger.info(f"Executing tool: {tool_name}")
        logger.info(f"Parameters: {json.dumps(params, indent=2)}")
        
        tool_func = self.tools.get(tool_name)
        if not tool_func:
            return {"success": False, "error": f"Tool {tool_name} not found"}
        
        try:
            result = tool_func(**params)
            logger.info(f"Tool execution completed: {result.get('success', False)}")
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def process_request(self, user_request: str) -> Dict[str, Any]:
        """
        Process a user request end-to-end.
        
        Args:
            user_request: Natural language request from user
            
        Returns:
            Dict with results and formatted response
        """
        logger.info(f"Processing request: {user_request[:100]}...")
        
        # Parse intent
        intent = self.parse_intent(user_request)
        logger.info(f"Parsed intent: {intent['action']}")
        
        # Execute based on action
        if intent["action"] == "both":
            # Generate code first, then analyze it
            logger.info("Executing chained operation: generate + analyze")
            
            # Step 1: Generate code
            gen_result = self.execute_tool("generate_code", intent["params"]["generate"])
            
            if not gen_result.get("success"):
                return {
                    "success": False,
                    "error": gen_result.get("error"),
                    "stage": "generation"
                }
            
            # Step 2: Analyze generated code
            analyze_params = intent["params"]["analyze"].copy()
            analyze_params["code"] = gen_result["code"]
            
            analyze_result = self.execute_tool("analyze_code", analyze_params)
            
            return {
                "success": True,
                "action": "both",
                "generation": gen_result,
                "analysis": analyze_result,
                "formatted_response": self._format_both_response(gen_result, analyze_result)
            }
        
        elif intent["action"] == "generate":
            result = self.execute_tool(intent["tool"], intent["params"])
            return {
                "success": result.get("success", False),
                "action": "generate",
                "result": result,
                "formatted_response": self._format_generate_response(result)
            }
        
        elif intent["action"] == "analyze":
            result = self.execute_tool(intent["tool"], intent["params"])
            return {
                "success": result.get("success", False),
                "action": "analyze",
                "result": result,
                "formatted_response": self._format_analyze_response(result)
            }
        
        else:
            return {
                "success": False,
                "error": "Unknown action type"
            }
    
    def _format_generate_response(self, result: Dict[str, Any]) -> str:
        """Format code generation response."""
        if not result.get("success"):
            return f"❌ Code generation failed: {result.get('error')}"
        
        response = f"""✅ Code Generated Successfully

Language: {result.get('language', 'unknown')}
Complexity: {result.get('complexity', 'unknown')}

Generated Code:
```{result.get('language', '')}
{result.get('code', '')}
```
"""
        return response
    
    def _format_analyze_response(self, result: Dict[str, Any]) -> str:
        """Format code analysis response."""
        if not result.get("success"):
            return f"❌ Code analysis failed: {result.get('error')}"
        
        analysis = result.get("analysis", {})
        response = f"""✅ Code Analysis Complete

Analysis Type: {result.get('analysis_type', 'unknown')}

Results:
{json.dumps(analysis, indent=2)}
"""
        return response
    
    def _format_both_response(self, gen_result: Dict[str, Any], analyze_result: Dict[str, Any]) -> str:
        """Format combined generation + analysis response."""
        response = "=" * 60 + "\n"
        response += "🤖 ADVANCED TOOL AGENT - COMPLETE WORKFLOW\n"
        response += "=" * 60 + "\n\n"
        
        # Generation section
        response += "📝 STEP 1: CODE GENERATION\n"
        response += "-" * 60 + "\n"
        if gen_result.get("success"):
            response += f"✅ Successfully generated {gen_result.get('language', 'unknown')} code\n\n"
            response += f"```{gen_result.get('language', '')}\n"
            response += f"{gen_result.get('code', '')}\n"
            response += "```\n\n"
        else:
            response += f"❌ Generation failed: {gen_result.get('error')}\n\n"
        
        # Analysis section
        response += "🔍 STEP 2: CODE ANALYSIS\n"
        response += "-" * 60 + "\n"
        if analyze_result.get("success"):
            response += f"✅ Analysis complete ({analyze_result.get('analysis_type', 'unknown')})\n\n"
            analysis = analyze_result.get("analysis", {})
            response += json.dumps(analysis, indent=2) + "\n\n"
        else:
            response += f"❌ Analysis failed: {analyze_result.get('error')}\n\n"
        
        response += "=" * 60 + "\n"
        return response
