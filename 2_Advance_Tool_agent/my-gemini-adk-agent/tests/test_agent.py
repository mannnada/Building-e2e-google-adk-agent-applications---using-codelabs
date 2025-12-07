"""Comprehensive tests for the Advanced Tool Agent."""

import unittest
from unittest.mock import patch, MagicMock
from app.agent import AdvancedToolAgent
from app.tools import generate_code_with_cli, analyze_code_with_cli


class TestAdvancedToolAgent(unittest.TestCase):
    """Test cases for the Advanced Tool Agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = AdvancedToolAgent()
    
    def test_parse_intent_generate(self):
        """Test intent parsing for code generation."""
        intent = self.agent.parse_intent("Generate a Python REST API")
        self.assertEqual(intent["action"], "generate")
        self.assertEqual(intent["tool"], "generate_code")
        self.assertEqual(intent["params"]["language"], "python")
    
    def test_parse_intent_analyze(self):
        """Test intent parsing for code analysis."""
        intent = self.agent.parse_intent("Analyze this code for security issues")
        self.assertEqual(intent["action"], "analyze")
        self.assertEqual(intent["tool"], "analyze_code")
        self.assertEqual(intent["params"]["analysis_type"], "security")
    
    def test_parse_intent_both(self):
        """Test intent parsing for combined operations."""
        intent = self.agent.parse_intent("Generate and analyze a Python script")
        self.assertEqual(intent["action"], "both")
        self.assertIn("generate_code", intent["tools"])
        self.assertIn("analyze_code", intent["tools"])
    
    def test_parse_intent_javascript(self):
        """Test language detection for JavaScript."""
        intent = self.agent.parse_intent("Create a JavaScript API")
        self.assertEqual(intent["params"]["language"], "javascript")
    
    def test_parse_intent_complexity(self):
        """Test complexity detection."""
        intent = self.agent.parse_intent("Generate a complex Python algorithm")
        self.assertEqual(intent["params"]["complexity"], "complex")
    
    @patch('app.tools.GeminiCLIWrapper.execute_cli_command')
    def test_generate_code_success(self, mock_execute):
        """Test successful code generation."""
        mock_execute.return_value = {
            "success": True,
            "output": "def hello():\n    print('Hello, World!')",
            "error": None
        }
        
        result = generate_code_with_cli("Create a hello world function", "python")
        
        self.assertTrue(result["success"])
        self.assertIn("code", result)
        self.assertEqual(result["language"], "python")
    
    @patch('app.tools.GeminiCLIWrapper.execute_cli_command')
    def test_generate_code_failure(self, mock_execute):
        """Test code generation failure."""
        mock_execute.return_value = {
            "success": False,
            "output": None,
            "error": "CLI not found"
        }
        
        result = generate_code_with_cli("Create a function", "python")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    @patch('app.tools.GeminiCLIWrapper.execute_cli_command')
    def test_analyze_code_security(self, mock_execute):
        """Test security analysis."""
        mock_execute.return_value = {
            "success": True,
            "output": '{"severity": "high", "vulnerabilities": []}',
            "error": None
        }
        
        code = "import os\nos.system('rm -rf /')"
        result = analyze_code_with_cli(code, "security")
        
        self.assertTrue(result["success"])
        self.assertIn("analysis", result)
    
    @patch('app.tools.GeminiCLIWrapper.execute_cli_command')
    def test_process_request_generate(self, mock_execute):
        """Test processing a generation request."""
        mock_execute.return_value = {
            "success": True,
            "output": "def test():\n    pass",
            "error": None
        }
        
        result = self.agent.process_request("Generate a Python function")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["action"], "generate")
        self.assertIn("formatted_response", result)
    
    def test_format_generate_response(self):
        """Test formatting of generation response."""
        result = {
            "success": True,
            "code": "print('test')",
            "language": "python",
            "complexity": "simple"
        }
        
        formatted = self.agent._format_generate_response(result)
        
        self.assertIn("Code Generated Successfully", formatted)
        self.assertIn("python", formatted)
        self.assertIn("print('test')", formatted)
    
    def test_format_analyze_response(self):
        """Test formatting of analysis response."""
        result = {
            "success": True,
            "analysis": {"severity": "low", "issues": []},
            "analysis_type": "security"
        }
        
        formatted = self.agent._format_analyze_response(result)
        
        self.assertIn("Code Analysis Complete", formatted)
        self.assertIn("security", formatted)


class TestGeminiCLIWrapper(unittest.TestCase):
    """Test cases for Gemini CLI wrapper."""
    
    @patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'})
    def test_wrapper_initialization(self):
        """Test wrapper initialization with API key."""
        from app.tools import GeminiCLIWrapper
        wrapper = GeminiCLIWrapper()
        self.assertEqual(wrapper.api_key, 'test_key')
    
    def test_wrapper_no_api_key(self):
        """Test wrapper fails without API key."""
        from app.tools import GeminiCLIWrapper
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError):
                GeminiCLIWrapper()


if __name__ == '__main__':
    unittest.main()
