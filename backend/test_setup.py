#!/usr/bin/env python3
"""
Quick setup test script for Phase 1
Tests that all imports work and basic structure is correct
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all main modules can be imported."""
    print("Testing imports...")
    
    try:
        from app.main import app
        print("✅ app.main imported")
        
        from app.core.config import settings
        print("✅ app.core.config imported")
        
        from app.storage.parquet_handler import ParquetHandler
        print("✅ app.storage.parquet_handler imported")
        
        from app.storage.metadata_handler import MetadataHandler
        print("✅ app.storage.metadata_handler imported")
        
        from app.storage.duckdb_query import DuckDBQuery
        print("✅ app.storage.duckdb_query imported")
        
        from app.services.project_service import ProjectService
        print("✅ app.services.project_service imported")
        
        from app.utils.date_utils import get_date_range
        print("✅ app.utils.date_utils imported")
        
        from app.schemas.project import ProjectCreate
        print("✅ app.schemas.project imported")
        
        from app.schemas.funnel import FunnelCreate
        print("✅ app.schemas.funnel imported")
        
        from app.schemas.event import EventSchema
        print("✅ app.schemas.event imported")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_data_directories():
    """Test that data directories exist."""
    print("\nTesting data directories...")
    
    data_dir = Path("data")
    required_dirs = ["events", "metadata", "config"]
    
    for dir_name in required_dirs:
        dir_path = data_dir / dir_name
        if dir_path.exists():
            print(f"✅ {dir_path} exists")
        else:
            print(f"⚠️  {dir_path} does not exist (will be created on first run)")
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   Created {dir_path}")


def test_config():
    """Test configuration."""
    print("\nTesting configuration...")
    
    try:
        from app.core.config import settings
        print(f"✅ DATA_DIR: {settings.DATA_DIR}")
        print(f"✅ ENVIRONMENT: {settings.ENVIRONMENT}")
        print(f"✅ API_PORT: {settings.API_PORT}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("IAFA Phase 1 Setup Test")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_imports()
    test_data_directories()
    all_passed &= test_config()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ Phase 1 Setup: PASSED")
        print("\nNext steps:")
        print("1. Run: uvicorn app.main:app --reload --port 8000")
        print("2. Visit: http://localhost:8000/docs")
    else:
        print("❌ Phase 1 Setup: FAILED")
        print("Please fix the errors above")
    print("=" * 50)
    
    sys.exit(0 if all_passed else 1)
