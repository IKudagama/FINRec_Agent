"""
FinAgent-Rec: Multi-Agent RAG System for Financial Recommendations

A sophisticated AI-powered system that combines:
- RDF Knowledge Graph (using rdflib)
- FAISS Vector Store (for semantic search)
- Multi-Agent Orchestration (Retrieval, Risk Alignment, Reasoning agents)
- Gradio Web Interface

For more information, see README.md
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .ontology import FinanceOntology, initialize_ontology
from .vector_store import FAISSVectorStore, initialize_vector_store
from .agents import (
    FinAgentOrchestrator,
    RetrievalAgent,
    RiskAlignmentAgent,
    ReasoningAgent,
    RecommendationRequest,
    RecommendationResult,
    create_orchestrator
)

__all__ = [
    "FinanceOntology",
    "initialize_ontology",
    "FAISSVectorStore",
    "initialize_vector_store",
    "FinAgentOrchestrator",
    "RetrievalAgent",
    "RiskAlignmentAgent",
    "ReasoningAgent",
    "RecommendationRequest",
    "RecommendationResult",
    "create_orchestrator"
]
