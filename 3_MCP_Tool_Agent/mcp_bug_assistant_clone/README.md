# MCP Bug Assistant Clone

A production-ready code analysis tool that detects bugs, security vulnerabilities, and code quality issues using MCP (Model Context Protocol) tools architecture.

## Features

- **Syntax Analysis**: Detects syntax errors in Python, JavaScript, and Java
- **Security Scanning**: Identifies dangerous patterns (eval, exec, credential exposure)
- **Bug Detection**: Finds common issues (bare except, SQL injection risks, TODO markers)
- **Fix Generation**: Provides automated fix suggestions with explanations
- **JSON Reports**: Generates detailed analysis reports
- **CLI Interface**: Easy command-line usage
- **Extensible**: Clean architecture for adding new analysis rules

## Installation

```bash
# Clone or navigate to project directory
cd mcp_bug_assistant_clone

# Install dependencies (optional - core functionality uses stdlib only)
pip install -r requirements.txt
```

## Quick Start

### Analyze a single file
```bash
python bug_assistant.py --file sample_buggy_code.py
```

### Analyze a directory
```bash
python bug_assistant.py --directory src/
```

### Specify output location
```bash
python bug_assistant.py --file mycode.py --output reports/analysis.json
```

### Default behavior (no arguments)
```bash
python bug_assistant.py
# Analyzes sample_buggy_code.py if present
```

## Usage Examples

### Basic File Analysis

```python
from bug_assistant import BugAnalyzer

analyzer = BugAnalyzer()
report = analyzer.analyze_file("mycode.py")
analyzer.generate_report("output.json")
```

### Using MCP Tools Directly

```python
from bug_assistant import MCPToolsLayer

tools = MCPToolsLayer()

# Syntax analysis
result = tools.analyze_code_syntax("def hello():\n    print('hi')", "python")
print(result)

# Bug detection
bugs = tools.detect_common_bugs("eval(user_input)", "python")
print(f"Found {bugs['bugs_found']} bugs")

# Fix generation
for bug in bugs['bugs']:
    fix = tools.generate_fix(bug)
    print(fix['explanation'])
    print(fix['patched_code'])
```

## Architecture

### MCP Tools Layer
The `MCPToolsLayer` class implements three core MCP tools:

1. **analyze_code_syntax**: AST-based syntax validation
2. **detect_common_bugs**: Pattern matching for security and quality issues
3. **generate_fix**: Automated fix suggestions

### Bug Analyzer
The `BugAnalyzer` class orchestrates analysis:
- File and directory scanning
- Result aggregation
- Report generation
- Summary statistics

## Detected Issues

### Security Issues (Critical/High)
- `eval()` and `exec()` usage
- Credential exposure in logs
- SQL injection vulnerabilities
- Dynamic imports with user input

### Error Handling (Medium)
- Bare except clauses
- Missing exception types

### Code Quality (Low)
- TODO/FIXME/HACK markers
- Incomplete implementations

## Report Format

Generated JSON reports include:

```json
{
  "files_analyzed": 1,
  "total_bugs": 5,
  "syntax_errors": 0,
  "generated_at": "2025-12-06T10:30:00",
  "reports": [
    {
      "file": "example.py",
      "language": "python",
      "syntax_analysis": {
        "valid": true,
        "errors": []
      },
      "bug_detection": {
        "bugs_found": 5,
        "bugs": [...],
        "severity_count": {
          "critical": 1,
          "high": 2,
          "medium": 1,
          "low": 1
        }
      },
      "fixes": [...]
    }
  ]
}
```

## Testing

Run the test suite:

```bash
python test_simple.py
```

Tests cover:
- Syntax analysis for valid/invalid code
- Bug detection for all issue types
- Fix generation accuracy
- Report generation
- Full integration workflow

## Environment Variables

Optional environment variables for enhanced features:

```bash
# For AI-powered analysis (future enhancement)
export GOOGLE_API_KEY="your-key"
export VERTEX_PROJECT_ID="your-project"
```

## Project Structure

```
mcp_bug_assistant_clone/
├── bug_assistant.py          # Main analyzer and MCP tools
├── sample_buggy_code.py      # Test file with intentional bugs
├── test_simple.py            # Test suite
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── demo_script.md            # Usage demonstrations
└── outputs/                  # Generated reports (auto-created)
    └── bug_report.json
```

## How MCP Tools Work

This project implements the MCP (Model Context Protocol) pattern:

1. **Tool Definition**: Each tool has a clear interface (input/output schema)
2. **Structured Data**: Tools accept and return JSON-compatible dicts
3. **Composability**: Tools can be chained and combined
4. **Stateless**: Each tool call is independent

The MCP pattern makes the analyzer:
- Easy to test
- Simple to extend
- Compatible with AI agents
- Portable across systems

## Extending the Analyzer

### Add New Bug Patterns

Edit `detect_common_bugs()` in `MCPToolsLayer`:

```python
# Add to dangerous_patterns list
dangerous_patterns.append(
    (r'your_pattern', "name", "description")
)
```

### Add New Languages

Update `analyze_code_syntax()` with language-specific parsing:

```python
elif language.lower() == "ruby":
    # Add Ruby syntax checking
    pass
```

### Add Custom Fix Rules

Extend `generate_fix()` with new fix logic:

```python
elif "your_issue" in issue_type:
    fix["explanation"] = "Your fix explanation"
    fix["patched_code"] = "Fixed code"
```

## Best Practices

- Run analysis regularly in CI/CD pipelines
- Address critical and high severity issues first
- Review fix suggestions before applying
- Use with other tools (linters, type checkers)
- Keep the tool updated with new patterns

## Limitations

- Static analysis only (no runtime behavior)
- Pattern-based detection (may have false positives)
- Language support limited to Python, JS, Java
- Fix suggestions require manual review

## Contributing

To improve the analyzer:

1. Add test cases in `test_simple.py`
2. Implement new detection patterns
3. Enhance fix generation logic
4. Add support for more languages
5. Improve accuracy and reduce false positives

## License

Open source - use and modify as needed.

## Support

For issues or questions:
- Review the demo script: `demo_script.md`
- Check test examples: `test_simple.py`
- Examine sample bugs: `sample_buggy_code.py`

---

Built with Python stdlib - no heavy dependencies required for core functionality.
