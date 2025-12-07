#!/usr/bin/env python3
"""
Simple test suite for Bug Assistant
Tests core functionality of the MCP tools and analyzer
"""

import unittest
import json
import os
from pathlib import Path
from bug_assistant import MCPToolsLayer, BugAnalyzer


class TestMCPTools(unittest.TestCase):
    """Test MCP Tools Layer"""
    
    def setUp(self):
        self.tools = MCPToolsLayer()
    
    def test_syntax_analysis_valid_python(self):
        """Test syntax analysis with valid Python code"""
        code = "def hello():\n    print('Hello, World!')"
        result = self.tools.analyze_code_syntax(code, "python")
        
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)
        self.assertEqual(result["language"], "python")
    
    def test_syntax_analysis_invalid_python(self):
        """Test syntax analysis with invalid Python code"""
        code = "def hello(\n    print('Missing closing paren')"
        result = self.tools.analyze_code_syntax(code, "python")
        
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["errors"]), 0)
    
    def test_detect_eval_bug(self):
        """Test detection of eval() usage"""
        code = "result = eval(user_input)"
        result = self.tools.detect_common_bugs(code, "python")
        
        self.assertGreater(result["bugs_found"], 0)
        bugs = result["bugs"]
        eval_bugs = [b for b in bugs if "eval" in b["issue"].lower()]
        self.assertGreater(len(eval_bugs), 0)
        self.assertEqual(eval_bugs[0]["severity"], "high")
    
    def test_detect_exec_bug(self):
        """Test detection of exec() usage"""
        code = "exec(malicious_code)"
        result = self.tools.detect_common_bugs(code, "python")
        
        self.assertGreater(result["bugs_found"], 0)
        bugs = result["bugs"]
        exec_bugs = [b for b in bugs if "exec" in b["issue"].lower()]
        self.assertGreater(len(exec_bugs), 0)
    
    def test_detect_bare_except(self):
        """Test detection of bare except clause"""
        code = "try:\n    risky()\nexcept:\n    pass"
        result = self.tools.detect_common_bugs(code, "python")
        
        bugs = result["bugs"]
        bare_except_bugs = [b for b in bugs if "bare except" in b["issue"].lower()]
        self.assertGreater(len(bare_except_bugs), 0)
    
    def test_detect_password_logging(self):
        """Test detection of password logging"""
        code = "print(f'Password: {password}')"
        result = self.tools.detect_common_bugs(code, "python")
        
        bugs = result["bugs"]
        cred_bugs = [b for b in bugs if "credential" in b["issue"].lower()]
        self.assertGreater(len(cred_bugs), 0)
        self.assertEqual(cred_bugs[0]["severity"], "critical")
    
    def test_detect_todo_markers(self):
        """Test detection of TODO/FIXME markers"""
        code = "# TODO: Implement this\n# FIXME: Bug here"
        result = self.tools.detect_common_bugs(code, "python")
        
        bugs = result["bugs"]
        todo_bugs = [b for b in bugs if b["type"] == "code_quality"]
        self.assertGreaterEqual(len(todo_bugs), 2)
    
    def test_generate_fix_for_eval(self):
        """Test fix generation for eval() bug"""
        bug = {
            "issue": "Dangerous function: eval",
            "code": "result = eval(data)",
            "severity": "high"
        }
        fix = self.tools.generate_fix(bug)
        
        self.assertTrue(fix["fix_available"])
        self.assertIn("ast.literal_eval", fix["explanation"])
        self.assertIn("ast.literal_eval", fix["patched_code"])
    
    def test_generate_fix_for_bare_except(self):
        """Test fix generation for bare except"""
        bug = {
            "issue": "Bare except clause",
            "code": "except:",
            "severity": "medium"
        }
        fix = self.tools.generate_fix(bug)
        
        self.assertTrue(fix["fix_available"])
        self.assertIn("Exception", fix["patched_code"])
    
    def test_severity_counting(self):
        """Test severity counting in bug detection"""
        code = """
eval(x)  # high
exec(y)  # high
print(password)  # critical
# TODO: fix  # low
"""
        result = self.tools.detect_common_bugs(code, "python")
        severity = result["severity_count"]
        
        self.assertGreater(severity["critical"], 0)
        self.assertGreater(severity["high"], 0)
        self.assertGreater(severity["low"], 0)


class TestBugAnalyzer(unittest.TestCase):
    """Test Bug Analyzer"""
    
    def setUp(self):
        self.analyzer = BugAnalyzer()
        self.test_file = "test_temp_code.py"
    
    def tearDown(self):
        # Clean up test file
        if Path(self.test_file).exists():
            os.remove(self.test_file)
        
        # Clean up test report
        if Path("test_report.json").exists():
            os.remove("test_report.json")
    
    def test_analyze_file(self):
        """Test file analysis"""
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write("def test():\n    eval('x')\n")
        
        report = self.analyzer.analyze_file(self.test_file)
        
        self.assertIn("file", report)
        self.assertIn("syntax_analysis", report)
        self.assertIn("bug_detection", report)
        self.assertIn("fixes", report)
        self.assertEqual(report["file"], self.test_file)
    
    def test_report_generation(self):
        """Test report generation"""
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write("print('test')")
        
        self.analyzer.analyze_file(self.test_file)
        self.analyzer.generate_report("test_report.json")
        
        self.assertTrue(Path("test_report.json").exists())
        
        with open("test_report.json", 'r') as f:
            report = json.load(f)
        
        self.assertIn("files_analyzed", report)
        self.assertIn("total_bugs", report)
        self.assertIn("reports", report)
        self.assertEqual(report["files_analyzed"], 1)
    
    def test_results_accumulation(self):
        """Test that results accumulate correctly"""
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write("eval('x')\nexec('y')")
        
        self.analyzer.analyze_file(self.test_file)
        
        self.assertEqual(self.analyzer.results["files_analyzed"], 1)
        self.assertGreater(self.analyzer.results["total_bugs"], 0)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_analysis_workflow(self):
        """Test complete analysis workflow"""
        test_file = "integration_test.py"
        report_file = "integration_report.json"
        
        try:
            # Create buggy test file
            with open(test_file, 'w') as f:
                f.write("""
def buggy_function():
    eval('dangerous')
    try:
        risky()
    except:
        pass
    # TODO: Fix this
""")
            
            # Run analysis
            analyzer = BugAnalyzer()
            analyzer.analyze_file(test_file)
            analyzer.generate_report(report_file)
            
            # Verify report
            self.assertTrue(Path(report_file).exists())
            
            with open(report_file, 'r') as f:
                report = json.load(f)
            
            self.assertEqual(report["files_analyzed"], 1)
            self.assertGreater(report["total_bugs"], 0)
            
            # Check that multiple bug types were detected
            bugs = report["reports"][0]["bug_detection"]["bugs"]
            bug_types = set(b["type"] for b in bugs)
            self.assertGreater(len(bug_types), 1)
            
        finally:
            # Cleanup
            if Path(test_file).exists():
                os.remove(test_file)
            if Path(report_file).exists():
                os.remove(report_file)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()
