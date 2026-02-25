"""
Vision tools for diagram extraction and analysis.
Uses Gemini for multimodal understanding.
"""
from pathlib import Path
from typing import List, Dict, Optional
import base64


def extract_images_from_pdf(pdf_path: Path) -> List[Path]:
    """
    Extract images from PDF file.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of paths to extracted images
    """
    try:
        from pdf2image import convert_from_path
        
        # Convert PDF pages to images
        images = convert_from_path(str(pdf_path))
        
        # Save images temporarily
        image_paths = []
        output_dir = pdf_path.parent / "extracted_images"
        output_dir.mkdir(exist_ok=True)
        
        for i, image in enumerate(images):
            img_path = output_dir / f"page_{i+1}.png"
            image.save(str(img_path), "PNG")
            image_paths.append(img_path)
        
        return image_paths
    except ImportError:
        return []
    except Exception:
        return []


def analyze_diagram_with_gemini(image_path: Path, api_key: str) -> Dict:
    """
    Analyze architectural diagram using Gemini Vision.
    
    Args:
        image_path: Path to image file
        api_key: Google API key
        
    Returns:
        Dict with analysis results
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        
        # Initialize Gemini with correct model name
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.0
        )
        
        # Read image
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
        
        # Analyze diagram
        prompt = """Analyze this architectural diagram and answer:

1. Is this a LangGraph StateGraph diagram or a generic flowchart?
2. Does it show parallel execution (fan-out/fan-in)?
3. List the nodes/components visible
4. Describe the flow pattern (linear, parallel, conditional)

Respond in JSON format:
{
    "diagram_type": "StateGraph|Flowchart|Sequence|Other",
    "has_parallel_execution": true/false,
    "nodes": ["node1", "node2"],
    "flow_pattern": "description"
}"""
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": f"data:image/png;base64,{image_data}"}
            ]
        )
        
        response = llm.invoke([message])
        
        # Parse response
        import json
        import re
        
        content = response.content if hasattr(response, 'content') else str(response)
        json_match = re.search(r'{.*}', content, re.DOTALL)
        
        if json_match:
            return json.loads(json_match.group(0))
        else:
            return {
                "diagram_type": "Unknown",
                "has_parallel_execution": False,
                "nodes": [],
                "flow_pattern": content[:200]
            }
    except Exception as e:
        return {
            "error": str(e),
            "diagram_type": "Error",
            "has_parallel_execution": False,
            "nodes": [],
            "flow_pattern": "Analysis failed"
        }
