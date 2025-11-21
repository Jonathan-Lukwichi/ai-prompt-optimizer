"""
Comprehensive Test Suite for Phase 2 Features
Tests all Phase 2 functionality: preferences, smart defaults, batch processing,
guided builder, enhancements, and analytics
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.user_preferences import UserPreferences, get_preferences
from core.database import DatabaseManager
from core.prompt_engine import PromptEngine
from core.prompt_builder import PromptBuilder, PromptComponents
from core.prompt_enhancer import PromptEnhancer, get_enhancer
import json

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}\n")

def test_1_user_preferences():
    """Test 1: User Preferences Tracking"""
    print_section("TEST 1: User Preferences Tracking")

    try:
        # Create preferences instance
        prefs = UserPreferences()

        # Track some optimizations
        print("[OK] Tracking 5 optimization events...")
        for i in range(5):
            prefs.track_optimization(
                domain='ml-data-science',
                role='data_scientist',
                task_type='analysis',
                selected_version='critical'
            )

        # Get smart defaults
        defaults = prefs.get_smart_defaults()
        print(f"[OK] Smart defaults generated:")
        print(f"     - Domain: {defaults.get('domain')}")
        print(f"     - Role: {defaults.get('role')}")
        print(f"     - Task: {defaults.get('task_type')}")
        print(f"     - Version: {defaults.get('version')}")

        # Validate
        assert defaults.get('domain') == 'ml-data-science', "Domain should be ml-data-science"
        assert defaults.get('role') == 'data_scientist', "Role should be data_scientist"
        assert defaults.get('task_type') == 'analysis', "Task should be analysis"
        assert defaults.get('version') == 'critical', "Version should be critical"

        # Get usage stats
        stats = prefs.get_usage_stats()
        print(f"\n[OK] Usage stats:")
        print(f"     - Total optimizations: {stats.get('total_optimizations')}")
        print(f"     - Preferred version: {stats.get('preferred_version')}")

        assert stats.get('total_optimizations') == 5, "Should have 5 optimizations"

        # Test export/import
        exported = prefs.export_preferences()
        print(f"\n[OK] Exported preferences ({len(exported)} chars)")

        new_prefs = UserPreferences()
        new_prefs.import_preferences(exported)
        new_stats = new_prefs.get_usage_stats()

        assert new_stats.get('total_optimizations') == 5, "Import should preserve count"
        print("[OK] Import/export working correctly")

        print("\n[SUCCESS] User Preferences tests passed!")
        return True

    except Exception as e:
        print(f"\n[ERROR] User Preferences test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_2_database_persistence():
    """Test 2: Database Preference Persistence"""
    print_section("TEST 2: Database Preference Persistence")

    try:
        # Create preferences and track data
        prefs = UserPreferences()

        print("[OK] Tracking test data...")
        for i in range(3):
            prefs.track_optimization(
                domain='academic',
                role='phd',
                task_type='research'
            )

        # Save to database
        print("[OK] Saving to database...")
        DatabaseManager.save_preferences(prefs, session_key="test_phase2")

        # Load from database
        print("[OK] Loading from database...")
        loaded_data = DatabaseManager.load_preferences(session_key="test_phase2")

        assert loaded_data is not None, "Should load saved preferences"
        assert loaded_data.get('total_optimizations') == 3, "Should have 3 optimizations"

        print(f"[OK] Loaded data:")
        print(f"     - Total optimizations: {loaded_data.get('total_optimizations')}")
        print(f"     - Preferred domain: {loaded_data.get('preferred_domain')}")
        print(f"     - Preferred role: {loaded_data.get('preferred_role')}")

        assert loaded_data.get('preferred_domain') == 'academic', "Domain should persist"
        assert loaded_data.get('preferred_role') == 'phd', "Role should persist"

        print("\n[SUCCESS] Database persistence tests passed!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Database persistence test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_3_smart_optimize():
    """Test 3: Smart Optimize (Quick Mode)"""
    print_section("TEST 3: Smart Optimize (Quick Mode)")

    try:
        engine = PromptEngine()

        test_prompts = [
            "Help me learn about neural networks",
            "Debug my Python sorting function",
            "Write a research question about climate change"
        ]

        print(f"[OK] Testing smart_optimize on {len(test_prompts)} prompts...")

        for idx, prompt in enumerate(test_prompts, 1):
            print(f"\n[OK] Prompt {idx}: {prompt[:50]}...")

            result = engine.smart_optimize(prompt)

            # Validate result structure
            assert 'detection' in result, "Should have detection"
            assert 'optimized' in result, "Should have optimized versions"
            assert 'best_version' in result, "Should have best version"
            assert 'improvement' in result, "Should have improvement score"

            print(f"     - Detected domain: {result['detection']['domain']}")
            print(f"     - Detected role: {result['detection']['role']}")
            print(f"     - Detected task: {result['detection']['task']}")
            print(f"     - Best version: {result['best_version_key']}")
            print(f"     - Improvement: +{result['improvement']:.1f} points")

            assert result['improvement'] > 0, "Should show improvement"
            assert result['best_version_key'] in ['basic', 'critical', 'tutor', 'safe'], "Valid version"

        print("\n[SUCCESS] Smart optimize tests passed!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Smart optimize test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_4_batch_optimize():
    """Test 4: Batch Optimize Functionality"""
    print_section("TEST 4: Batch Optimize Functionality")

    try:
        engine = PromptEngine()
        prefs = get_preferences()

        # Simulate batch input
        batch_input = """Explain machine learning algorithms
