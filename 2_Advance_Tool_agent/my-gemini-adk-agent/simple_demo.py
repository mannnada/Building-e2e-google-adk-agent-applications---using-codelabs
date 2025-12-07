#!/usr/bin/env python3
"""Simple visual demo showing the agent processing a real request."""

import time
from app.agent import AdvancedToolAgent

def typewriter_print(text, delay=0.03):
    """Print text with typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_box(text, width=70):
    """Print text in a box."""
    print("┌" + "─" * (width - 2) + "┐")
    print("│" + text.center(width - 2) + "│")
    print("└" + "─" * (width - 2) + "┘")

def demo_scenario_1():
    """Demo: Generate a REST API"""
    print("\n" + "=" * 70)
    print_box("🎬 SCENARIO 1: Generate a REST API")
    print("=" * 70 + "\n")
    
    # User request
    request = "Generate a Python REST API with authentication"
    print("👤 User Request:")
    typewriter_print(f'   "{request}"', 0.02)
    print()
    
    time.sleep(0.5)
    
    # Agent processing
    print("🤖 Agent Processing...")
    time.sleep(0.5)
    
    agent = AdvancedToolAgent()
    
    # Step 1: Parse intent
    print("\n   Step 1: Parsing intent...")
    time.sleep(0.3)
    intent = agent.parse_intent(request)
    print(f"   ✓ Action detected: {intent['action']}")
    print(f"   ✓ Language detected: {intent['params']['language']}")
    print(f"   ✓ Complexity: {intent['params']['complexity']}")
    
    time.sleep(0.5)
    
    # Step 2: Select tool
    print("\n   Step 2: Selecting tool...")
    time.sleep(0.3)
    print(f"   ✓ Tool selected: {intent['tool']}")
    print(f"   ✓ Will call: generate_code_with_cli()")
    
    time.sleep(0.5)
    
    # Step 3: Mock execution
    print("\n   Step 3: Executing tool...")
    time.sleep(0.3)
    print("   ✓ Calling Gemini CLI...")
    print("   ✓ Command: gemini --model=gemini-2.0-flash-exp think -p '...'")
    
    time.sleep(0.5)
    
    # Step 4: Mock result
    print("\n   Step 4: Processing result...")
    time.sleep(0.3)
    print("   ✓ Code generated successfully!")
    print("   ✓ Formatting response...")
    
    time.sleep(0.5)
    
    # Final output
    print("\n" + "─" * 70)
    print("📊 RESULT:")
    print("─" * 70)
    
    mock_code = """from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel

app = FastAPI()
security = HTTPBearer()

