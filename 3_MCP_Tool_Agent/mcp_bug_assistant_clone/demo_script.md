# MCP Bug Assistant - Demo Script

This document demonstrates the complete functionality of the Bug Assistant tool.

## Setup

```bash
# Navigate to project directory
cd mcp_bug_assistant_clone

# Verify Python version (3.10+ required)
python --version

# Optional: Install dev dependencies
pip install -r requirements.txt
```

## Demo 1: Analyze Sample Buggy Code

The project includes `sample_buggy_code.py` with intentional bugs for testing.

```bash
# Run default analysis
python bug_assistant.py

# Or explicitly specify the file
python bug_assistant.py --file sample_buggy_code.py
```

**Expected Output:**
```
2025-12-06 10:30:00 - INFO - Analyzing: sample_buggy_code.py
2025-12-06 10:30:00 - INFO - Report saved to: outputs/bug_report.json

============================================================
BUG ANALYSIS SUMMARY
============================================================
Files Analyzed: 1
Total Bugs Found: 15
Syntax Errors: 0

Severity Breakdown:
  Critical: 2
  High: 4
  Medium: 1
  Low: 8

Top Issues Found:

1. [CRITICAL] Potential credential exposure
   File: sample_buggy_code.py (Line 28)
   Code: print(f"User {username} logged in with password: {passw...

2. [HIGH] Dangerous function: eval
   File: sample_buggy_code.py (Line 14)
   Code: result = eval(user_input)  # DANGEROUS!...

...
============================================================
```

## Demo 2: Analyze a Directory

```bash
# Create a test directory structure
mkdir -p test_project/src
echo "eval('test')" > test_project/src/file1.py
echo "exec('code')" > test_project/src/file2.py

# Analyze the entire directory
python bug_assistant.py --directory test_project/ --output test_analysis.json
```

## Demo 3: Using MCP Tools Programmatically

Create a file `demo_usage.py`:

```python
from bug_assistant import MCPToolsLayer, BugAnalyzer

# Initialize tools
tools = MCPToolsLayer()

print("=== Demo 1: Syntax Analysis ===")
code1 = """
def hello():
    print('Hello, World!')
"""
result = tools.analyze_code_syntax(code1, "python")
print(f"Valid: {result['valid']}")
print(f"Errors: {result['errors']}")

print("\n=== Demo 2: Invalid Syntax ===")
code2 = """
def broken(
    print('Missing paren')
"""
result = tools.analyze_code_syntax(code2, "python")
print(f"Valid: {result['valid']}")
print(f"Errors: {result['errors']}")

print("\n=== Demo 3: Bug Detection ===")
code3 = """
def risky():
    user_input = input("Enter code: ")
    result = eval(user_input)
    return result
"""
bugs = tools.detect_common_bugs(code3, "python")
print(f"Bugs found: {bugs['bugs_found']}")
for bug in bugs['bugs']:
    print(f"  - [{bug['severity']}] {bug['issue']} at line {bug['line']}")

print("\n=== Demo 4: Fix Generation ===")
for bug in bugs['bugs']:
    fix = tools.generate_fix(bug)
    print(f"\nBug: {bug['issue']}")
    print(f"Explanation: {fix['explanation']}")
    print(f"Suggested Fix: {fix['suggested_fix']}")
    print(f"Patched Code: {fix['patched_code']}")

print("\n=== Demo 5: Full Analysis Workflow ===")
analyzer = BugAnalyzer()

# Analyze multiple files
analyzer.analyze_file("sample_buggy_code.py")

# Generate report
analyzer.generate_report("demo_report.json")
print("\nReport generated: demo_report.json")
```

Run it:
```bash
python demo_usage.py
```

## Demo 4: Testing Security Patterns

Create `security_test.py`:

```python
# Test file with various security issues

# Issue 1: eval usage
def dangerous_eval():
    user_code = input("Enter code: ")
    eval(user_code)  # HIGH severity

# Issue 2: exec usage
def dangerous_exec():
    exec(open('untrusted.py').read())  # HIGH severity

# Issue 3: Password logging
def login(username, password):
    print(f"Password: {password}")  # CRITICAL severity

# Issue 4: SQL injection
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)  # HIGH severity

# Issue 5: Bare except
def risky():
    try:
        dangerous_operation()
    except:  # MEDIUM severity
        pass
```

Analyze it:
```bash
python bug_assistant.py --file security_test.py --output security_report.json
```

## Demo 5: Running Tests

```bash
# Run all tests
python test_simple.py

# Expected output shows all tests passing
```

**Sample Test Output:**
```
test_detect_bare_except (__main__.TestMCPTools) ... ok
test_detect_eval_bug (__main__.TestMCPTools) ... ok
test_detect_exec_bug (__main__.TestMCPTools) ... ok
test_detect_password_logging (__main__.TestMCPTools) ... ok
test_detect_todo_markers (__main__.TestMCPTools) ... ok
test_generate_fix_for_bare_except (__main__.TestMCPTools) ... ok
test_generate_fix_for_eval (__main__.TestMCPTools) ... ok
test_syntax_analysis_invalid_python (__main__.TestMCPTools) ... ok
test_syntax_analysis_valid_python (__main__.TestMCPTools) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.123s

OK
```

