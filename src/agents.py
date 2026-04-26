"""
Multi-Agent Orchestration for FinAgent-Rec
Implements three agents: Retrieval, Risk Alignment, and Reasoning
Uses state machine pattern for agent coordination
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum
from ontology import FinanceOntology
from vector_store import FAISSVectorStore
from config import WEIGHTS, RECOMMENDATION_THRESHOLD, RISK_LEVELS
import json


class AgentState(Enum):
    """States for multi-agent orchestration"""
    IDLE = "idle"
    RETRIEVING = "retrieving"
    VALIDATING = "validating"
    REASONING = "reasoning"
    COMPLETED = "completed"


@dataclass
class RecommendationRequest:
    """Represents a recommendation request"""
    user_id: str
    risk_profile: str
    description: str = "I need financial advice"
    num_recommendations: int = 3


@dataclass
class RecommendationResult:
    """Represents a recommendation result"""
    product_id: str
    product_name: str
    risk_level: str
    overall_score: float
    vector_similarity: float
    graph_consistency: float
    explanation: str
    justification: Dict = field(default_factory=dict)


class RetrievalAgent:
    """
    Retrieval Agent: Fetches data from both RDF Graph and Vector Store
    """
    
    def __init__(self, ontology: FinanceOntology, vector_store: FAISSVectorStore):
        self.ontology = ontology
        self.vector_store = vector_store
    
    def retrieve_by_risk_profile(self, risk_level: str) -> List[Dict]:
        """
        Retrieve products from RDF graph by risk level
        """
        results = self.ontology.query_products_by_risk(risk_level)
        return results
    
    def retrieve_by_semantic_search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve products from vector store by semantic similarity
        """
        results = self.vector_store.search(query, k=k)
        return results
    
    def retrieve_combined(self, risk_level: str, query: str, k: int = 5) -> Dict[str, List]:
        """
        Retrieve from both sources for comprehensive search
        """
        return {
            "by_risk": self.retrieve_by_risk_profile(risk_level),
            "by_semantics": self.retrieve_by_semantic_search(query, k=k)
        }


class RiskAlignmentAgent:
    """
    Risk Alignment Agent: Validates if products match user's risk profile
    Scores graph consistency
    """
    
    def __init__(self, ontology: FinanceOntology):
        self.ontology = ontology
    
    def calculate_risk_alignment(self, user_risk: str, product_risk: str) -> float:
        """
        Calculate how well a product's risk aligns with user's risk profile
        
        Returns alignment score (0-1)
        """
        user_value = RISK_LEVELS.get(user_risk, 0.5)
        product_value = RISK_LEVELS.get(product_risk, 0.5)
        
        # Alignment is inverse of the difference
        # If they match exactly, score is 1.0
        diff = abs(user_value - product_value)
        alignment = 1.0 - min(diff, 1.0)
        
        return alignment
    
    def validate_products(self, products: List[Dict], user_risk: str) -> List[Dict]:
        """
        Validate products and add alignment scores
        """
        validated = []
        
        for product in products:
            product_risk = product.get("risk_level", "Medium")
            alignment = self.calculate_risk_alignment(user_risk, product_risk)
            
            product_with_score = {
                **product,
                "graph_consistency": alignment,
                "is_aligned": alignment >= 0.5
            }
            validated.append(product_with_score)
        
        # Sort by alignment score
        validated.sort(key=lambda x: x["graph_consistency"], reverse=True)
        
        return validated


class ReasoningAgent:
    """
    Reasoning Agent: Generates natural language explanations
    Cites specific triples/relationships from the knowledge graph
    """
    
    def __init__(self, ontology: FinanceOntology):
        self.ontology = ontology
    
    def generate_explanation(self, 
                           product: Dict, 
                           user_risk: str,
                           vector_sim: float,
                           graph_consistency: float) -> str:
        """
        Generate a natural language explanation for why a product is recommended
        """
        product_name = product.get("name", "Unknown Product")
        product_risk = product.get("risk_level", "Unknown")
        volatility = product.get("volatility", 0)
        expected_return = product.get("expected_return", 0)
        description = product.get("description", "")
        
        explanation = f"'{product_name}' is recommended for your {user_risk} risk profile. "
        
        # Add graph-based reasoning
        if graph_consistency >= 0.8:
            explanation += f"According to the knowledge graph, this {product_risk}-risk product "
            explanation += f"(volatility: {volatility:.2f}) is well-aligned with your profile. "
        elif graph_consistency >= 0.5:
            explanation += f"This product with {product_risk} risk and volatility of {volatility:.2f} "
            explanation += f"is moderately suitable for you. "
        else:
            explanation += f"While this product has some relevant characteristics, "
            explanation += f"it may not be ideal for your {user_risk} risk profile. "
        
        # Add semantic reasoning
        if vector_sim >= 0.8:
            explanation += f"Vector similarity analysis shows strong semantic match ({vector_sim:.2f}). "
        elif vector_sim >= 0.5:
            explanation += f"Semantic analysis suggests moderate relevance ({vector_sim:.2f}). "
        
        # Add specifics
        if expected_return > 0:
            explanation += f"Expected return: {expected_return*100:.1f}%. "
        
        explanation += f"Product details: {description}"
        
        return explanation.strip()
    
    def generate_justification(self, 
                              product: Dict,
                              user_risk: str,
                              ontology_match: bool) -> Dict:
        """
        Generate detailed justification with RDF triples
        """
        return {
            "ontology_triples": [
                f"<{product['id']}> hasRiskLevel <{product['risk_level']}>",
                f"<{product['id']}> hasVolatility {product.get('volatility', 0)}",
                f"<{product['id']}> hasExpectedReturn {product.get('expected_return', 0)}",
                f"<{user_risk}Risk> isSuitableFor <{product['id']}>" if ontology_match else None
            ],
            "matching_criteria": {
                "risk_alignment": f"User profile ({user_risk}) matched with product risk ({product['risk_level']})",
                "volatility_check": f"Product volatility {product.get('volatility', 0)} assessed",
                "return_expectation": f"Expected return {product.get('expected_return', 0)} evaluated"
            }
        }


