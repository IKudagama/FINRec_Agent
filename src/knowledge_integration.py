"""
Integration of Knowledge Graph with Existing Agents
Enhanced multi-agent system with knowledge-based reasoning
"""

from agents import (
    RetrievalAgent, RiskAlignmentAgent, ReasoningAgent, FinAgentOrchestrator,
    RecommendationRequest, RecommendationResult
)
from knowledge_graph import initialize_financial_knowledge_graph
from agent_knowledge import (
    AgentKnowledgeSystem, KnowledgeEnhancedRetrievalAgent,
    KnowledgeEnhancedRiskAlignmentAgent, KnowledgeEnhancedReasoningAgent
)
from typing import List, Dict
from ontology import FinanceOntology
from vector_store import FAISSVectorStore
from config import WEIGHTS


class KnowledgeEnhancedOrchestrator(FinAgentOrchestrator):
    """
    Enhanced orchestrator that integrates knowledge graph with agents
    """
    
    def __init__(self, 
                 ontology: FinanceOntology,
                 vector_store: FAISSVectorStore,
                 knowledge_graph=None):
        super().__init__(ontology, vector_store)
        
        # Initialize knowledge graph
        if knowledge_graph is None:
            self.knowledge_graph = initialize_financial_knowledge_graph()
        else:
            self.knowledge_graph = knowledge_graph
        
        # Initialize agent knowledge system
        self.agent_ks = AgentKnowledgeSystem(self.knowledge_graph)
        
        # Create knowledge-enhanced agents
        self.enhanced_retrieval_agent = KnowledgeEnhancedRetrievalAgent(self.agent_ks)
        self.enhanced_risk_agent = KnowledgeEnhancedRiskAlignmentAgent(self.agent_ks)
        self.enhanced_reasoning_agent = KnowledgeEnhancedReasoningAgent(self.agent_ks)
    
    def get_knowledge_context(self, request: RecommendationRequest):
        """
        Get knowledge context for reasoning
        """
        return self.agent_ks.get_knowledge_context(request.risk_profile, [])
    
    def get_knowledge_enhanced_recommendations(self, 
                                              request: RecommendationRequest) -> List[RecommendationResult]:
        """
        Generate recommendations with knowledge graph enhancement
        """
        # Get base recommendations
        base_recommendations = self.get_recommendations(request)
        
        # Enhance with knowledge
        enhanced_recommendations = []
        for rec in base_recommendations:
            # Add knowledge-based analysis
            product = {
                "name": rec.product_name,
                "risk_level": rec.risk_level,
                "expected_return": rec.overall_score,
                "volatility": rec.vector_similarity
            }
            
            # Apply knowledge rules
            inflation_analysis = self.agent_ks.apply_inflation_rule(rec.overall_score)
            sharpe_ratio = self.agent_ks.apply_sharpe_ratio_rule(rec.overall_score, rec.vector_similarity)
            time_horizon = self.agent_ks.apply_risk_time_horizon_rule()
            
            # Enhance explanation with knowledge
            knowledge_explanation = self.agent_ks.explain_recommendation(product, request.risk_profile)
            
            enhanced_rec = RecommendationResult(
                product_id=rec.product_id,
                product_name=rec.product_name,
                risk_level=rec.risk_level,
                overall_score=rec.overall_score,
                vector_similarity=rec.vector_similarity,
                graph_consistency=rec.graph_consistency,
                explanation=rec.explanation + "\n\n" + knowledge_explanation,
                justification={
                    **rec.justification,
                    "knowledge_analysis": {
                        "inflation_analysis": inflation_analysis,
                        "sharpe_ratio": sharpe_ratio,
                        "time_horizon_recommendation": time_horizon
                    }
                }
            )
            
            enhanced_recommendations.append(enhanced_rec)
        
        return enhanced_recommendations
    
    def debug_knowledge_graph(self):
        """
        Print knowledge graph statistics and examples
        """
        print("\n" + "="*70)
        print("KNOWLEDGE GRAPH STATISTICS")
        print("="*70)
        
        print(f"Total triples: {self.knowledge_graph.get_graph_size()}")
        
        # Asset risks
        print("\nAsset Risk Levels:")
        for asset in ["Equity", "Debt", "Commodity"]:
            risk = self.knowledge_graph.get_asset_risk_level(asset)
            print(f"  {asset}: {risk}")
        
        # Financial metrics
        print("\nFinancial Metrics:")
        for metric in ["risk_free_rate", "inflation_rate", "market_return"]:
            value = self.knowledge_graph.get_metric_value(metric)
            print(f"  {metric}: {value}")
        
        # Knowledge context
        print("\nKnowledge Context (Medium Risk Profile):")
        context = self.agent_ks.get_knowledge_context("Medium", [])
        print(f"  Risk-free rate: {context.financial_metrics['risk_free_rate']}")
        print(f"  Inflation rate: {context.financial_metrics['inflation_rate']}")
        print(f"  Reasoning rules available: {len(context.reasoning_rules)}")
        print(f"  Relevant facts: {len(context.relevant_facts)}")


