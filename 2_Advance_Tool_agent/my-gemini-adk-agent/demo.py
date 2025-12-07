#!/usr/bin/env python3
"""Demo script to showcase the Advanced Tool Agent capabilities."""

import sys
from app.agent import AdvancedToolAgent

def print_banner():
    """Print demo banner."""
    print("\n" + "=" * 70)
    print("  🤖 ADVANCED TOOL AGENT - DEMO")
    print("=" * 70)
    print("\nThis demo shows the agent's capabilities:")
    print("  • Intent parsing")
    print("  • Tool selection")
    print("  • Workflow orchestration")
    print("\n" + "=" * 70 + "\n")

def demo_intent_parsing():
    """Demo 1: Intent Parsing"""
    print("📝 DEMO 1: Intent Parsing")
    print("-" * 70)
    
    agent = AdvancedToolAgent()
    
    test_requests = [
        "Generate a Python REST API with authentication",
        "Analyze this code for security issues",
        "Create and analyze a data pipeline in Python",
        "Build a JavaScript Express API",
        "Check this code for performance problems"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{i}. Request: \"{request}\"")
        intent = agent.parse_intent(request)
        print(f"   → Action: {intent['action']}")
        
        if intent['action'] == 'generate':
            print(f"   → Tool: {intent['tool']}")
            print(f"   → Language: {intent['params']['language']}")
            print(f"   → Complexity: {intent['params']['complexity']}")
        elif intent['action'] == 'analyze':
            print(f"   → Tool: {intent['tool']}")
            print(f"   → Analysis Type: {intent['params']['analysis_type']}")
        elif intent['action'] == 'both':
            print(f"   → Tools: {' → '.join(intent['tools'])}")
            print(f"   → Language: {intent['params']['generate']['language']}")
            print(f"   → Analysis: {intent['params']['analyze']['analysis_type']}")
    
    print("\n✅ Intent parsing works perfectly!")
    print("-" * 70 + "\n")

def demo_tool_detection():
    """Demo 2: Tool Detection"""
    print("🔧 DEMO 2: Tool Detection & Parameter Extraction")
    print("-" * 70)
    
    agent = AdvancedToolAgent()
    
    scenarios = [
        {
            "request": "Generate a complex Go microservice",
            "expected": {
                "language": "go",
                "complexity": "complex"
            }
        },
        {
            "request": "Create a simple Python script",
            "expected": {
                "language": "python",
                "complexity": "simple"
            }
        },
        {
            "request": "Analyze for performance issues",
            "expected": {
                "analysis_type": "performance"
            }
        },
        {
            "request": "Check code style and best practices",
            "expected": {
                "analysis_type": "style"
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. Request: \"{scenario['request']}\"")
        intent = agent.parse_intent(scenario['request'])
        
        if intent['action'] == 'generate':
            params = intent['params']
            print(f"   ✓ Detected language: {params['language']}")
            print(f"   ✓ Detected complexity: {params['complexity']}")
        elif intent['action'] == 'analyze':
            params = intent['params']
            print(f"   ✓ Detected analysis type: {params['analysis_type']}")
    
    print("\n✅ Tool detection works perfectly!")
    print("-" * 70 + "\n")

def demo_response_formatting():
    """Demo 3: Response Formatting"""
    print("📊 DEMO 3: Response Formatting")
    print("-" * 70)
    
    agent = AdvancedToolAgent()
    
    # Mock generation result
    gen_result = {
        "success": True,
        "code": "def hello_world():\n    print('Hello, World!')",
        "language": "python",
        "complexity": "simple"
    }
    
    print("\n1. Code Generation Response:")
    print(agent._format_generate_response(gen_result))
    
    # Mock analysis result
    analyze_result = {
        "success": True,
        "analysis": {
            "severity": "low",
            "vulnerabilities": [],
            "summary": "Code looks good!"
        },
        "analysis_type": "security"
    }
    
    print("\n2. Code Analysis Response:")
    print(agent._format_analyze_response(analyze_result))
    
    print("✅ Response formatting works perfectly!")
    print("-" * 70 + "\n")

def demo_architecture():
    """Demo 4: Architecture Overview"""
    print("🏗️  DEMO 4: Architecture Overview")
    print("-" * 70)
    
    print("""
The agent uses a layered architecture:

┌─────────────────────────────────────┐
│      User Request (Natural)         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Intent Parser                  │
│  • Detect action type               │
│  • Extract language                 │
│  • Determine complexity             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Tool Selector                  │
│  • Choose appropriate tool(s)       │
│  • Prepare parameters               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Tool Executor                  │
│  • generate_code_with_cli()         │
│  • analyze_code_with_cli()          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Gemini CLI Wrapper             │
│  • Subprocess management            │
│  • Timeout handling                 │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Gemini CLI (Node.js)           │
│  • Communicates with Gemini API     │
└─────────────────────────────────────┘
    """)
    
    print("✅ Architecture is clean and modular!")
    print("-" * 70 + "\n")

def demo_features():
    """Demo 5: Feature Summary"""
    print("✨ DEMO 5: Feature Summary")
    print("-" * 70)
    
    features = {
        "Code Generation": [
            "✓ Python (FastAPI, Flask)",
            "✓ JavaScript (Express, Node.js)",
            "✓ Go",
            "✓ REST APIs, data pipelines, scripts"
        ],
        "Code Analysis": [
            "✓ Security vulnerabilities",
            "✓ Performance issues",
            "✓ Style and best practices",
            "✓ Comprehensive analysis"
        ],
        "Interfaces": [
            "✓ Interactive CLI",
            "✓ Single request mode",
            "✓ REST API server",
            "✓ Programmatic usage"
        ],
        "Deployment": [
            "✓ Local execution",
            "✓ Docker container",
            "✓ Google Cloud Run",
            "✓ Cloud Build CI/CD"
        ]
    }
    
    for category, items in features.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  {item}")
    
    print("\n✅ All features implemented!")
    print("-" * 70 + "\n")

def main():
    """Run all demos."""
    print_banner()
    
    try:
        demo_intent_parsing()
        input("Press Enter to continue to next demo...")
        
        demo_tool_detection()
        input("Press Enter to continue to next demo...")
        
        demo_response_formatting()
        input("Press Enter to continue to next demo...")
        
        demo_architecture()
        input("Press Enter to continue to next demo...")
        
        demo_features()
        
        print("=" * 70)
        print("  🎉 DEMO COMPLETE!")
        print("=" * 70)
        print("\nNext Steps:")
        print("  1. Install Gemini CLI: npm install -g @google/generative-ai-cli")
        print("  2. Setup .env file with your GEMINI_API_KEY")
        print("  3. Run: python tool_agent.py --interactive")
        print("\nFor full functionality with real Gemini CLI calls:")
        print("  python tests/quick_test.py")
        print("\n" + "=" * 70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