class FinAgentOrchestrator:
    """
    Orchestrates the multi-agent system
    Coordinates Retrieval, Risk Alignment, and Reasoning agents
    """
    
    def __init__(self, 
                 ontology: FinanceOntology,
                 vector_store: FAISSVectorStore):
        self.ontology = ontology
        self.vector_store = vector_store
        self.retrieval_agent = RetrievalAgent(ontology, vector_store)
        self.risk_agent = RiskAlignmentAgent(ontology)
        self.reasoning_agent = ReasoningAgent(ontology)
        self.state = AgentState.IDLE
    
    def score_recommendation(self, 
                            vector_sim: float,
                            graph_consistency: float) -> float:
        """
        Calculate final recommendation score using weighted formula:
        Score = (w1 * VectorSimilarity) + (w2 * GraphConsistency)
        
        Higher weight on graph consistency for safety
        """
        w1 = WEIGHTS["vector_similarity"]
        w2 = WEIGHTS["graph_consistency"]
        
        score = (w1 * vector_sim) + (w2 * graph_consistency)
        return min(score, 1.0)  # Normalize to 0-1
    
    def get_recommendations(self, request: RecommendationRequest) -> List[RecommendationResult]:
        """
        Main orchestration method
        Coordinates all three agents to generate recommendations
        """
        self.state = AgentState.RETRIEVING
        
        # Step 1: Retrieval Agent
        retrieval_results = self.retrieval_agent.retrieve_combined(
            request.risk_profile,
            request.description,
            k=request.num_recommendations * 2
        )
        
        # Merge results from both sources
        all_products = {}
        for product in retrieval_results["by_risk"]:
            all_products[product["product"]] = {
                **product,
                "from_graph": True,
                "from_vector": False
            }
        
        for product in retrieval_results["by_semantics"]:
            key = f"Product_{product['product_id']}"
            if key in all_products:
                all_products[key]["from_vector"] = True
                all_products[key]["vector_sim"] = product["similarity_score"]
            else:
                all_products[key] = {
                    **product,
                    "from_graph": False,
                    "from_vector": True,
                    "product": key
                }
        
        # Step 2: Risk Alignment Agent
        self.state = AgentState.VALIDATING
        products_list = list(all_products.values())
        validated_products = self.risk_agent.validate_products(products_list, request.risk_profile)
        
        # Step 3: Reasoning Agent & Scoring
        self.state = AgentState.REASONING
        recommendations = []
        
        for product in validated_products:
            # Get vector similarity if not already calculated
            vector_sim = product.get("vector_sim", 0.0)
            if vector_sim == 0.0 and "similarity_score" in product:
                vector_sim = product["similarity_score"]
            
            # Get graph consistency
            graph_consistency = product.get("graph_consistency", 0.5)
            
            # Calculate final score
            overall_score = self.score_recommendation(vector_sim, graph_consistency)
            
            # Only include if above threshold
            if overall_score >= RECOMMENDATION_THRESHOLD:
                # Generate explanation
                explanation = self.reasoning_agent.generate_explanation(
                    product,
                    request.risk_profile,
                    vector_sim,
                    graph_consistency
                )
                
                # Generate justification
                justification = self.reasoning_agent.generate_justification(
                    product,
                    request.risk_profile,
                    product.get("graph_consistency", 0) >= 0.5
                )
                
                recommendation = RecommendationResult(
                    product_id=product.get("id") or product.get("product_id", "unknown"),
                    product_name=product.get("name", "Unknown"),
                    risk_level=product.get("risk_level", "Unknown"),
                    overall_score=overall_score,
                    vector_similarity=vector_sim,
                    graph_consistency=graph_consistency,
                    explanation=explanation,
                    justification=justification
                )
                recommendations.append(recommendation)
        
        # Sort by overall score
        recommendations.sort(key=lambda x: x.overall_score, reverse=True)
        
        # Return top N
        self.state = AgentState.COMPLETED
        return recommendations[:request.num_recommendations]


def create_orchestrator(ontology: FinanceOntology, 
                       vector_store: FAISSVectorStore) -> FinAgentOrchestrator:
    """
    Factory function to create a configured orchestrator
    """
    return FinAgentOrchestrator(ontology, vector_store)


if __name__ == "__main__":
    from ontology import initialize_ontology
    from vector_store import initialize_vector_store
    
    # Initialize components
    ontology = initialize_ontology()
    vector_store = initialize_vector_store()
    
    # Create orchestrator
    orchestrator = create_orchestrator(ontology, vector_store)
    
    # Test recommendation
    request = RecommendationRequest(
        user_id="user_001",
        risk_profile="Medium",
        description="I'm looking for balanced investments with moderate returns"
    )
    
    recommendations = orchestrator.get_recommendations(request)
    
    print(f"Generated {len(recommendations)} recommendations:\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec.product_name}")
        print(f"   Overall Score: {rec.overall_score:.3f}")
        print(f"   Vector Similarity: {rec.vector_similarity:.3f}")
        print(f"   Graph Consistency: {rec.graph_consistency:.3f}")
        print(f"   Explanation: {rec.explanation}\n")
