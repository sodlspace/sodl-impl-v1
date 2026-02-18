#!/usr/bin/env python
"""
Setup Verification Script for AdvancedTodoApp
Checks if the environment is correctly set up to run the application.
"""
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_python_version():
    """Check if Python version is 3.12 or higher"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 12:
        print("✅ Python version is compatible (3.12+)")
        return True
    else:
        print("❌ Python 3.12 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}")
        return False


def check_packages():
    """Check if required packages are installed"""
    print_header("Checking Required Packages")
    
    required_packages = {
        "fastapi": "FastAPI web framework",
        "uvicorn": "ASGI server",
        "jinja2": "Template engine",
        "pydantic": "Data validation",
        "pytest": "Testing framework",
        "httpx": "HTTP client for tests",
        "requests": "HTTP client for examples"
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"❌ {package:15} - {description} (NOT INSTALLED)")
            all_installed = False
    
    if not all_installed:
        print("\n⚠️  Some packages are missing!")
        print("   Run: pip install -r requirements.txt")
    
    return all_installed


def check_directory_structure():
    """Check if the required directories and files exist"""
    print_header("Checking Directory Structure")
    
    base_dir = Path(__file__).parent
    
    required_paths = {
        "app": "Application directory",
        "app/main.py": "Main application file",
        "app/api.py": "API endpoints",
        "app/storage.py": "Storage module",
        "app/templates": "Templates directory",
        "app/templates/base.html": "Base template",
        "app/templates/index.html": "Index template",
        "app/static": "Static files directory",
        "app/static/css/style.css": "CSS stylesheet",
        "app/static/js/app.js": "JavaScript file",
        "app/tests": "Tests directory",
        "requirements.txt": "Dependencies file",
        "run_app.py": "Quick start script"
    }
    
    all_exist = True
    for path, description in required_paths.items():
        full_path = base_dir / path
        if full_path.exists():
            print(f"✅ {path:30} - {description}")
        else:
            print(f"❌ {path:30} - {description} (NOT FOUND)")
            all_exist = False
    
    return all_exist


def check_imports():
    """Try importing the application modules"""
    print_header("Checking Application Imports")
    
    modules = [
        ("app.storage", "Storage module"),
        ("app.api", "API module"),
        ("app.main", "Main application")
    ]
    
    all_imported = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name:20} - {description}")
        except Exception as e:
            print(f"❌ {module_name:20} - {description}")
            print(f"   Error: {str(e)}")
            all_imported = False
    
    return all_imported


def check_port_availability():
    """Check if default port 8000 is available"""
    print_header("Checking Port Availability")
    
    import socket
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print("⚠️  Port 8000 is currently in use")
            print("   The app might already be running, or another service is using this port")
            print("   You can use a different port with: uvicorn app.main:app --port 8001")
            return False
        else:
            print("✅ Port 8000 is available")
            return True
    except Exception as e:
        print(f"⚠️  Could not check port availability: {e}")
        return True


def main():
    """Run all verification checks"""
    print("\n" + "🔍 AdvancedTodoApp Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_packages),
        ("Directory Structure", check_directory_structure),
        ("Application Imports", check_imports),
        ("Port Availability", check_port_availability)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Verification Summary")
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} - {name}")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✨ All checks passed! You're ready to run the app.")
        print("\nNext steps:")
        print("  1. Start the app:    python run_app.py")
        print("  2. Open browser:     http://localhost:8000")
        print("  3. View API docs:    http://localhost:8000/docs")
        print("  4. Run tests:        pytest")
        print("  5. Try the demo:     python examples/api_demo.py")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Check Python version: python --version")
        print("  • Verify you're in the project root directory")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
