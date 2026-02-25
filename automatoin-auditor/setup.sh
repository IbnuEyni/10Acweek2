#!/bin/bash
# Setup script for Automaton Auditor

echo "🚀 Setting up Automaton Auditor..."

# Check Python version
python3 --version

# Upgrade pip and typing-extensions
echo "📦 Upgrading core packages..."
python3 -m pip install --upgrade pip typing-extensions

# Install project dependencies
echo "📦 Installing dependencies..."
python3 -m pip install --upgrade \
    "pydantic>=2.0.0" \
    "langgraph>=0.2.0" \
    "langchain>=0.3.0" \
    "langchain-openai>=0.2.0" \
    "langchain-anthropic>=0.2.0" \
    "gitpython>=3.1.0" \
    "python-dotenv>=1.0.0" \
    "langsmith>=0.1.0" \
    "pytest>=7.0.0"

echo "✅ Dependencies installed"

# Validate setup
echo ""
echo "🔍 Running Phase 1 validation..."
python3 validate_phase1.py

echo ""
echo "📝 Next steps:"
echo "1. Copy .env.example to .env: cp .env.example .env"
echo "2. Edit .env with your API keys"
echo "3. Run tests: pytest tests/"
