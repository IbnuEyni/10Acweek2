"""
LLM factory for multi-provider support.
Supports Groq, DeepSeek, OpenAI, Anthropic, and more.
"""
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from src.utils.config import Config


def get_llm(temperature: float = 0.0, model: str = None):
    """
    Get LLM instance based on configured provider.
    
    Args:
        temperature: Sampling temperature (0.0 = deterministic)
        model: Override default model
        
    Returns:
        LLM instance
    """
    provider = Config.LLM_PROVIDER.lower()
    model = model or Config.DEFAULT_LLM_MODEL
    
    if provider == "groq":
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set")
        return ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model=model or "llama-3.3-70b-versatile",
            temperature=temperature
        )
    
    elif provider == "deepseek":
        if not Config.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY not set")
        return ChatOpenAI(
            api_key=Config.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
            model=model or "deepseek-chat",
            temperature=temperature
        )
    
    elif provider == "openai":
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set")
        return ChatOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model=model or "gpt-4o",
            temperature=temperature
        )
    
    elif provider == "anthropic":
        if not Config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set")
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            api_key=Config.ANTHROPIC_API_KEY,
            model=model or "claude-3-5-sonnet-20241022",
            temperature=temperature
        )
    
    else:
        raise ValueError(
            f"Unknown provider: {provider}. "
            f"Supported: groq, deepseek, openai, anthropic"
        )


def get_judge_llm():
    """Get LLM for judge evaluations (high reasoning capability)."""
    return get_llm(temperature=0.0)
