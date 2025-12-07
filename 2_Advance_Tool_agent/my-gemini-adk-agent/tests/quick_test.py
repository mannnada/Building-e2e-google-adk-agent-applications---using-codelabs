#!/usr/bin/env python3
"""Quick test script to verify agent functionality."""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent import AdvancedToolAgent

load_dotenv()


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def test_rest_api_generation():
    """Test REST API generation."""
    print_section("TEST 1: REST API Generation")
    
    agent = AdvancedToolAgent()
    request = "Generate a Python REST API with authentication using FastAPI"
    
    print(f"Request: {request}\n")
    print("🤖 Processing...\n")
    
    result = agent.process_request(request)
    
    if result.get("success"):
        print("✅ Test PASSED")
        print("\nTool Calls:")
        print(f"  - Action: {result.get('action')}")
        print(f"  - Tool: generate_code")
        print(f"\nGenerated Code Preview:")
        code = result.get("result", {}).get("code", "")
        print(code[:500] + "..." if len(code) > 500 else code)
    else:
        print("❌ Test FAILED")
        print(f"Error: {result.get('error')}")
    
    return result.get("success", False)


def test_security_analysis():
    """Test security analysis."""
    print_section("TEST 2: Security Analysis")
    
    agent = AdvancedToolAgent()
    
    # Sample code with security issues
    code_to_analyze = """
import os
import pickle

def process_user_input(user_data):
    # Dangerous: using eval
    result = eval(user_data)
    
    # Dangerous: command injection
    os.system(f"echo {user_data}")
    
    # Dangerous: insecure deserialization
    data = pickle.loads(user_data)
    
    return result
"""
    
    request = f"Analyze this code for security vulnerabilities: {code_to_analyze}"
    
    print(f"Request: Analyze code for security issues\n")
    print("Code to analyze:")
    print(code_to_analyze)
    print("\n🤖 Processing...\n")
    
    result = agent.process_request(request)
    
    if result.get("success"):
        print("✅ Test PASSED")
        print("\nTool Calls:")
        print(f"  - Action: {result.get('action')}")
        print(f"  - Tool: analyze_code")
        print(f"\nAnalysis Preview:")
        analysis = result.get("result", {}).get("analysis", {})
        print(str(analysis)[:500] + "..." if len(str(analysis)) > 500 else str(analysis))
    else:
        print("❌ Test FAILED")
        print(f"Error: {result.get('error')}")
    
    return result.get("success", False)


def test_combined_workflow():
    """Test combined generation + analysis."""
    print_section("TEST 3: Combined Workflow (Generate + Analyze)")
    
    agent = AdvancedToolAgent()
    request = "Generate a Python data processing script and analyze it for performance"
    
    print(f"Request: {request}\n")
    print("🤖 Processing...\n")
    
    result = agent.process_request(request)
    
    if result.get("success"):
        print("✅ Test PASSED")
        print("\nTool Calls:")
        print(f"  - Action: {result.get('action')}")
        print(f"  - Tools: generate_code → analyze_code")
        print(f"\nWorkflow completed successfully")
        
        # Show generation result
        gen_result = result.get("generation", {})
        if gen_result.get("success"):
            print("\n  ✓ Code generation: SUCCESS")
        
        # Show analysis result
        analyze_result = result.get("analysis", {})
        if analyze_result.get("success"):
            print("  ✓ Code analysis: SUCCESS")
    else:
        print("❌ Test FAILED")
        print(f"Error: {result.get('error')}")
    
    return result.get("success", False)


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  ADVANCED TOOL AGENT - QUICK TEST SUITE")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("\n❌ Error: GEMINI_API_KEY not found in environment")
        print("Please create a .env file with your API key")
        return 1
    
    print("\n✅ API key found")
    print("🚀 Starting tests...\n")
    
    results = []
    
    # Run tests
    try:
        results.append(("REST API Generation", test_rest_api_generation()))
        results.append(("Security Analysis", test_security_analysis()))
        results.append(("Combined Workflow", test_combined_workflow()))
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Print summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
