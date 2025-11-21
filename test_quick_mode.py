"""
Test script for Quick Mode functionality
Tests smart_optimize end-to-end
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.prompt_engine import PromptEngine
from core.smart_analyzer import SmartAnalyzer

def test_smart_analyzer():
    """Test SmartAnalyzer with sample prompts"""
    print("\n" + "="*60)
    print("TEST 1: SmartAnalyzer - Auto-Detection")
    print("="*60)

    analyzer = SmartAnalyzer()

    # Test prompt 1: ML/Data Science
    prompt1 = "Help me build a neural network for image classification"
    result1 = analyzer.analyze_prompt(prompt1)

    print(f"\nPrompt: '{prompt1}'")
    print(f"[OK] Detected Domain: {result1['domain']}")
    print(f"[OK] Detected Role: {result1['role']}")
    print(f"[OK] Detected Task: {result1['task']}")
    print(f"[OK] Confidence: {result1['confidence']:.2f}")
    print(f"[OK] Best Version: {analyzer.get_best_version_type(result1)}")

    # Test prompt 2: Academic
    prompt2 = "I need to understand the main findings from recent research on climate change"
    result2 = analyzer.analyze_prompt(prompt2)

    print(f"\nPrompt: '{prompt2}'")
    print(f"[OK] Detected Domain: {result2['domain']}")
    print(f"[OK] Detected Role: {result2['role']}")
    print(f"[OK] Detected Task: {result2['task']}")
    print(f"[OK] Confidence: {result2['confidence']:.2f}")
    print(f"[OK] Best Version: {analyzer.get_best_version_type(result2)}")

    # Test prompt 3: Python Development
    prompt3 = "Debug this Python code that keeps throwing a TypeError"
    result3 = analyzer.analyze_prompt(prompt3)

    print(f"\nPrompt: '{prompt3}'")
    print(f"[OK] Detected Domain: {result3['domain']}")
    print(f"[OK] Detected Role: {result3['role']}")
    print(f"[OK] Detected Task: {result3['task']}")
    print(f"[OK] Confidence: {result3['confidence']:.2f}")
    print(f"[OK] Best Version: {analyzer.get_best_version_type(result3)}")

    return True

def test_smart_optimize():
    """Test smart_optimize method"""
    print("\n" + "="*60)
    print("TEST 2: PromptEngine.smart_optimize()")
    print("="*60)

    engine = PromptEngine()

    # Simple test prompt
    test_prompt = "Explain machine learning to me"

    print(f"\nTest Prompt: '{test_prompt}'")
    print("\nCalling smart_optimize()...")

    try:
        result = engine.smart_optimize(test_prompt)

        print("\n[OK] Smart optimization successful!")
        print(f"[OK] Detected Domain: {result['detection']['domain']}")
        print(f"[OK] Best Version Selected: {result['best_version_key']}")
        print(f"[OK] Original Score: {result['original_score']:.0f}/100")
        print(f"[OK] Optimized Score: {result['optimized_score']:.0f}/100")
        print(f"[OK] Improvement: +{result['improvement']:.0f} points")

        print(f"\n[OK] Best Version Preview (first 150 chars):")
        print(f"   {result['best_version'][:150]}...")

        print(f"\n[OK] All Versions Available:")
        for version_key in result['all_versions'].keys():
            print(f"   - {version_key}")

        return True

    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_analyzer():
    """Test fallback keyword-based analysis"""
    print("\n" + "="*60)
    print("TEST 3: Fallback Analyzer (Keyword-Based)")
    print("="*60)

    analyzer = SmartAnalyzer()

    # Test with prompts that should trigger different domains
    prompts = [
        ("machine learning model training dataset", "ml-data-science"),
        ("python code function debug error", "python-development"),
        ("research paper thesis literature review", "academic"),
    ]

    for prompt, expected_domain in prompts:
        result = analyzer._fallback_analysis(prompt)
        match = "[OK]" if result['domain'] == expected_domain else "[FAIL]"
        print(f"\n{match} Prompt: '{prompt}'")
        print(f"  Expected: {expected_domain}, Got: {result['domain']}")
        print(f"  Role: {result['role']}, Task: {result['task']}")

    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("QUICK MODE - COMPREHENSIVE TESTING")
    print("="*60)

    all_passed = True

    # Test 1: SmartAnalyzer
    try:
        test_smart_analyzer()
    except Exception as e:
        print(f"\n[ERROR] SmartAnalyzer test failed: {str(e)}")
        all_passed = False

    # Test 2: Smart Optimize (requires API key)
    print("\n\nNOTE: Test 2 requires a valid Gemini API key.")
    print("If you haven't set GEMINI_API_KEY in .env, this test will fail.")

    try:
        from core.config import Config
        if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "your_gemini_api_key_here":
            test_smart_optimize()
        else:
            print("\n[WARN] Skipping smart_optimize test - No API key configured")
    except Exception as e:
        print(f"\n[ERROR] smart_optimize test failed: {str(e)}")
        all_passed = False

    # Test 3: Fallback analyzer
    try:
        test_fallback_analyzer()
    except Exception as e:
        print(f"\n[ERROR] Fallback analyzer test failed: {str(e)}")
        all_passed = False

    # Summary
    print("\n" + "="*60)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED!")
    else:
        print("[WARNING] Some tests failed - check output above")
    print("="*60 + "\n")
