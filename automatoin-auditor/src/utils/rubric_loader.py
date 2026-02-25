"""
Rubric loader and parser for the Automaton Auditor.
"""
import json
from typing import List, Dict
from pathlib import Path
from src.state import RubricDimension
from src.utils.config import Config


def load_rubric() -> Dict:
    """Load the complete rubric JSON."""
    with open(Config.RUBRIC_PATH) as f:
        return json.load(f)


def get_rubric_dimensions() -> List[RubricDimension]:
    """Parse rubric into Pydantic models."""
    rubric = load_rubric()
    return [RubricDimension(**dim) for dim in rubric["dimensions"]]


def get_synthesis_rules() -> Dict[str, str]:
    """Extract synthesis rules for Chief Justice."""
    rubric = load_rubric()
    return rubric["synthesis_rules"]


def filter_dimensions_by_artifact(artifact_type: str) -> List[RubricDimension]:
    """Filter rubric dimensions by target artifact (github_repo or pdf_report)."""
    dimensions = get_rubric_dimensions()
    return [dim for dim in dimensions if dim.target_artifact == artifact_type]
