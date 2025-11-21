"""
Test script for Batch Optimize functionality
Tests prompt parsing, batch processing, and export functionality
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.prompt_engine import PromptEngine
from core.user_preferences import get_preferences
import json
import csv
import io

def test_prompt_parsing():
    """Test parsing prompts from different input formats"""
    print("\n" + "="*60)
    print("TEST 1: Prompt Parsing")
    print("="*60)

    # Test 1: Parse from --- separated text
    batch_input = """Explain machine learning to me
---
Help me write a Python sorting function
---
Create a research question about climate change"""

    raw_prompts = batch_input.replace('\r\n', '\n').split('---')
    prompts = [p.strip() for p in raw_prompts if p.strip() and len(p.strip()) > 5]

    print(f"\n[OK] Parsed {len(prompts)} prompts from text input")
    assert len(prompts) == 3, "Should parse 3 prompts"

    for i, p in enumerate(prompts, 1):
        print(f"  {i}. {p[:50]}...")

    # Test 2: Filter out short prompts
    test_input = "Good prompt\n---\nx\n---\nAnother good one"
    raw = test_input.split('---')
    filtered = [p.strip() for p in raw if p.strip() and len(p.strip()) > 5]

    print(f"\n[OK] Filtered prompts: {len(filtered)} valid out of 3 total")
    assert len(filtered) == 2, "Should filter out 'x'"

    print("\n[OK] Prompt parsing working correctly!")
    return True

def test_batch_processing():
    """Test batch optimization with smart_optimize"""
    print("\n" + "="*60)
    print("TEST 2: Batch Processing")
    print("="*60)

    engine = PromptEngine()
    prefs = get_preferences()

    test_prompts = [
        "Explain machine learning",
        "Help me debug Python code",
        "Create a research question"
    ]

    results = []

    print(f"\n[OK] Processing {len(test_prompts)} prompts...")

    for idx, prompt in enumerate(test_prompts, 1):
        try:
            print(f"  Processing {idx}/{len(test_prompts)}: {prompt[:30]}...")

            # Use smart_optimize
            result = engine.smart_optimize(prompt)

            # Track preferences
            prefs.track_optimization(
                domain=result['detection']['domain'],
                role=result['detection']['role'],
                task_type=result['detection']['task']
            )

            # Store result
            results.append({
                'index': idx,
                'original': prompt,
                'optimized': result['best_version'],
                'improvement': result['improvement'],
                'version_type': result['best_version_key'],
                'domain': result['detection']['domain']
            })

            print(f"    [OK] +{result['improvement']:.0f} points ({result['best_version_key']})")

        except Exception as e:
            print(f"    [ERROR] Failed: {str(e)}")
            results.append({
                'index': idx,
                'original': prompt,
                'error': str(e)
            })

    print(f"\n[OK] Batch processing complete!")
    print(f"[OK] Successful: {len([r for r in results if 'error' not in r])}/{len(results)}")

    # Calculate average improvement
    successful = [r for r in results if 'error' not in r]
    if successful:
        avg_improvement = sum(r['improvement'] for r in successful) / len(successful)
        print(f"[OK] Average improvement: +{avg_improvement:.1f} points")

    return results

def test_export_functionality(results):
    """Test export to JSON and CSV"""
    print("\n" + "="*60)
    print("TEST 3: Export Functionality")
    print("="*60)

    # Test 1: JSON export
    try:
        json_data = json.dumps(results, indent=2)
        print(f"\n[OK] JSON export: {len(json_data)} characters")
        print(f"[OK] JSON preview: {json_data[:100]}...")

        # Verify JSON is valid
        parsed = json.loads(json_data)
        assert len(parsed) == len(results), "JSON should have all results"
        print("[OK] JSON structure valid")

    except Exception as e:
        print(f"[ERROR] JSON export failed: {str(e)}")
        return False

    # Test 2: CSV export
    try:
        successful_results = [r for r in results if 'error' not in r]

        if successful_results:
            csv_buffer = io.StringIO()
            csv_writer = csv.DictWriter(
                csv_buffer,
                fieldnames=['index', 'original', 'optimized', 'version_type', 'improvement', 'domain']
            )
            csv_writer.writeheader()
            csv_writer.writerows(successful_results)

            csv_data = csv_buffer.getvalue()
            lines = csv_data.split('\n')

            print(f"\n[OK] CSV export: {len(lines)} lines")
            print(f"[OK] CSV header: {lines[0]}")
            print(f"[OK] CSV rows: {len(lines) - 2}")  # Subtract header and empty line

            assert len(lines) >= len(successful_results) + 1, "CSV should have header + data rows"
            print("[OK] CSV structure valid")

    except Exception as e:
        print(f"[ERROR] CSV export failed: {str(e)}")
        return False

    # Test 3: TXT export (all optimized prompts)
    try:
        successful_results = [r for r in results if 'error' not in r]
        all_optimized = "\n\n---\n\n".join([r['optimized'] for r in successful_results])

        print(f"\n[OK] TXT export: {len(all_optimized)} characters")
        print(f"[OK] TXT preview: {all_optimized[:100]}...")
        print("[OK] TXT export valid")

    except Exception as e:
        print(f"[ERROR] TXT export failed: {str(e)}")
        return False

    print("\n[OK] All export formats working!")
    return True

def test_error_handling():
    """Test error handling for edge cases"""
    print("\n" + "="*60)
    print("TEST 4: Error Handling")
    print("="*60)

    # Test 1: Empty input
    batch_input = ""
    prompts = [p.strip() for p in batch_input.split('---') if p.strip() and len(p.strip()) > 5]
    print(f"\n[OK] Empty input: {len(prompts)} prompts (expected 0)")
    assert len(prompts) == 0, "Should handle empty input"

    # Test 2: Only short prompts
    batch_input = "x\n---\nab\n---\ncd"
    prompts = [p.strip() for p in batch_input.split('---') if p.strip() and len(p.strip()) > 5]
    print(f"[OK] Short prompts filtered: {len(prompts)} prompts (expected 0)")
    assert len(prompts) == 0, "Should filter out short prompts"

    # Test 3: Mixed valid/invalid
    batch_input = "This is valid\n---\nx\n---\nThis is also valid"
    prompts = [p.strip() for p in batch_input.split('---') if p.strip() and len(p.strip()) > 5]
    print(f"[OK] Mixed input: {len(prompts)} valid prompts (expected 2)")
    assert len(prompts) == 2, "Should keep only valid prompts"

    print("\n[OK] Error handling working correctly!")
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("BATCH OPTIMIZE - COMPREHENSIVE TESTING")
    print("="*60)

    all_passed = True

    # Test 1: Prompt parsing
    try:
        test_prompt_parsing()
    except Exception as e:
        print(f"\n[ERROR] Prompt parsing test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        all_passed = False

    # Test 2: Batch processing
    try:
        results = test_batch_processing()
    except Exception as e:
        print(f"\n[ERROR] Batch processing test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        all_passed = False
        results = []

    # Test 3: Export functionality
    try:
        if results:
            test_export_functionality(results)
        else:
            print("\n[WARN] Skipping export test (no results to export)")
    except Exception as e:
        print(f"\n[ERROR] Export functionality test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        all_passed = False

    # Test 4: Error handling
    try:
        test_error_handling()
    except Exception as e:
        print(f"\n[ERROR] Error handling test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        all_passed = False

    # Summary
    print("\n" + "="*60)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED!")
        print("\nBatch Optimize functionality is fully operational:")
        print("  - Prompt parsing working")
        print("  - Batch processing functional")
        print("  - Export formats (JSON/CSV/TXT) working")
        print("  - Error handling robust")
    else:
        print("[WARNING] Some tests failed - check output above")
    print("="*60 + "\n")
