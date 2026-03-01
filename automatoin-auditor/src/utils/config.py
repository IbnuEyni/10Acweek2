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
    
    # API Keys (Multiple providers supported)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Model Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # groq, deepseek, openai, anthropic
    DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "llama-3.3-70b-versatile")
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.0"))
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    RUBRIC_PATH = PROJECT_ROOT / "rubric" / "auditor_rubric.json"
    AUDIT_OUTPUT_DIR = PROJECT_ROOT / "audit"
    
    # Safety
    GIT_CLONE_TIMEOUT = 60
    MAX_FILE_SIZE_MB = 10
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        has_api_key = any([
            cls.OPENAI_API_KEY,
            cls.ANTHROPIC_API_KEY,
            cls.GROQ_API_KEY,
            cls.DEEPSEEK_API_KEY,
            cls.GOOGLE_API_KEY,
            cls.TOGETHER_API_KEY,
            cls.OLLAMA_BASE_URL
        ])
        
        if not has_api_key:
            raise ValueError(
                "At least one LLM provider required:\n"
                "  - OPENAI_API_KEY\n"
                "  - ANTHROPIC_API_KEY\n"
                "  - GROQ_API_KEY (fast & free)\n"
                "  - DEEPSEEK_API_KEY (recommended - cheap & powerful)\n"
                "  - GOOGLE_API_KEY\n"
                "  - TOGETHER_API_KEY\n"
                "  - OLLAMA_BASE_URL (local)"
            )
        
        if not cls.RUBRIC_PATH.exists():
            raise FileNotFoundError(f"Rubric not found at {cls.RUBRIC_PATH}")


# Validate on import
Config.validate()
