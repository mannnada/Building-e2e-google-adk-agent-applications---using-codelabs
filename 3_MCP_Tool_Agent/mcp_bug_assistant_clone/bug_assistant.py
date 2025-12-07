#!/usr/bin/env python3
"""
MCP Bug Assistant - Advanced Code Analysis Tool
Analyzes code for bugs, security issues, and generates fixes using MCP tools.
"""

import ast
import json
import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPToolsLayer:
    """MCP Tools implementation for bug analysis"""
    
    @staticmethod
    def analyze_code_syntax(code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyze code for syntax errors
        
        Args:
            code: Source code to analyze
            language: Programming language (python, javascript, java)
            
        Returns:
            Dict with syntax analysis results
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "language": language
        }
        
        if language.lower() == "python":
            try:
                ast.parse(code)
                result["valid"] = True
            except SyntaxError as e:
                result["valid"] = False
                result["errors"].append({
                    "type": "SyntaxError",
                    "message": str(e.msg),
                    "line": e.lineno,
                    "offset": e.offset,
                    "text": e.text.strip() if e.text else ""
                })
            except Exception as e:
                result["valid"] = False
                result["errors"].append({
                    "type": type(e).__name__,
                    "message": str(e),
                    "line": None
                })
        
        elif language.lower() in ["javascript", "js"]:
            # Basic JS syntax checks
            if code.count('{') != code.count('}'):
                result["valid"] = False
                result["errors"].append({
                    "type": "SyntaxError",
                    "message": "Mismatched curly braces",
                    "line": None
                })
            if code.count('(') != code.count(')'):
                result["valid"] = False
                result["errors"].append({
                    "type": "SyntaxError",
                    "message": "Mismatched parentheses",
                    "line": None
                })
        
        return result
    
    @staticmethod
    def detect_common_bugs(code: str, language: str = "python") -> Dict[str, Any]:
        """
        Detect common bug patterns and security issues
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Dict with detected bugs
        """
        bugs = []
        lines = code.split('\n')
        
        if language.lower() == "python":
            # Dangerous function usage
            dangerous_patterns = [
                (r'\beval\s*\(', "eval", "Security risk: eval() can execute arbitrary code"),
                (r'\bexec\s*\(', "exec", "Security risk: exec() can execute arbitrary code"),
                (r'__import__\s*\(', "__import__", "Security risk: dynamic imports can be dangerous"),
            ]
            
            for i, line in enumerate(lines, 1):
                # Check dangerous patterns
                for pattern, name, message in dangerous_patterns:
                    if re.search(pattern, line):
                        bugs.append({
                            "type": "security",
                            "severity": "high",
                            "line": i,
                            "code": line.strip(),
                            "issue": f"Dangerous function: {name}",
                            "description": message
                        })
                
                # Password/secret logging
                if re.search(r'(password|secret|token|api_key)', line, re.IGNORECASE):
                    if re.search(r'(print|log|logger)', line, re.IGNORECASE):
                        bugs.append({
                            "type": "security",
                            "severity": "critical",
                            "line": i,
                            "code": line.strip(),
                            "issue": "Potential credential exposure",
                            "description": "Logging sensitive information"
                        })
                
                # Bare except
                if re.search(r'except\s*:', line):
                    bugs.append({
                        "type": "error_handling",
                        "severity": "medium",
                        "line": i,
                        "code": line.strip(),
                        "issue": "Bare except clause",
                        "description": "Catches all exceptions, may hide bugs"
                    })
                
                # TODO/FIXME markers
                if re.search(r'#\s*(TODO|FIXME|HACK|XXX)', line, re.IGNORECASE):
                    match = re.search(r'#\s*(TODO|FIXME|HACK|XXX)', line, re.IGNORECASE)
                    bugs.append({
                        "type": "code_quality",
                        "severity": "low",
                        "line": i,
                        "code": line.strip(),
                        "issue": f"{match.group(1)} marker found",
                        "description": "Incomplete or temporary code"
                    })
                
                # SQL injection risk
                if re.search(r'execute\s*\([^)]*%s|execute\s*\([^)]*\+', line):
                    bugs.append({
                        "type": "security",
                        "severity": "high",
                        "line": i,
                        "code": line.strip(),
                        "issue": "Potential SQL injection",
                        "description": "Use parameterized queries instead"
                    })
        
        # Count by severity
        severity_count = {
            "critical": sum(1 for b in bugs if b.get("severity") == "critical"),
            "high": sum(1 for b in bugs if b.get("severity") == "high"),
            "medium": sum(1 for b in bugs if b.get("severity") == "medium"),
            "low": sum(1 for b in bugs if b.get("severity") == "low")
        }
        
        return {
            "bugs_found": len(bugs),
            "bugs": bugs,
            "severity_count": severity_count,
            "language": language
        }
    
    @staticmethod
    def generate_fix(bug: Dict[str, Any], context: str = "") -> Dict[str, Any]:
        """
        Generate fix suggestions for detected bugs
        
        Args:
            bug: Bug information dict
            context: Additional code context
            
        Returns:
            Dict with fix suggestions
        """
        fix = {
            "bug": bug,
            "fix_available": True,
            "explanation": "",
            "suggested_fix": "",
            "patched_code": ""
        }
        
        issue_type = bug.get("issue", "").lower()
        original_code = bug.get("code", "")
        
        # Generate fixes based on bug type
        if "eval" in issue_type:
            fix["explanation"] = "Replace eval() with safer alternatives like ast.literal_eval() for literals, or json.loads() for JSON data."
            fix["suggested_fix"] = "Use ast.literal_eval() or json.loads() instead"
            fix["patched_code"] = original_code.replace("eval(", "ast.literal_eval(")
        
        elif "exec" in issue_type:
            fix["explanation"] = "Avoid exec() entirely. Refactor code to use functions, imports, or configuration files."
            fix["suggested_fix"] = "Refactor to eliminate exec() usage"
            fix["patched_code"] = f"# REFACTOR NEEDED: {original_code}"
        
        elif "bare except" in issue_type:
            fix["explanation"] = "Specify exception types to catch. Use 'except Exception as e:' at minimum."
            fix["suggested_fix"] = "Specify exception type"
            fix["patched_code"] = original_code.replace("except:", "except Exception as e:")
        
        elif "credential exposure" in issue_type:
            fix["explanation"] = "Never log sensitive data. Use masking or remove logging entirely."
            fix["suggested_fix"] = "Remove or mask sensitive data in logs"
            fix["patched_code"] = f"# REMOVE OR MASK: {original_code}"
        
        elif "sql injection" in issue_type:
            fix["explanation"] = "Use parameterized queries with placeholders instead of string concatenation."
            fix["suggested_fix"] = "Use parameterized queries"
            fix["patched_code"] = "cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
        
        elif "todo" in issue_type or "fixme" in issue_type:
            fix["explanation"] = "Complete the TODO/FIXME item or remove the marker if done."
            fix["suggested_fix"] = "Address the TODO/FIXME comment"
            fix["patched_code"] = original_code
        
        else:
            fix["explanation"] = "Review and address the identified issue."
            fix["suggested_fix"] = "Manual review required"
            fix["patched_code"] = original_code
        
        return fix