# ==============================================================================
# ENHANCED EXAMPLE RECOMMENDATIONS
# ==============================================================================

def example_knowledge_enhanced_recommendations():
    """
    Show example of knowledge-enhanced recommendations
    """
    from ontology import initialize_ontology
    from vector_store import initialize_vector_store
    
    # Initialize all components
    ontology = initialize_ontology()
    vector_store = initialize_vector_store()
    knowledge_graph = initialize_financial_knowledge_graph()
    
    # Create orchestrator
    orchestrator = KnowledgeEnhancedOrchestrator(ontology, vector_store, knowledge_graph)
    
    print("\n" + "="*70)
    print("KNOWLEDGE-ENHANCED RECOMMENDATION SYSTEM")
    print("="*70)
    
    # Show knowledge graph
    orchestrator.debug_knowledge_graph()
    
    # Generate recommendations
    print("\n" + "="*70)
    print("GENERATING RECOMMENDATIONS WITH KNOWLEDGE ENHANCEMENT")
    print("="*70)
    
    request = RecommendationRequest(
        user_id="kg_user_001",
        risk_profile="Medium",
        description="I want balanced investments with good risk-adjusted returns"
    )
    
    recommendations = orchestrator.get_knowledge_enhanced_recommendations(request)
    
    print(f"\nGenerated {len(recommendations)} knowledge-enhanced recommendations:\n")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.product_name}")
        print(f"   Risk Level: {rec.risk_level}")
        print(f"   Overall Score: {rec.overall_score:.1%}")
        print(f"   Vector Similarity: {rec.vector_similarity:.1%}")
        print(f"   Graph Consistency: {rec.graph_consistency:.1%}")
        
        # Show knowledge-based analysis
        if "knowledge_analysis" in rec.justification:
            ka = rec.justification["knowledge_analysis"]
            print(f"\n   Knowledge-Based Analysis:")
            if "inflation_analysis" in ka:
                inf = ka["inflation_analysis"]
                print(f"     - Real Return (after inflation): {inf['real_return']:.1%}")
                print(f"     - Preserves Purchasing Power: {inf['preserves_purchasing_power']}")
            if "sharpe_ratio" in ka:
                print(f"     - Sharpe Ratio: {ka['sharpe_ratio']:.2f}")
            if "time_horizon_recommendation" in ka:
                print(f"     - Time Horizon Recommendation: {ka['time_horizon_recommendation']}")
        
        print(f"\n   Explanation:\n{rec.explanation[:300]}...")


def analyze_knowledge_graph_coverage():
    """
    Analyze coverage of knowledge graph
    """
    kg = initialize_financial_knowledge_graph()
    ks = AgentKnowledgeSystem(kg)
    
    print("\n" + "="*70)
    print("KNOWLEDGE GRAPH COVERAGE ANALYSIS")
    print("="*70)
    
    # Asset knowledge
    print("\n1. Asset Class Knowledge:")
    for asset in ["Equity", "Debt", "Commodity"]:
        asset_kg = ks.get_asset_knowledge(asset)
        print(f"\n   {asset}:")
        print(f"     Risk Level: {asset_kg['risk_level']}")
        print(f"     Characteristics: {len(asset_kg['characteristics'])} items")
    
    # Financial concepts
    print("\n2. Financial Concepts:")
    concepts = ["Volatility", "Liquidity", "Risk", "Return", "Diversification"]
    for concept in concepts:
        concept_kg = ks.get_financial_concept(concept)
        print(f"   ✓ {concept_kg.get('label', concept)}")
    
    # Knowledge rules
    print("\n3. Reasoning Rules:")
    rules = kg.query_reasoning_rules()
    for rule in rules:
        print(f"   ✓ {rule['rule']}")
    
    # Financial metrics
    print("\n4. Financial Metrics:")
    metrics = ["risk_free_rate", "inflation_rate", "market_return", "market_volatility"]
    for metric in metrics:
        value = kg.get_metric_value(metric)
        print(f"   {metric}: {value}")


if __name__ == "__main__":
    # Run examples
    
    # 1. Show knowledge-enhanced recommendations
    example_knowledge_enhanced_recommendations()
    
    # 2. Analyze knowledge coverage
    analyze_knowledge_graph_coverage()
    
    print("\n✓ Knowledge graph integration complete!")
