#!/usr/bin/env python3
"""Main CLI entry point for the Advanced Tool Agent."""

import argparse
import sys
import os
from dotenv import load_dotenv
from app.agent import AdvancedToolAgent

# Load environment variables
load_dotenv()


def interactive_mode():
    """Run agent in interactive mode."""
    print("=" * 60)
    print("🤖 ADVANCED TOOL AGENT - Interactive Mode")
    print("=" * 60)
    print("\nCapabilities:")
    print("  • Generate code (REST APIs, scripts, pipelines)")
    print("  • Analyze code (security, performance, style)")
    print("  • Combined workflows (generate + analyze)")
    print("\nExamples:")
    print("  - 'Generate a Python REST API with authentication'")
    print("  - 'Analyze this code for security issues: <code>'")
    print("  - 'Create and analyze a data pipeline in Python'")
    print("\nType 'quit' or 'exit' to stop\n")
    print("=" * 60 + "\n")
    
    agent = AdvancedToolAgent()
    
    while True:
        try:
            user_input = input("💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\n🤖 Processing your request...\n")
            
            result = agent.process_request(user_input)
            
            if result.get("success"):
                print(result.get("formatted_response", ""))
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def single_request_mode(request: str):
    """Process a single request and exit."""
    print("🤖 Processing request...\n")
    
    agent = AdvancedToolAgent()
    result = agent.process_request(request)
    
    if result.get("success"):
        print(result.get("formatted_response", ""))
        return 0
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Advanced Tool Agent - Generate and analyze code using Gemini CLI"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--request",
        type=str,
        help="Process a single request and exit"
    )
    
    args = parser.parse_args()
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found in environment")
        print("Please create a .env file with your API key")
        print("Example: GEMINI_API_KEY=your_api_key_here")
        return 1
    
    if args.interactive:
        interactive_mode()
        return 0
    elif args.request:
        return single_request_mode(args.request)
    else:
        # Default to interactive mode
        interactive_mode()
        return 0


if __name__ == "__main__":
    sys.exit(main())
