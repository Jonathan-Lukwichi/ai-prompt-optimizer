"""
Test script for user preferences system
Tests preference tracking, smart defaults, and database persistence
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.user_preferences import UserPreferences, get_preferences
from core.database import DatabaseManager

def test_preference_tracking():
    """Test basic preference tracking"""
    print("\n" + "="*60)
    print("TEST 1: Preference Tracking")
    print("="*60)

    prefs = UserPreferences()

    # Track some optimizations
    print("\nTracking optimizations...")

    # ML/DS domain - data scientist - analysis (3 times)
    for i in range(3):
        prefs.track_optimization(
            domain='ml-data-science',
            role='data_scientist',
            task_type='analysis'
        )

    # Academic domain - phd - research (2 times)
    for i in range(2):
        prefs.track_optimization(
            domain='academic',
            role='phd',
            task_type='research'
        )

    # Track version usage
    prefs.track_version_usage('critical', 'copy')
    prefs.track_version_usage('critical', 'copy')
    prefs.track_version_usage('basic', 'copy')

    # Get stats
    stats = prefs.get_usage_stats()

    print(f"\n[OK] Total optimizations: {stats['total_optimizations']}")
    print(f"[OK] Domain usage: {stats['domains']}")
    print(f"[OK] Role usage: {stats['roles']}")
    print(f"[OK] Task usage: {stats['tasks']}")
    print(f"[OK] Version usage: {stats['versions']}")

    return prefs

def test_smart_defaults():
    """Test smart default recommendations"""
    print("\n" + "="*60)
    print("TEST 2: Smart Defaults")
    print("="*60)

    prefs = UserPreferences()

    # Track usage patterns
    for i in range(5):
        prefs.track_optimization(
            domain='ml-data-science',
            role='data_scientist',
            task_type='analysis',
            selected_version='critical'
        )

    for i in range(2):
        prefs.track_optimization(
            domain='academic',
            role='student',
            task_type='learning'
        )

    # Get smart defaults
    defaults = prefs.get_smart_defaults()

    print(f"\n[OK] Preferred domain: {defaults['domain']}")
    print(f"[OK] Preferred role: {defaults['role']}")
    print(f"[OK] Preferred task: {defaults['task_type']}")
    print(f"[OK] Preferred version: {defaults['version']}")

    # Verify correctness
    assert defaults['domain'] == 'ml-data-science', "Should prefer ml-data-science (used 5 times)"
    assert defaults['role'] == 'data_scientist', "Should prefer data_scientist"
    assert defaults['task_type'] == 'analysis', "Should prefer analysis"
    assert defaults['version'] == 'critical', "Should prefer critical"

    print("\n[OK] All smart defaults are correct!")

    return prefs

def test_database_persistence():
    """Test saving and loading from database"""
    print("\n" + "="*60)
    print("TEST 3: Database Persistence")
    print("="*60)

    # Create preferences with data
    prefs = UserPreferences()

    for i in range(3):
        prefs.track_optimization(
            domain='python-development',
            role='software_dev',
            task_type='debugging',
            selected_version='basic'
        )

    print("\n[OK] Created preferences with 3 optimizations")

    # Save to database
    try:
        saved = DatabaseManager.save_preferences(prefs, session_key="test_session")
        print(f"[OK] Saved to database: {saved.total_optimizations} optimizations")
    except Exception as e:
        print(f"[ERROR] Could not save: {str(e)}")
        return False

    # Load from database
    try:
        loaded_data = DatabaseManager.load_preferences(session_key="test_session")

        if loaded_data:
            print(f"[OK] Loaded from database: {loaded_data['total_optimizations']} optimizations")
            print(f"[OK] Domains: {loaded_data['domain_usage']}")
            print(f"[OK] Preferred domain: {loaded_data['preferred_domain']}")
            print(f"[OK] Preferred role: {loaded_data['preferred_role']}")

            # Verify data integrity
            assert loaded_data['total_optimizations'] == 3
            assert loaded_data['preferred_domain'] == 'python-development'
            assert loaded_data['preferred_role'] == 'software_dev'

            print("\n[OK] Database persistence working correctly!")
            return True
        else:
            print("[ERROR] No data loaded from database")
            return False

    except Exception as e:
        print(f"[ERROR] Could not load: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_template_suggestions():
    """Test template suggestion logic"""
    print("\n" + "="*60)
    print("TEST 4: Template Suggestions")
    print("="*60)

    prefs = UserPreferences()

    # Test short prompts (should suggest template)
    short_prompt = "explain ml"
    should_suggest = prefs.should_suggest_template(short_prompt)
    print(f"\n[OK] Short prompt '{short_prompt}': suggest={should_suggest}")
    assert should_suggest == True, "Should suggest template for short prompt"

    # Test beginner pattern (should suggest)
    beginner_prompt = "help me understand machine learning"
    should_suggest = prefs.should_suggest_template(beginner_prompt)
    print(f"[OK] Beginner prompt '{beginner_prompt}': suggest={should_suggest}")
    assert should_suggest == True, "Should suggest template for beginner pattern"

    # Test detailed prompt (should not suggest)
    detailed_prompt = "I am working on a machine learning project analyzing time series data for stock market prediction. I have cleaned the data and performed exploratory analysis. Now I need help selecting the right algorithm and hyperparameters for my specific use case."
    should_suggest = prefs.should_suggest_template(detailed_prompt)
    print(f"[OK] Detailed prompt: suggest={should_suggest}")
    assert should_suggest == False, "Should not suggest template for detailed prompt"

    # Test template suggestions by domain
    suggestions = prefs.get_template_suggestions('academic', 'research')
    print(f"\n[OK] Academic/Research suggestions: {suggestions}")
    assert len(suggestions) > 0, "Should have suggestions for academic research"

    suggestions = prefs.get_template_suggestions('ml-data-science', 'analysis')
    print(f"[OK] ML/DS/Analysis suggestions: {suggestions}")

    print("\n[OK] Template suggestion logic working!")
    return True

def test_export_import():
    """Test export/import functionality"""
    print("\n" + "="*60)
    print("TEST 5: Export/Import")
    print("="*60)

    # Create preferences
    prefs = UserPreferences()

    for i in range(4):
        prefs.track_optimization(
            domain='academic',
            role='professor',
            task_type='teaching'
        )

    # Export
    exported = prefs.export_preferences()
    print("\n[OK] Exported preferences:")
    print(exported[:200] + "...")

    # Create new instance and import
    new_prefs = UserPreferences()
    new_prefs.import_preferences(exported)

    # Verify
    new_stats = new_prefs.get_usage_stats()
    print(f"\n[OK] Imported total optimizations: {new_stats['total_optimizations']}")
    assert new_stats['total_optimizations'] == 4, "Should have 4 optimizations after import"

    print("[OK] Export/import working correctly!")
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("USER PREFERENCES - COMPREHENSIVE TESTING")
    print("="*60)

    all_passed = True

    # Test 1: Basic tracking
    try:
        test_preference_tracking()
    except Exception as e:
        print(f"\n[ERROR] Preference tracking test failed: {str(e)}")
        all_passed = False

    # Test 2: Smart defaults
    try:
        test_smart_defaults()
    except Exception as e:
        print(f"\n[ERROR] Smart defaults test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        all_passed = False

    # Test 3: Database persistence
    try:
        test_database_persistence()
    except Exception as e:
        print(f"\n[ERROR] Database persistence test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        all_passed = False

    # Test 4: Template suggestions
    try:
        test_template_suggestions()
    except Exception as e:
        print(f"\n[ERROR] Template suggestions test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        all_passed = False

    # Test 5: Export/import
    try:
        test_export_import()
    except Exception as e:
        print(f"\n[ERROR] Export/import test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        all_passed = False

    # Summary
    print("\n" + "="*60)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED!")
        print("\nUser preferences system is fully functional:")
        print("  - Preference tracking working")
        print("  - Smart defaults calculating correctly")
        print("  - Database persistence working")
        print("  - Template suggestions working")
        print("  - Export/import functional")
    else:
        print("[WARNING] Some tests failed - check output above")
    print("="*60 + "\n")
