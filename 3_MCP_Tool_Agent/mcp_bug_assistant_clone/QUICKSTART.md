# Quick Start Guide

Get up and running with MCP Bug Assistant in 2 minutes.

## Installation

```bash
cd mcp_bug_assistant_clone
```

No dependencies required for basic usage! (Uses Python stdlib only)

## Run Your First Analysis

```bash
# Analyze the sample buggy code
python bug_assistant.py
```

You'll see output like:
```
Files Analyzed: 1
Total Bugs Found: 18
  Critical: 4
  High: 6
  Medium: 2
  Low: 6
```

## Check the Report

```bash
# View the generated JSON report
type outputs\bug_report.json
```

## Analyze Your Own Code

```bash
# Single file
python bug_assistant.py --file yourcode.py

# Entire directory
python bug_assistant.py --directory src/

# Custom output location
python bug_assistant.py --file app.py --output reports/analysis.json
```

## Run Tests

```bash
python test_simple.py
```

All 14 tests should pass!

## What Gets Detected?

- **Critical**: Password/secret logging, credential exposure
- **High**: eval(), exec(), SQL injection risks
- **Medium**: Bare except clauses, poor error handling
- **Low**: TODO/FIXME markers, code quality issues

## Next Steps

1. Read the full [README.md](README.md)
2. Try the [demo_script.md](demo_script.md) examples
3. Analyze your project
4. Review the generated reports
5. Apply the suggested fixes

## Example Output

```
Top Issues Found:

1. [CRITICAL] Potential credential exposure
   File: mycode.py (Line 42)
   Code: print(f"Password: {password}")

2. [HIGH] Dangerous function: eval
   File: mycode.py (Line 15)
   Code: result = eval(user_input)
```

Each issue includes:
- Severity level
- Line number
- Code snippet
- Fix suggestion
- Explanation

That's it! You're ready to find bugs.
