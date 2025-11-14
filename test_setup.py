#!/usr/bin/env python
"""
AIRA AI Chatbot - Test Suite
Verify all components are correctly configured
"""

import os
import json
import yaml
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"  ✓ {description}: {filepath}")
        return True
    else:
        print(f"  ✗ {description}: {filepath} NOT FOUND")
        return False

def check_yaml_valid(filepath):
    """Check if YAML file is valid"""
    try:
        with open(filepath, 'r') as f:
            yaml.safe_load(f)
        print(f"  ✓ YAML valid: {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ YAML invalid: {filepath} - {str(e)}")
        return False

def check_json_valid(filepath):
    """Check if JSON file is valid"""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        print(f"  ✓ JSON valid: {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ JSON invalid: {filepath} - {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("  AIRA AI Chatbot - Pre-Deployment Verification")
    print("="*60 + "\n")
    
    results = []
    
    # Check core files
    print("[1] Checking Core Files")
    results.append(check_file_exists('app.py', 'Flask App'))
    results.append(check_file_exists('intents.json', 'College FAQs'))
    results.append(check_file_exists('requirements.txt', 'Dependencies'))
    print()
    
    # Check startup scripts
    print("[2] Checking Startup Scripts")
    results.append(check_file_exists('train_model.bat', 'Training Script'))
    results.append(check_file_exists('start_rasa.bat', 'Rasa Launcher'))
    results.append(check_file_exists('start_flask.bat', 'Flask Launcher'))
    results.append(check_file_exists('setup_windows.bat', 'Setup Helper'))
    print()
    
    # Check Rasa files
    print("[3] Checking Rasa Project Files")
    results.append(check_file_exists('rasa_minimal/domain.yml', 'Domain'))
    results.append(check_file_exists('rasa_minimal/nlu.yml', 'NLU Training Data'))
    results.append(check_file_exists('rasa_minimal/stories.yml', 'Dialogue Stories'))
    results.append(check_file_exists('rasa_minimal/config.yml', 'ML Pipeline Config'))
    results.append(check_file_exists('rasa_minimal/rules.yml', 'Fallback Rules'))
    results.append(check_file_exists('rasa_minimal/credentials.yml', 'Server Config'))
    results.append(check_file_exists('rasa_minimal/actions.py', 'Custom Actions'))
    print()
    
    # Check documentation
    print("[4] Checking Documentation")
    results.append(check_file_exists('RASA_COMPLETE_SETUP.md', 'Complete Setup Guide'))
    results.append(check_file_exists('QUICK_START.md', 'Quick Start Guide'))
    results.append(check_file_exists('IMPLEMENTATION_COMPLETE.md', 'Implementation Summary'))
    print()
    
    # Check YAML validity
    print("[5] Validating Rasa YAML Files")
    results.append(check_yaml_valid('rasa_minimal/domain.yml'))
    results.append(check_yaml_valid('rasa_minimal/nlu.yml'))
    results.append(check_yaml_valid('rasa_minimal/stories.yml'))
    results.append(check_yaml_valid('rasa_minimal/config.yml'))
    results.append(check_yaml_valid('rasa_minimal/rules.yml'))
    results.append(check_yaml_valid('rasa_minimal/credentials.yml'))
    print()
    
    # Check JSON validity
    print("[6] Validating JSON Files")
    results.append(check_json_valid('intents.json'))
    print()
    
    # Check templates and static files
    print("[7] Checking Web Assets")
    results.append(check_file_exists('templates/index.html', 'Chat UI'))
    results.append(check_file_exists('static/script.js', 'Frontend Logic'))
    results.append(check_file_exists('static/style.css', 'Styling'))
    print()
    
    # Summary
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"  Results: {passed}/{total} checks passed")
    print("="*60)
    
    if passed == total:
        print("\n  ✓ All checks passed! System is ready to deploy.")
        print("\n  Next steps:")
        print("  1. Install Rasa: conda install -c conda-forge rasa=3.6.0")
        print("  2. Train model: python -m rasa train --domain rasa_minimal/domain.yml ...")
        print("  3. Start Rasa: python -m rasa run -m rasa_minimal/models --enable-api")
        print("  4. Start Flask: python app.py")
        print("  5. Open: http://localhost:5000")
        return 0
    else:
        print("\n  ✗ Some checks failed. Please verify the files above.")
        return 1

if __name__ == '__main__':
    exit(main())
