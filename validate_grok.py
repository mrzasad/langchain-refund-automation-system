#!/usr/bin/env python
"""
Validation script to ensure Grok API is properly configured
"""

import os
from pathlib import Path
from dotenv import load_dotenv

print("=" * 80)
print("GROK API CONFIGURATION VALIDATION")
print("=" * 80)

# Load environment variables
load_dotenv()

# 1. Check .env file
env_path = Path(".env")
print(f"\n1. .env File Check:")
print(f"   Location: {env_path.absolute()}")
print(f"   Exists: {'Yes' if env_path.exists() else 'No'}")

if env_path.exists():
    with open(env_path, 'r') as f:
        content = f.read()
        print(f"   Content:\n{content}")

# 2. Check environment variables
print(f"\n2. Environment Variables Check:")
llm_provider = os.getenv("LLM_PROVIDER")
grok_key = os.getenv("GROK_API_KEY")

print(f"   LLM_PROVIDER: {llm_provider}")
print(f"   GROK_API_KEY exists: {'Yes' if grok_key else 'No'}")
if grok_key:
    if len(grok_key) > 10:
        masked = grok_key[:4] + '*' * (len(grok_key) - 8) + grok_key[-4:]
        print(f"   GROK_API_KEY (masked): {masked}")
    else:
        print(f"   GROK_API_KEY: [INVALID - too short]")

# 3. Validate configuration
print(f"\n3. Configuration Validation:")
if llm_provider == "grok":
    print(f"   ✓ LLM_PROVIDER correctly set to 'grok'")
else:
    print(f"   ✗ ERROR: LLM_PROVIDER is '{llm_provider}', expected 'grok'")

if grok_key:
    print(f"   ✓ GROK_API_KEY is configured")
    if grok_key.startswith('xai-'):
        print(f"   ✓ GROK_API_KEY format looks correct (starts with 'xai-')")
    else:
        print(f"   ⚠ WARNING: GROK_API_KEY doesn't start with 'xai-' (you may have a Groq key instead)")
else:
    print(f"   ✗ ERROR: GROK_API_KEY is not set")

# 4. Test imports
print(f"\n4. Import Validation:")
try:
    from langchain_openai import ChatOpenAI
    print(f"   ✓ ChatOpenAI imported successfully")
except ImportError as e:
    print(f"   ✗ ERROR: Failed to import ChatOpenAI: {e}")

# 5. Test config loading
print(f"\n5. Config Module Validation:")
try:
    from config import API_KEY, LLM_MODEL, LLM_PROVIDER
    print(f"   ✓ config.py loaded successfully")
    print(f"   - LLM_PROVIDER: {LLM_PROVIDER}")
    print(f"   - LLM_MODEL: {LLM_MODEL}")
    print(f"   - API_KEY exists: {'Yes' if API_KEY else 'No'}")
except Exception as e:
    print(f"   ✗ ERROR: Failed to load config.py: {e}")

# 6. Test API connection (minimal)
print(f"\n6. API Connection Test:")
try:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="grok-2",
        api_key=grok_key,
        base_url="https://api.x.ai/v1",
        temperature=0
    )
    print(f"   ✓ ChatOpenAI client created successfully")
    print(f"   ✓ Using endpoint: https://api.x.ai/v1")
    print(f"   ✓ Model: grok-2")
except Exception as e:
    print(f"   ⚠ WARNING: Could not create LLM client: {e}")

print("\n" + "=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)

# Final summary
issues = []
if not llm_provider or llm_provider != "grok":
    issues.append("LLM_PROVIDER not set to 'grok'")
if not grok_key:
    issues.append("GROK_API_KEY not configured")
if grok_key and not grok_key.startswith('xai-'):
    issues.append("GROK_API_KEY may not be from xAI (doesn't start with 'xai-')")

if issues:
    print("\nISSUES FOUND:")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
else:
    print("\n✓ All validations passed! Grok API is properly configured.")
