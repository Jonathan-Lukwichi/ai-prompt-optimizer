"""
Setup Verification Script
Run this to check if everything is configured correctly
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'streamlit',
        'openai',
        'sqlalchemy',
        'dotenv',
        'plotly'
    ]

    missing = []
    for package in required:
        try:
            __import__(package if package != 'dotenv' else 'dotenv')
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} NOT installed")
            missing.append(package)

    return len(missing) == 0, missing

def check_env_file():
    """Check if .env file exists and has API key"""
    env_path = Path('.env')

    if not env_path.exists():
        print("✗ .env file NOT found")
        print("  → Copy .env.example to .env and add your API key")
        return False

    print("✓ .env file found")

    # Check if API key is set
    with open(env_path) as f:
        content = f.read()
        if 'OPENAI_API_KEY=your' in content or 'OPENAI_API_KEY=' not in content:
            print("⚠ OPENAI_API_KEY not set in .env")
            print("  → Edit .env and add your OpenAI API key")
            return False
        else:
            print("✓ OPENAI_API_KEY appears to be set")

    return True

def check_directory_structure():
    """Check if all required directories exist"""
    required_dirs = [
        '.streamlit',
        'core',
        'utils',
        'pages',
        'data'
    ]

    all_exist = True
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"✗ {dir_name}/ directory MISSING")
            all_exist = False

    return all_exist

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        '.streamlit/config.toml',
        '.streamlit/style.css',
        'core/config.py',
        'core/database.py',
        'core/prompt_engine.py',
        'utils/ui_components.py'
    ]

    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} MISSING")
            all_exist = False

    return all_exist

def main():
    """Main verification"""
    print("=" * 50)
    print("AI PROMPT OPTIMIZER - Setup Verification")
    print("=" * 50)
    print()

    print("[1/5] Checking Python version...")
    python_ok = check_python_version()
    print()

    print("[2/5] Checking dependencies...")
    deps_ok, missing = check_dependencies()
    print()

    print("[3/5] Checking .env configuration...")
    env_ok = check_env_file()
    print()

    print("[4/5] Checking directory structure...")
    dirs_ok = check_directory_structure()
    print()

    print("[5/5] Checking required files...")
    files_ok = check_required_files()
    print()

    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)

    if python_ok and deps_ok and env_ok and dirs_ok and files_ok:
        print("✓ ALL CHECKS PASSED!")
        print()
        print("You're ready to run the app:")
        print("  streamlit run app.py")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print()

        if not deps_ok:
            print("To install dependencies:")
            print("  pip install -r requirements.txt")
            print()

        if not env_ok:
            print("To configure .env:")
            print("  1. Copy .env.example to .env")
            print("  2. Edit .env and add your OPENAI_API_KEY")
            print()

        print("See QUICKSTART.md for detailed instructions")
        return 1

if __name__ == '__main__':
    exit(main())
