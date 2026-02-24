"""
PDF tools for document parsing and analysis.
Extracts text and cross-references with code evidence.
"""
from pathlib import Path
from typing import List, Dict, Optional


def parse_pdf_simple(pdf_path: Path) -> str:
    """
    Parse PDF and extract text content.
    Fallback to simple extraction if Docling unavailable.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    try:
        # Try Docling first (enterprise-grade)
        from docling.document_converter import DocumentConverter
        
        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))
        return result.document.export_to_markdown()
    except ImportError:
        # Fallback to PyPDF2
        try:
            import PyPDF2
            
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            return f"Error: PDF parsing libraries not available. Install: pip install docling PyPDF2"


def extract_concepts(text: str, concepts: List[str]) -> Dict[str, List[str]]:
    """
    Search for specific concepts in text and extract context.
    
    Args:
        text: Document text
        concepts: List of concepts to search for
        
    Returns:
        Dict mapping concept to list of sentences containing it
    """
    findings = {concept: [] for concept in concepts}
    
    sentences = text.split('.')
    
    for sentence in sentences:
        for concept in concepts:
            if concept.lower() in sentence.lower():
                findings[concept].append(sentence.strip())
    
    return findings


def cross_reference_claims(text: str, verified_files: List[str]) -> Dict:
    """
    Cross-reference file paths mentioned in PDF with actual files.
    
    Args:
        text: PDF text content
        verified_files: List of actual file paths from repo
        
    Returns:
        Dict with verified and hallucinated claims
    """
    # Extract potential file paths from text
    import re
    
    # Pattern: src/something.py or similar
    path_pattern = r'[a-zA-Z_][a-zA-Z0-9_/]*\.py'
    mentioned_paths = re.findall(path_pattern, text)
    
    verified_files_str = [str(f) for f in verified_files]
    
    verified = []
    hallucinated = []
    
    for path in set(mentioned_paths):
        # Check if any verified file ends with this path
        if any(path in vf for vf in verified_files_str):
            verified.append(path)
        else:
            hallucinated.append(path)
    
    return {
        "verified_claims": verified,
        "hallucinated_claims": hallucinated,
        "total_mentioned": len(set(mentioned_paths))
    }


def extract_architectural_keywords(text: str) -> Dict[str, int]:
    """
    Count occurrences of key architectural terms.
    
    Args:
        text: Document text
        
    Returns:
        Dict with keyword counts
    """
    keywords = [
        "Dialectical Synthesis",
        "Metacognition",
        "Fan-Out",
        "Fan-In",
        "State Synchronization",
        "Parallel Execution",
        "Pydantic",
        "StateGraph",
        "LangGraph",
        "Multi-Agent"
    ]
    
    counts = {}
    text_lower = text.lower()
    
    for keyword in keywords:
        counts[keyword] = text_lower.count(keyword.lower())
    
    return counts
