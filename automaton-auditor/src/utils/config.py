"""
Configuration management for the Automaton Auditor.
Handles environment variables, API keys, and observability setup.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LangSmith Observability
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "automaton-auditor")
if langsmith_key := os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGCHAIN_API_KEY"] = langsmith_key


class Config:
    """Central configuration for the auditor system."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Model Configuration
    DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gpt-4o")
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.0"))
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    RUBRIC_PATH = PROJECT_ROOT / "rubric" / "week2_rubric.json"
    AUDIT_OUTPUT_DIR = PROJECT_ROOT / "audit"
    
    # Safety
    GIT_CLONE_TIMEOUT = 60
    MAX_FILE_SIZE_MB = 10
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            raise ValueError("At least one LLM API key required (OPENAI_API_KEY or ANTHROPIC_API_KEY)")
        
        if not cls.RUBRIC_PATH.exists():
            raise FileNotFoundError(f"Rubric not found at {cls.RUBRIC_PATH}")


# Validate on import
Config.validate()