class User(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(user: User):
    # Authentication logic here
    return {"token": "jwt_token_here"}

@app.get("/protected")
async def protected(token = Depends(security)):
    return {"message": "Access granted!"}"""
    
    print("\n✅ Generated Python REST API with authentication:\n")
    print("```python")
    print(mock_code)
    print("```")
    
    print("\n" + "=" * 70 + "\n")

def demo_scenario_2():
    """Demo: Analyze code for security"""
    print("\n" + "=" * 70)
    print_box("🎬 SCENARIO 2: Analyze Code for Security")
    print("=" * 70 + "\n")
    
    # User request with code
    dangerous_code = """import os

def run_command(user_input):
    os.system(user_input)  # Dangerous!
    result = eval(user_input)  # Very dangerous!
    return result"""
    
    print("👤 User Request:")
    typewriter_print('   "Analyze this code for security issues"', 0.02)
    print("\n📝 Code to analyze:")
    print("```python")
    print(dangerous_code)
    print("```\n")
    
    time.sleep(0.5)
    
    # Agent processing
    print("🤖 Agent Processing...")
    time.sleep(0.5)
    
    agent = AdvancedToolAgent()
    
    # Step 1: Parse intent
    print("\n   Step 1: Parsing intent...")
    time.sleep(0.3)
    request = "Analyze this code for security issues"
    intent = agent.parse_intent(request)
    print(f"   ✓ Action detected: {intent['action']}")
    print(f"   ✓ Analysis type: {intent['params']['analysis_type']}")
    
    time.sleep(0.5)
    
    # Step 2: Select tool
    print("\n   Step 2: Selecting tool...")
    time.sleep(0.3)
    print(f"   ✓ Tool selected: {intent['tool']}")
    print(f"   ✓ Will call: analyze_code_with_cli()")
    
    time.sleep(0.5)
    
    # Step 3: Mock execution
    print("\n   Step 3: Analyzing code...")
    time.sleep(0.3)
    print("   ✓ Scanning for vulnerabilities...")
    print("   ✓ Checking for dangerous functions...")
    print("   ✓ Evaluating security risks...")
    
    time.sleep(0.5)
    
    # Step 4: Mock result
    print("\n   Step 4: Generating report...")
    time.sleep(0.3)
    print("   ⚠️  Found 2 critical vulnerabilities!")
    
    time.sleep(0.5)
    
    # Final output
    print("\n" + "─" * 70)
    print("📊 SECURITY ANALYSIS RESULT:")
    print("─" * 70)
    
    print("\n🚨 Severity: HIGH\n")
    
    print("Vulnerabilities Found:\n")
    
    print("1. ⚠️  Command Injection (Line 4)")
    print("   Type: Critical Security Risk")
    print("   Issue: os.system() with user input allows arbitrary command execution")
    print("   Fix: Use subprocess.run() with argument list instead\n")
    
    print("2. ⚠️  Arbitrary Code Execution (Line 5)")
    print("   Type: Critical Security Risk")
    print("   Issue: eval() executes arbitrary Python code from user input")
    print("   Fix: Never use eval() with untrusted input. Use ast.literal_eval()\n")
    
    print("Summary:")
    print("This code has CRITICAL security vulnerabilities that could lead to")
    print("complete system compromise. Immediate remediation required!")
    
    print("\n" + "=" * 70 + "\n")

def demo_scenario_3():
    """Demo: Combined workflow"""
    print("\n" + "=" * 70)
    print_box("🎬 SCENARIO 3: Generate + Analyze (Combined)")
    print("=" * 70 + "\n")
    
    # User request
    request = "Generate a Python function to validate emails and analyze it"
    print("👤 User Request:")
    typewriter_print(f'   "{request}"', 0.02)
    print()
    
    time.sleep(0.5)
    
    # Agent processing
    print("🤖 Agent Processing...")
    time.sleep(0.5)
    
    agent = AdvancedToolAgent()
    
    # Step 1: Parse intent
    print("\n   Step 1: Parsing intent...")
    time.sleep(0.3)
    intent = agent.parse_intent(request)
    print(f"   ✓ Action detected: {intent['action']}")
    print(f"   ✓ Workflow: Generate → Analyze")
    
    time.sleep(0.5)
    
    # Step 2: Generate
    print("\n   Step 2: Generating code...")
    time.sleep(0.5)
    print("   ✓ Creating email validation function...")
    
    mock_code = """import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))"""
    
    print("\n   Generated code:")
    print("   " + "─" * 60)
    for line in mock_code.split('\n'):
        print(f"   {line}")
    print("   " + "─" * 60)
    
    time.sleep(0.5)
    
    # Step 3: Analyze
    print("\n   Step 3: Analyzing generated code...")
    time.sleep(0.5)
    print("   ✓ Checking security...")
    print("   ✓ Checking performance...")
    print("   ✓ Checking style...")
    
    time.sleep(0.5)
    
    # Final output
    print("\n" + "─" * 70)
    print("📊 COMBINED RESULT:")
    print("─" * 70)
    
    print("\n✅ Code Generation: SUCCESS")
    print("✅ Code Analysis: SUCCESS\n")
    
    print("Analysis Summary:")
    print("  • Security: ✓ No vulnerabilities found")
    print("  • Performance: ✓ Efficient regex pattern")
    print("  • Style: ✓ Follows Python best practices")
    print("  • Overall Score: 9/10")
    
    print("\n💡 Recommendation: Code is production-ready!")
    
    print("\n" + "=" * 70 + "\n")

def main():
    """Run simple demo."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + "  🤖 ADVANCED TOOL AGENT - SIMPLE DEMO  ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\nThis demo shows 3 real-world scenarios:\n")
    print("  1️⃣  Generate a REST API")
    print("  2️⃣  Analyze code for security")
    print("  3️⃣  Generate + Analyze (combined workflow)")
    
    input("\n👉 Press Enter to start the demo...")
    
    try:
        # Scenario 1
        demo_scenario_1()
        input("👉 Press Enter for next scenario...")
        
        # Scenario 2
        demo_scenario_2()
        input("👉 Press Enter for next scenario...")
        
        # Scenario 3
        demo_scenario_3()
        
        # Conclusion
        print("\n" + "=" * 70)
        print_box("🎉 DEMO COMPLETE!")
        print("=" * 70)
        
        print("\n✨ What You Just Saw:\n")
        print("  ✓ Natural language understanding")
        print("  ✓ Intelligent tool selection")
        print("  ✓ Code generation capabilities")
        print("  ✓ Security analysis")
        print("  ✓ Combined workflows")
        print("  ✓ Production-ready outputs")
        
        print("\n🚀 Ready to Try It Yourself?\n")
        print("  1. Install Gemini CLI: npm install -g @google/generative-ai-cli")
        print("  2. Add your API key to .env file")
        print("  3. Run: python tool_agent.py --interactive")
        
        print("\n📚 Documentation:")
        print("  • START_HERE.md - Quick start guide")
        print("  • README.md - Complete documentation")
        print("  • test_prompts.md - More examples")
        
        print("\n" + "=" * 70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