## Demo 6: Examining JSON Reports

```bash
# Generate a report
python bug_assistant.py --file sample_buggy_code.py

# View the JSON report (Windows)
type outputs\bug_report.json

# Or use Python to pretty-print
python -m json.tool outputs/bug_report.json
```

**Sample Report Structure:**
```json
{
  "files_analyzed": 1,
  "total_bugs": 15,
  "syntax_errors": 0,
  "generated_at": "2025-12-06T10:30:00.123456",
  "reports": [
    {
      "file": "sample_buggy_code.py",
      "language": "python",
      "timestamp": "2025-12-06T10:30:00.123456",
      "syntax_analysis": {
        "valid": true,
        "errors": [],
        "warnings": [],
        "language": "python"
      },
      "bug_detection": {
        "bugs_found": 15,
        "bugs": [
          {
            "type": "security",
            "severity": "high",
            "line": 14,
            "code": "result = eval(user_input)",
            "issue": "Dangerous function: eval",
            "description": "Security risk: eval() can execute arbitrary code"
          }
        ],
        "severity_count": {
          "critical": 2,
          "high": 4,
          "medium": 1,
          "low": 8
        }
      },
      "fixes": [
        {
          "bug": {...},
          "fix_available": true,
          "explanation": "Replace eval() with safer alternatives...",
          "suggested_fix": "Use ast.literal_eval() or json.loads() instead",
          "patched_code": "result = ast.literal_eval(user_input)"
        }
      ]
    }
  ]
}
```

## Demo 7: Custom Analysis Script

Create `custom_analysis.py`:

```python
#!/usr/bin/env python3
"""Custom analysis workflow"""

from bug_assistant import BugAnalyzer
from pathlib import Path
import json

def analyze_project(project_path, output_dir="reports"):
    """Analyze entire project and generate detailed reports"""
    
    analyzer = BugAnalyzer()
    
    # Analyze all Python files
    project = Path(project_path)
    for py_file in project.rglob("*.py"):
        if "venv" not in str(py_file):
            print(f"Analyzing: {py_file}")
            analyzer.analyze_file(str(py_file))
    
    # Generate main report
    Path(output_dir).mkdir(exist_ok=True)
    analyzer.generate_report(f"{output_dir}/full_report.json")
    
    # Generate severity-specific reports
    results = analyzer.results
    
    critical_bugs = []
    high_bugs = []
    
    for report in results["reports"]:
        for bug in report["bug_detection"]["bugs"]:
            bug["file"] = report["file"]
            if bug["severity"] == "critical":
                critical_bugs.append(bug)
            elif bug["severity"] == "high":
                high_bugs.append(bug)
    
    # Save critical issues
    with open(f"{output_dir}/critical_issues.json", "w") as f:
        json.dump(critical_bugs, f, indent=2)
    
    # Save high priority issues
    with open(f"{output_dir}/high_priority.json", "w") as f:
        json.dump(high_bugs, f, indent=2)
    
    print(f"\nReports saved to {output_dir}/")
    print(f"Critical issues: {len(critical_bugs)}")
    print(f"High priority: {len(high_bugs)}")

if __name__ == "__main__":
    analyze_project(".", "analysis_reports")
```

Run it:
```bash
python custom_analysis.py
```

## Demo 8: Integration with CI/CD

Example GitHub Actions workflow (`.github/workflows/bug-check.yml`):

```yaml
name: Bug Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Run Bug Analysis
        run: |
          python bug_assistant.py --directory src/ --output bug_report.json
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: bug-report
          path: bug_report.json
      
      - name: Check for Critical Issues
        run: |
          python -c "
          import json
          with open('bug_report.json') as f:
              data = json.load(f)
          critical = sum(r['summary']['severity']['critical'] 
                        for r in data['reports'])
          if critical > 0:
              print(f'Found {critical} critical issues!')
              exit(1)
          "
```

## Troubleshooting

### Issue: Module not found
```bash
# Ensure you're in the correct directory
cd mcp_bug_assistant_clone

# Verify file exists
dir bug_assistant.py
```

### Issue: Permission denied
```bash
# On Unix systems, make executable
chmod +x bug_assistant.py
```

### Issue: No output generated
```bash
# Check if outputs directory was created
dir outputs

# Verify file was analyzed
python bug_assistant.py --file sample_buggy_code.py
```

## Next Steps

1. Analyze your own codebase
2. Integrate into your development workflow
3. Customize detection patterns for your needs
4. Add new language support
5. Enhance fix generation logic

## Summary

This demo covered:
- Basic CLI usage
- Programmatic API usage
- Security pattern detection
- Report generation
- Testing
- Custom workflows
- CI/CD integration

The MCP Bug Assistant is ready for production use!
