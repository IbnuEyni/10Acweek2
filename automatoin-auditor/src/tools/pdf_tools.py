"""
PDF tools for document parsing and analysis.
Extracts text, supports chunking, and cross-references with code evidence.
"""
from pathlib import Path
from typing import List, Dict, Optional, Iterator


def parse_pdf_simple(pdf_path: Path) -> str:
    """
    Parse PDF and extract text content.
    Fallback to simple extraction if Docling unavailable.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text content
        
    Raises:
        FileNotFoundError: If PDF doesn't exist
        ValueError: If PDF is corrupted or empty
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    if pdf_path.stat().st_size == 0:
        raise ValueError(f"PDF is empty: {pdf_path}")
    
    try:
        # Try Docling first (enterprise-grade)
        from docling.document_converter import DocumentConverter
        
        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))
        text = result.document.export_to_markdown()
        
        if not text or len(text.strip()) < 100:
            raise ValueError("PDF extracted but content too short (< 100 chars)")
        
        return text
    except ImportError:
        # Fallback to PyPDF2
        try:
            import PyPDF2
            
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                
                if len(reader.pages) == 0:
                    raise ValueError("PDF has 0 pages")
                
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                
                if not text or len(text.strip()) < 100:
                    raise ValueError("PDF extracted but content too short (< 100 chars)")
                
                return text
        except ImportError:
            return f"Error: PDF parsing libraries not available. Install: pip install docling PyPDF2"


def chunk_pdf_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> Iterator[Dict[str, any]]:
    """
    Split PDF text into overlapping chunks for queryable access.
    Useful for large documents that exceed LLM context windows.
    
    Args:
        text: Full PDF text
        chunk_size: Target chunk size in characters
        overlap: Overlap between chunks for context continuity
        
    Yields:
        Dict with chunk_id, text, start_pos, end_pos
    """
    if not text:
        return
    
    start = 0
    chunk_id = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        
        # Try to break at sentence boundary
        if end < len(text):
            last_period = text.rfind('.', start, end)
            if last_period > start + chunk_size // 2:
                end = last_period + 1
        
        yield {
            "chunk_id": chunk_id,
            "text": text[start:end],
            "start_pos": start,
            "end_pos": end,
            "length": end - start
        }
        
        chunk_id += 1
        start = end - overlap if end < len(text) else end


def query_chunks(text: str, query: str, max_chunks: int = 3) -> List[Dict]:
    """
    Search for query in chunked text and return most relevant chunks.
    Simple keyword-based search (can be enhanced with embeddings).
    
    Args:
        text: Full PDF text
        query: Search query (e.g., "StateGraph architecture")
        max_chunks: Maximum chunks to return
        
    Returns:
        List of relevant chunks sorted by relevance
    """
    chunks = list(chunk_pdf_text(text))
    query_lower = query.lower()
    
    # Score chunks by keyword matches
    scored_chunks = []
    for chunk in chunks:
        score = chunk["text"].lower().count(query_lower)
        if score > 0:
            scored_chunks.append({**chunk, "relevance_score": score})
    
    # Sort by relevance and return top chunks
    scored_chunks.sort(key=lambda x: x["relevance_score"], reverse=True)
    return scored_chunks[:max_chunks]


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
        "Parallel Execution",
        "State Synchronization",
        "Pydantic",
        "StateGraph",
        "LangGraph",
        "Multi-Agent",
        "Fan-Out",
        "Fan-In",
        "CRDT",
        "Reducer",
        "Concurrent",
        "Deterministic",
        "Commutative",
        "Idempotent",
        "Type Safety",
        "Graph Compilation",
        "Node Orchestration"
    ]
    
    counts = {}
    text_lower = text.lower()
    
    for keyword in keywords:
        counts[keyword] = text_lower.count(keyword.lower())
    
    return counts