---
Help me write a sorting function
---
Create a literature review outline"""

        # Parse prompts
        raw_prompts = batch_input.replace('\r\n', '\n').split('---')
        prompts = [p.strip() for p in raw_prompts if p.strip() and len(p.strip()) > 5]

        print(f"[OK] Parsed {len(prompts)} prompts from batch input")
        assert len(prompts) == 3, "Should parse 3 prompts"

        # Process batch
        results = []
        print(f"\n[OK] Processing batch of {len(prompts)} prompts...")

        for idx, prompt in enumerate(prompts, 1):
            print(f"     Processing {idx}/{len(prompts)}: {prompt[:30]}...")

            result = engine.smart_optimize(prompt)

            # Track preferences
            prefs.track_optimization(
                domain=result['detection']['domain'],
                role=result['detection']['role'],
                task_type=result['detection']['task']
            )

            results.append({
                'index': idx,
                'original': prompt,
                'optimized': result['best_version'],
                'improvement': result['improvement'],
                'version_type': result['best_version_key']
            })

            print(f"       [OK] +{result['improvement']:.0f} points")

        # Validate results
        assert len(results) == 3, "Should have 3 results"

        successful = [r for r in results if 'error' not in r]
        avg_improvement = sum(r['improvement'] for r in successful) / len(successful)

        print(f"\n[OK] Batch processing complete:")
        print(f"     - Successful: {len(successful)}/{len(results)}")
        print(f"     - Average improvement: +{avg_improvement:.1f} points")

        # Test export formats
        print("\n[OK] Testing export formats...")

        # JSON
        json_data = json.dumps(results, indent=2)
        assert len(json_data) > 0, "JSON export should work"
        print(f"     - JSON: {len(json_data)} chars")

        # TXT
        all_optimized = "\n\n---\n\n".join([r['optimized'] for r in results])
        assert len(all_optimized) > 0, "TXT export should work"
        print(f"     - TXT: {len(all_optimized)} chars")

        print("\n[SUCCESS] Batch optimize tests passed!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Batch optimize test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_5_guided_prompt_builder():
    """Test 5: Guided Prompt Builder"""
    print_section("TEST 5: Guided Prompt Builder")

    try:
        builder = PromptBuilder()

        # Test 6-Step Framework
        print("[OK] Testing 6-Step Framework...")
        components = PromptComponents(
            role="Data Scientist",
            context="Analyzing customer churn data for SaaS company",
            task="Build a prediction model to identify at-risk customers",
            format="Python code with comments and explanations",
            rules="Use scikit-learn, focus on interpretability",
            examples="Similar to RFM analysis but with behavioral features"
        )

        prompt_6step = builder.build_from_6_step(components)
        print(f"[OK] 6-Step prompt generated ({len(prompt_6step)} chars)")

        assert "Data Scientist" in prompt_6step, "Should include role"
        assert "churn" in prompt_6step.lower(), "Should include context"
        assert len(prompt_6step) > 100, "Should be comprehensive"

        # Test CRAFT Formula
        print("\n[OK] Testing CRAFT Formula...")
        components_craft = PromptComponents(
            craft_context="Academic research project on climate change",
            craft_role="Environmental Scientist",
            craft_action="Analyze temperature trends and create visualizations",
            craft_format="Python script with matplotlib",
            craft_thinking_mode="Step-by-step analytical approach"
        )

        prompt_craft = builder.build_from_craft(components_craft)
        print(f"[OK] CRAFT prompt generated ({len(prompt_craft)} chars)")

        assert "Environmental Scientist" in prompt_craft, "Should include role"
        assert "climate" in prompt_craft.lower(), "Should include context"
        assert "visualizations" in prompt_craft.lower(), "Should include action"

        # Test quality validation
        print("\n[OK] Testing quality validation...")
        validation = builder.validate_prompt(prompt_6step)

        assert 'score' in validation, "Should have score"
        assert 'strengths' in validation, "Should have strengths"
        assert 'weaknesses' in validation, "Should have weaknesses"

        print(f"[OK] Validation score: {validation['score']}/100")
        print(f"[OK] Strengths: {len(validation['strengths'])} identified")
        print(f"[OK] Weaknesses: {len(validation['weaknesses'])} identified")

        assert validation['score'] >= 0 and validation['score'] <= 100, "Valid score range"

        print("\n[SUCCESS] Guided prompt builder tests passed!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Guided prompt builder test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_6_prompt_enhancements():
    """Test 6: Prompt Enhancement Features"""
    print_section("TEST 6: Prompt Enhancement Features")

    try:
        enhancer = get_enhancer()

        test_prompt = "Write a function to sort numbers"

        # Test Quick Enhance
        print("[OK] Testing Quick Enhance...")
        enhancement = enhancer.quick_enhance(test_prompt)

        assert enhancement.enhanced, "Should have enhanced prompt"
        assert enhancement.score_before > 0, "Should have before score"
        assert enhancement.score_after > enhancement.score_before, "Should improve"
        assert len(enhancement.changes) > 0, "Should have changes list"

        improvement = enhancement.score_after - enhancement.score_before

        print(f"[OK] Quick Enhance result:")
        print(f"     - Before: {enhancement.score_before}/100")
        print(f"     - After: {enhancement.score_after}/100")
        print(f"     - Improvement: +{improvement} points")
        print(f"     - Changes: {len(enhancement.changes)} improvements")

        # Test Iterative Refinement (Stage 1 only)
        print("\n[OK] Testing Iterative Refinement (Stage 1)...")
        refinement = enhancer.start_iterative_refinement(test_prompt)

        assert refinement.stage_number == 1, "Should start at stage 1"
        assert refinement.prompt, "Should have current prompt"
        assert len(refinement.questions) > 0, "Should have questions"

        print(f"[OK] Iterative Refinement started:")
        print(f"     - Stage: {refinement.stage_number}/5")
        print(f"     - Questions: {len(refinement.questions)}")
        print(f"     - Current score: {refinement.score}/100")

        for i, q in enumerate(refinement.questions[:2], 1):
            print(f"       Q{i}: {q[:60]}...")

        print("\n[SUCCESS] Prompt enhancement tests passed!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Prompt enhancement test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_7_integration():
    """Test 7: Integration - Full Workflow"""
    print_section("TEST 7: Integration - Full Workflow")

    try:
        print("[OK] Simulating complete user workflow...\n")

        # Step 1: User preferences initialized
        print("Step 1: Initialize user preferences")
        prefs = get_preferences()
        print("  [OK] Preferences loaded")

        # Step 2: User optimizes a prompt (Quick Mode)
        print("\nStep 2: Optimize prompt with Quick Mode")
        engine = PromptEngine()
        result = engine.smart_optimize("Explain quantum computing to beginners")
        print(f"  [OK] Optimized: +{result['improvement']:.1f} points")

        # Step 3: Track optimization
        print("\nStep 3: Track optimization in preferences")
        prefs.track_optimization(
            domain=result['detection']['domain'],
            role=result['detection']['role'],
            task_type=result['detection']['task'],
            selected_version=result['best_version_key']
        )
        print("  [OK] Tracking successful")

        # Step 4: Save to database
        print("\nStep 4: Save preferences to database")
        DatabaseManager.save_preferences(prefs, session_key="integration_test")
        print("  [OK] Saved to database")

        # Step 5: Load preferences (simulating next session)
        print("\nStep 5: Load preferences (next session)")
        loaded = DatabaseManager.load_preferences(session_key="integration_test")
        assert loaded is not None, "Should load preferences"
        print("  [OK] Preferences loaded")

        # Step 6: Get smart defaults
        print("\nStep 6: Get smart defaults")
        new_prefs = get_preferences()
        new_prefs.import_preferences(json.dumps(loaded))
        defaults = new_prefs.get_smart_defaults()
        print(f"  [OK] Smart defaults:")
        print(f"       - Domain: {defaults.get('domain', 'N/A')}")
        print(f"       - Role: {defaults.get('role', 'N/A')}")

        # Step 7: Use guided builder
        print("\nStep 7: Build prompt with guided builder")
        builder = PromptBuilder()
        components = PromptComponents(
            role="Teacher",
            task="Explain quantum computing",
            format="Simple explanation with examples"
        )
        built_prompt = builder.build_from_6_step(components)
        assert len(built_prompt) > 50, "Should build comprehensive prompt"
        print(f"  [OK] Prompt built ({len(built_prompt)} chars)")

        # Step 8: Enhance with Quick Enhance
        print("\nStep 8: Enhance with Quick Enhance")
        enhancer = get_enhancer()
        enhancement = enhancer.quick_enhance("Write a sorting algorithm")
        improvement = enhancement.score_after - enhancement.score_before
        assert improvement > 0, "Should improve prompt"
        print(f"  [OK] Enhanced: +{improvement} points")

        print("\n[SUCCESS] Integration workflow tests passed!")
        print("All Phase 2 components work together correctly!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all Phase 2 tests"""
    print("\n" + "="*70)
    print("PHASE 2 - COMPREHENSIVE TEST SUITE")
    print("Testing all Phase 2 features end-to-end")
    print("="*70)

    results = []

    # Run all tests
    results.append(("User Preferences", test_1_user_preferences()))
    results.append(("Database Persistence", test_2_database_persistence()))
    results.append(("Smart Optimize", test_3_smart_optimize()))
    results.append(("Batch Optimize", test_4_batch_optimize()))
    results.append(("Guided Prompt Builder", test_5_guided_prompt_builder()))
    results.append(("Prompt Enhancements", test_6_prompt_enhancements()))
    results.append(("Integration Workflow", test_7_integration()))

    # Summary
    print_section("TEST SUMMARY")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    print(f"\n{'='*70}")
    if passed == total:
        print(f"[SUCCESS] ALL {total} TESTS PASSED!")
        print("\nPhase 2 is fully functional and ready for production!")
        print("\nFeatures tested:")
        print("  - User preference tracking and smart defaults")
        print("  - Database persistence and loading")
        print("  - Quick Mode (smart_optimize)")
        print("  - Batch optimization processing")
        print("  - Guided prompt builder (6-Step + CRAFT)")
        print("  - Quick Enhance and Iterative Refinement")
        print("  - Full integration workflow")
    else:
        print(f"[WARNING] {passed}/{total} tests passed")
        print(f"{total - passed} test(s) failed - check output above")
    print("="*70 + "\n")

    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