class BugAnalyzer:
    """Main bug analysis engine"""
    
    def __init__(self):
        self.tools = MCPToolsLayer()
        self.results = {
            "files_analyzed": 0,
            "total_bugs": 0,
            "syntax_errors": 0,
            "reports": []
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file"""
        logger.info(f"Analyzing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return {"error": str(e), "file": file_path}
        
        # Determine language
        ext = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java'
        }
        language = language_map.get(ext, 'python')
        
        # Run analysis
        syntax_result = self.tools.analyze_code_syntax(code, language)
        bug_result = self.tools.detect_common_bugs(code, language)
        
        # Generate fixes
        fixes = []
        for bug in bug_result.get("bugs", []):
            fix = self.tools.generate_fix(bug, code)
            fixes.append(fix)
        
        report = {
            "file": file_path,
            "language": language,
            "timestamp": datetime.now().isoformat(),
            "syntax_analysis": syntax_result,
            "bug_detection": bug_result,
            "fixes": fixes,
            "summary": {
                "syntax_valid": syntax_result.get("valid", True),
                "bugs_found": bug_result.get("bugs_found", 0),
                "severity": bug_result.get("severity_count", {})
            }
        }
        
        self.results["files_analyzed"] += 1
        self.results["total_bugs"] += bug_result.get("bugs_found", 0)
        if not syntax_result.get("valid", True):
            self.results["syntax_errors"] += 1
        
        self.results["reports"].append(report)
        
        return report
    
    def analyze_directory(self, dir_path: str, extensions: List[str] = None) -> List[Dict[str, Any]]:
        """Analyze all files in a directory"""
        if extensions is None:
            extensions = ['.py', '.js', '.java']
        
        reports = []
        dir_path = Path(dir_path)
        
        for ext in extensions:
            for file_path in dir_path.rglob(f'*{ext}'):
                if 'venv' in str(file_path) or 'node_modules' in str(file_path):
                    continue
                report = self.analyze_file(str(file_path))
                reports.append(report)
        
        return reports
    
    def generate_report(self, output_path: str = "bug_report.json"):
        """Generate and save analysis report"""
        self.results["generated_at"] = datetime.now().isoformat()
        
        # Save JSON report
        output_dir = Path(output_path).parent
        if output_dir and not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"Report saved to: {output_path}")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print readable summary"""
        print("\n" + "="*60)
        print("BUG ANALYSIS SUMMARY")
        print("="*60)
        print(f"Files Analyzed: {self.results['files_analyzed']}")
        print(f"Total Bugs Found: {self.results['total_bugs']}")
        print(f"Syntax Errors: {self.results['syntax_errors']}")
        
        # Aggregate severity counts
        total_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for report in self.results["reports"]:
            severity = report.get("summary", {}).get("severity", {})
            for level in total_severity:
                total_severity[level] += severity.get(level, 0)
        
        print("\nSeverity Breakdown:")
        print(f"  Critical: {total_severity['critical']}")
        print(f"  High: {total_severity['high']}")
        print(f"  Medium: {total_severity['medium']}")
        print(f"  Low: {total_severity['low']}")
        
        # Top bugs
        print("\nTop Issues Found:")
        all_bugs = []
        for report in self.results["reports"]:
            bugs = report.get("bug_detection", {}).get("bugs", [])
            for bug in bugs:
                bug["file"] = report["file"]
                all_bugs.append(bug)
        
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_bugs.sort(key=lambda x: severity_order.get(x.get("severity", "low"), 4))
        
        for i, bug in enumerate(all_bugs[:10], 1):
            print(f"\n{i}. [{bug.get('severity', 'unknown').upper()}] {bug.get('issue', 'Unknown')}")
            print(f"   File: {bug.get('file', 'unknown')} (Line {bug.get('line', '?')})")
            print(f"   Code: {bug.get('code', '')[:60]}...")
        
        print("\n" + "="*60 + "\n")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="MCP Bug Assistant - Analyze code for bugs and security issues"
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Path to a single file to analyze'
    )
    parser.add_argument(
        '--directory',
        type=str,
        help='Path to directory to analyze recursively'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='outputs/bug_report.json',
        help='Output path for JSON report (default: outputs/bug_report.json)'
    )
    parser.add_argument(
        '--extensions',
        type=str,
        nargs='+',
        default=['.py', '.js', '.java'],
        help='File extensions to analyze (default: .py .js .java)'
    )
    
    args = parser.parse_args()
    
    analyzer = BugAnalyzer()
    
    if args.file:
        analyzer.analyze_file(args.file)
    elif args.directory:
        analyzer.analyze_directory(args.directory, args.extensions)
    else:
        # Default: analyze sample file if it exists
        sample_file = "sample_buggy_code.py"
        if Path(sample_file).exists():
            logger.info(f"No file/directory specified. Analyzing {sample_file}")
            analyzer.analyze_file(sample_file)
        else:
            logger.error("No file or directory specified. Use --file or --directory")
            parser.print_help()
            sys.exit(1)
    
    analyzer.generate_report(args.output)


if __name__ == "__main__":
