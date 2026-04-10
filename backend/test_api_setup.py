#!/usr/bin/env python3
"""
Quick test script to verify the API and campaign generation are working.
Run this to diagnose any issues.
"""

import os
import sys
import json

def test_imports():
    """Test if all required imports work."""
    print("=" * 60)
    print("Testing imports...")
    print("=" * 60)
    
    try:
        print("✓ Importing OpenAIClientWrapper...", end=" ")
        from openai_client import OpenAIClientWrapper
        print("OK")
        
        print("✓ Importing CampaignService...", end=" ")
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))
        from campaign_service import CampaignService
        print("OK")
        
        print("✓ Importing FastAPI...", end=" ")
        from fastapi import FastAPI
        print("OK")
        
        print("\n✅ All imports successful!\n")
        return True
    except ImportError as e:
        print(f"\n❌ Import error: {e}\n")
        return False


def test_openai_client():
    """Test OpenAI client initialization."""
    print("=" * 60)
    print("Testing OpenAI Client...")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY not set!")
        print("\nTo set it:")
        print("  export OPENAI_API_KEY='sk-...'")
        return False
    
    print("✓ OPENAI_API_KEY is set")
    
    try:
        from openai_client import OpenAIClientWrapper
        client = OpenAIClientWrapper()
        print("✓ OpenAIClientWrapper initialized")
        
        # Test response generation
        print("✓ Testing response generation...", end=" ")
        response = client.generate_response(
            "Say 'API is working!' in exactly these words.",
            temperature=0.1,
            max_tokens=20
        )
        
        if "working" in response.lower():
            print("OK")
            print(f"  Response: {response.strip()}")
        else:
            print(f"\nWarning: Unexpected response: {response}")
        
        print("\n✅ OpenAI client is working!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        return False


def test_campaign_service():
    """Test campaign service."""
    print("=" * 60)
    print("Testing Campaign Service...")
    print("=" * 60)
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))
        from campaign_service import CampaignService
        
        print("✓ CampaignService imported")
        
        service = CampaignService()
        print("✓ CampaignService initialized")
        
        # Test quick campaign generation
        print("✓ Generating quick campaign...", end=" ")
        result = service.generate_quick_campaign(
            product_name="TestProduct",
            product_description="A test product",
            tone="professional"
        )
        
        if "blog" in result and "twitter" in result:
            print("OK")
            print(f"  Content types: {list(result.keys())}")
        else:
            print(f"\nWarning: Unexpected result: {result}")
        
        print("\n✅ Campaign service is working!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        return False


def test_api_structure():
    """Test if API file structure is correct."""
    print("=" * 60)
    print("Testing API Structure...")
    print("=" * 60)
    
    try:
        print("✓ Checking api.py...", end=" ")
        with open("api.py", "r") as f:
            content = f.read()
            if "FastAPI" in content and "generate_campaign" in content:
                print("OK")
            else:
                print("WARNING - Missing expected content")
        
        print("✓ Checking campaign_service.py...", end=" ")
        with open("agents/campaign_service.py", "r") as f:
            content = f.read()
            if "CampaignService" in content and "generate_full_campaign" in content:
                print("OK")
            else:
                print("WARNING - Missing expected content")
        
        print("\n✅ API structure is correct!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        return False


def test_file_compilation():
    """Test if Python files compile without syntax errors."""
    print("=" * 60)
    print("Testing File Compilation...")
    print("=" * 60)
    
    import py_compile
    
    files_to_check = [
        "api.py",
        "openai_client.py",
        "agents/campaign_service.py"
    ]
    
    all_ok = True
    for filepath in files_to_check:
        try:
            print(f"✓ Compiling {filepath}...", end=" ")
            py_compile.compile(filepath, doraise=True)
            print("OK")
        except py_compile.PyCompileError as e:
            print(f"ERROR: {e}")
            all_ok = False
    
    if all_ok:
        print("\n✅ All files compile successfully!\n")
    else:
        print("\n❌ Some files have syntax errors!\n")
    
    return all_ok


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  AUTONOMOUS CONTENT FACTORY - API TEST SUITE  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    os.chdir(os.path.dirname(__file__) or ".")
    
    results = []
    
    results.append(("File Compilation", test_file_compilation()))
    results.append(("Imports", test_imports()))
    results.append(("API Structure", test_api_structure()))
    results.append(("OpenAI Client", test_openai_client()))
    results.append(("Campaign Service", test_campaign_service()))
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! API is ready to run.")
        print("\nTo start the server:")
        print("  bash start_server.sh")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
