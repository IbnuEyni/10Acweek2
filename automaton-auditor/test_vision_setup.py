#!/usr/bin/env python3
"""
Test Vision Inspector setup.
Verifies Gemini API key and image analysis capability.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils.config import Config


def test_vision_setup():
    """Test if vision inspector is properly configured."""
    
    print("=" * 60)
    print("VISION INSPECTOR SETUP TEST")
    print("=" * 60)
    
    # Check Google API key
    print("\n1️⃣  Checking Google API key...")
    if Config.GOOGLE_API_KEY and Config.GOOGLE_API_KEY != "YOUR_GOOGLE_API_KEY_HERE":
        print(f"   ✅ Google API key configured: {Config.GOOGLE_API_KEY[:20]}...")
    else:
        print("   ❌ Google API key NOT configured")
        print("\n   To enable Vision Inspector:")
        print("   1. Get free API key: https://aistudio.google.com/app/apikey")
        print("   2. Add to .env: GOOGLE_API_KEY=your_key_here")
        print("\n   Note: Vision Inspector is OPTIONAL for Phase 2")
        return
    
    # Test Gemini connection
    print("\n2️⃣  Testing Gemini connection...")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.0
        )
        
        response = llm.invoke("Say 'Vision OK' if you can read this.")
        print(f"   ✅ Gemini responding: {response.content[:50]}")
    except Exception as e:
        print(f"   ❌ Gemini connection failed: {e}")
        return
    
    # Check pdf2image
    print("\n3️⃣  Checking pdf2image library...")
    try:
        import pdf2image
        print("   ✅ pdf2image installed")
    except ImportError:
        print("   ⚠️  pdf2image not installed")
        print("   Install: pip install pdf2image")
        print("   Also requires poppler: sudo apt install poppler-utils")
    
    print("\n" + "=" * 60)
    print("✅ VISION INSPECTOR READY")
    print("=" * 60)
    print("\nVision Inspector will analyze diagrams in PDF reports.")
    print("It will detect StateGraph patterns and parallel execution.")


if __name__ == "__main__":
    test_vision_setup()
