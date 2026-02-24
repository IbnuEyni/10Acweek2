#!/usr/bin/env python3
"""
Phase 1 validation script.
Verifies infrastructure setup before proceeding to Phase 2.
"""
import sys
from pathlib import Path


def validate_structure():
    """Validate directory structure."""
    print("🔍 Validating project structure...")
    
    required_dirs = [
        "src/nodes",
        "src/tools",
        "src/utils",
        "rubric",
        "audit/report_bypeer_received",
        "audit/report_onpeer_generated",
        "audit/report_onself_generated",
        "audit/langsmith_logs",
        "tests"
    ]
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Missing directory: {dir_path}")
            return False
    
    print("✅ Directory structure valid")
    return True


def validate_files():
    """Validate required files exist."""
    print("\n🔍 Validating required files...")
    
    required_files = [
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "README.md",
        "Dockerfile",
        "src/__init__.py",
        "src/state.py",
        "src/utils/config.py",
        "src/utils/rubric_loader.py",
        "rubric/week2_rubric.json"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Missing file: {file_path}")
            return False
    
    print("✅ All required files present")
    return True


def validate_state_models():
    """Validate state models can be imported."""
    print("\n🔍 Validating state models...")
    
    try:
        from src.state import Evidence, JudicialOpinion, RubricDimension, AgentState
        print("✅ State models import successfully")
        
        # Test Evidence model
        evidence = Evidence(
            goal="test",
            found=True,
            location="test.py",
            rationale="test",
            confidence=0.9
        )
        print("✅ Evidence model instantiation works")
        
        # Test JudicialOpinion model
        opinion = JudicialOpinion(
            judge="Prosecutor",
            criterion_id="test",
            score=3,
            argument="test",
            cited_evidence=[]
        )
        print("✅ JudicialOpinion model instantiation works")
        
        return True
    except Exception as e:
        print(f"❌ State model validation failed: {e}")
        return False


def validate_rubric():
    """Validate rubric can be loaded."""
    print("\n🔍 Validating rubric loader...")
    
    try:
        from src.utils.rubric_loader import (
            load_rubric,
            get_rubric_dimensions,
            get_synthesis_rules
        )
        
        rubric = load_rubric()
        print(f"✅ Rubric loaded: {rubric['rubric_metadata']['rubric_name']}")
        
        dimensions = get_rubric_dimensions()
        print(f"✅ Parsed {len(dimensions)} rubric dimensions")
        
        rules = get_synthesis_rules()
        print(f"✅ Loaded {len(rules)} synthesis rules")
        
        return True
    except Exception as e:
        print(f"❌ Rubric validation failed: {e}")
        return False


def validate_config():
    """Validate configuration (without requiring API keys)."""
    print("\n🔍 Validating configuration...")
    
    try:
        # Temporarily allow missing API keys for validation
        import os
        os.environ["OPENAI_API_KEY"] = "test_key"
        
        from src.utils.config import Config
        
        print(f"✅ Config loaded")
        print(f"   - Project root: {Config.PROJECT_ROOT}")
        print(f"   - Rubric path: {Config.RUBRIC_PATH}")
        print(f"   - Default model: {Config.DEFAULT_LLM_MODEL}")
        
        return True
    except Exception as e:
        print(f"❌ Config validation failed: {e}")
        return False


def main():
    """Run all validations."""
    print("=" * 60)
    print("PHASE 1 VALIDATION: Foundation & Infrastructure")
    print("=" * 60)
    
    validations = [
        validate_structure,
        validate_files,
        validate_state_models,
        validate_rubric,
        validate_config
    ]
    
    results = [validation() for validation in validations]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ PHASE 1 COMPLETE - All validations passed!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Copy .env.example to .env and add your API keys")
        print("2. Install dependencies: uv pip install -e .")
        print("3. Run tests: pytest tests/")
        print("4. Proceed to Phase 2: Detective Layer implementation")
        return 0
    else:
        print("❌ PHASE 1 INCOMPLETE - Some validations failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
