"""
Agent Knowledge System
Enables agents to reason using the financial domain knowledge graph
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from knowledge_graph import FinancialDomainKnowledge
import json


@dataclass
class KnowledgeContext:
    """Context for agent reasoning with knowledge"""
    user_risk_profile: str
    financial_metrics: Dict[str, float]
    asset_characteristics: Dict[str, Dict[str, Any]]
    reasoning_rules: List[Dict]
    relevant_facts: List[Dict]


class AgentKnowledgeSystem:
    """
    Provides knowledge-enhanced reasoning for recommendation agents
    """
    
    def __init__(self, knowledge_graph: FinancialDomainKnowledge):
        self.kg = knowledge_graph
        self._build_knowledge_index()
    
    def _build_knowledge_index(self):
        """
        Build efficient index of knowledge for fast lookup
        """
        self.asset_risks = {}
        self.asset_volatilities = {}
        self.asset_liquidity = {}
        
        # Cache asset characteristics
        for asset_class in ["Equity", "Debt", "Commodity", "Currency", "Derivative"]:
            try:
                chars = self.kg.query_asset_characteristics(asset_class)
                self.asset_risks[asset_class] = self.kg.get_asset_risk_level(asset_class)
            except:
                pass
    
    def get_knowledge_context(self, user_risk_profile: str, 
                             products: List[Dict]) -> KnowledgeContext:
        """
        Build knowledge context for agent reasoning
        """
        # Get financial metrics
        metrics = {
            "risk_free_rate": self.kg.get_metric_value("risk_free_rate"),
            "inflation_rate": self.kg.get_metric_value("inflation_rate"),
            "market_return": self.kg.get_metric_value("market_return"),
            "market_volatility": self.kg.get_metric_value("market_volatility")
        }
        
        # Get asset characteristics
        asset_chars = {}
        for asset in ["Equity", "Debt", "Commodity"]:
            try:
                asset_chars[asset] = self.kg.query_asset_characteristics(asset)
            except:
                asset_chars[asset] = {}
        
        # Get reasoning rules
        rules = self.kg.query_reasoning_rules()
        
        # Get relevant facts
        facts = self._get_relevant_facts(user_risk_profile, products)
        
        return KnowledgeContext(
            user_risk_profile=user_risk_profile,
            financial_metrics=metrics,
            asset_characteristics=asset_chars,
            reasoning_rules=rules,
            relevant_facts=facts
        )
    
    def _get_relevant_facts(self, risk_profile: str, products: List[Dict]) -> List[Dict]:
        """
        Get facts relevant to the user and products
        """
        # For now, return predefined relevant facts
        facts = [
            {
                "fact": "Diversification reduces unsystematic risk",
                "applies_to": ["portfolio construction", "risk management"]
            },
            {
                "fact": "Higher returns require higher risk tolerance",
                "applies_to": ["high-yield bonds", "crypto", "small-cap stocks"]
            },
            {
                "fact": "Treasury bonds are stable but may not beat inflation",
                "applies_to": ["low-risk investors", "bonds"]
            },
            {
                "fact": "Time horizon determines risk capacity",
                "applies_to": ["young investors", "long-term planning"]
            }
        ]
        
        return facts
    
    # =============================================================================
    # KNOWLEDGE-BASED REASONING METHODS
    # =============================================================================
    
    def apply_diversification_rule(self, products: List[Dict]) -> float:
        """
        Evaluate portfolio diversification using knowledge rules
        
        Returns: Diversification score (0-1)
        """
        # Get asset types
        asset_types = set()
        for product in products:
            risk_level = product.get("risk_level", "Medium")
            # Map risk level to asset type
            if risk_level == "Low":
                asset_types.add("Debt")
            elif risk_level == "High":
                asset_types.add("Equity")
            else:
                asset_types.add("Mixed")
        
        # Score based on diversity
        diversity_score = min(len(asset_types) / 3.0, 1.0)  # Max 3 asset types
        return diversity_score
    
    def apply_risk_time_horizon_rule(self, user_age: int = None, 
                                     years_to_retirement: int = None) -> str:
        """
        Apply time horizon rule to determine appropriate risk level
        
        Returns: Recommended risk level based on time horizon
        """
        if years_to_retirement is None and user_age:
            years_to_retirement = 65 - user_age
        
        if years_to_retirement is None:
            years_to_retirement = 20  # Default assumption
        
        # Apply time horizon rule
        if years_to_retirement > 15:
            return "High"  # Can take more risk
        elif years_to_retirement > 7:
            return "Medium"
        else:
            return "Low"  # Short horizon = conservative
    
    def apply_inflation_rule(self, product_return: float) -> Dict[str, Any]:
        """
        Apply inflation rule to assess purchasing power preservation
        
        Returns: Analysis of return vs. inflation
        """
        inflation = self.kg.get_metric_value("inflation_rate") or 0.03
        real_return = product_return - inflation
        
        return {
            "nominal_return": product_return,
            "inflation_rate": inflation,
            "real_return": real_return,
            "preserves_purchasing_power": real_return > 0,
            "recommendation": "Good for long-term" if real_return > 0.02 else "May lose to inflation"
        }
    
    def apply_sharpe_ratio_rule(self, product_return: float, volatility: float) -> float:
        """
        Calculate Sharpe ratio using knowledge of risk-free rate
        
        Returns: Risk-adjusted return metric
        """
        risk_free_rate = self.kg.get_metric_value("risk_free_rate") or 0.045
        
        if volatility == 0:
            return 0.0
        
        sharpe_ratio = (product_return - risk_free_rate) / volatility
        return max(sharpe_ratio, 0.0)
    
    def apply_correlation_rule(self, product1: Dict, product2: Dict) -> Dict[str, Any]:
        """
        Analyze correlation between two products for diversification benefit
        
        Returns: Correlation analysis
        """
        # Simplified: infer correlation from risk profiles
        risk1 = product1.get("risk_level", "Medium")
        risk2 = product2.get("risk_level", "Medium")
        
        # Same risk = higher correlation (move together)
        if risk1 == risk2:
            correlation = 0.7
            diversification_benefit = "Low"
        else:
            correlation = 0.3
            diversification_benefit = "High"
        
        return {
            "product1": product1.get("name"),
            "product2": product2.get("name"),
            "estimated_correlation": correlation,
            "diversification_benefit": diversification_benefit,
            "recommendation": "Combine for better diversification" if correlation < 0.5 else "Similar risk profiles"
        }
    
    # =============================================================================
    # KNOWLEDGE QUERYING METHODS
    # =============================================================================
    
    def get_asset_knowledge(self, asset_name: str) -> Dict[str, Any]:
        """
        Get comprehensive knowledge about an asset class
        """
        knowledge = {
            "asset": asset_name,
            "risk_level": self.kg.get_asset_risk_level(asset_name),
            "characteristics": self.kg.query_asset_characteristics(asset_name),
            "concepts": self.kg.query_concept_hierarchy(f"AssetClass_{asset_name}")
        }
        return knowledge
    
    def get_financial_concept(self, concept_name: str) -> Dict[str, Any]:
        """
        Get knowledge about a financial concept
        """
        query = f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX fintech: <http://example.com/fintech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?label ?definition ?interpretation
        WHERE {{
            fintech:Concept_{concept_name} ?prop ?value .
            OPTIONAL {{ fintech:Concept_{concept_name} skos:prefLabel ?label }}
            OPTIONAL {{ fintech:Concept_{concept_name} skos:definition ?definition }}
            OPTIONAL {{ fintech:Concept_{concept_name} fintech:hasInterpretation ?interpretation }}
        }}
        """
        
        results = {"concept": concept_name}
        for row in self.kg.graph.query(query):
            if row.label:
                results["label"] = str(row.label)
            if row.definition:
                results["definition"] = str(row.definition)
            if row.interpretation:
                results["interpretation"] = str(row.interpretation)
        
        return results
    
    def explain_recommendation(self, product: Dict, user_profile: str) -> str:
        """
        Generate knowledge-based explanation for a recommendation
        """
        explanation = f"\n{product['name']} Explanation (Knowledge-Based):\n"
        explanation += "=" * 50 + "\n"
        
        # Risk alignment
        product_risk = product.get("risk_level", "Unknown")
        explanation += f"Risk Level Match: {user_profile} investor ↔ {product_risk} product\n"
        
        # Inflation analysis
        inflation_analysis = self.apply_inflation_rule(product.get("expected_return", 0))
        explanation += f"Inflation Protection: Real return of {inflation_analysis['real_return']:.1%}\n"
        
        # Sharpe ratio
        sharpe = self.apply_sharpe_ratio_rule(
            product.get("expected_return", 0),
            product.get("volatility", 0)
        )
        explanation += f"Risk-Adjusted Return (Sharpe): {sharpe:.2f}\n"
        
        # Key facts
        explanation += "\nKey Financial Principles Applied:\n"
        explanation += "  • Higher returns require higher risk tolerance\n"
        explanation += "  • Diversification reduces unsystematic risk\n"
        explanation += "  • Time horizon determines risk capacity\n"
        
        return explanation


class KnowledgeEnhancedRetrievalAgent:
    """
    Retrieval agent enhanced with knowledge graph reasoning
    """
    
    def __init__(self, agent_ks: AgentKnowledgeSystem):
        self.ks = agent_ks
    
    def retrieve_with_knowledge(self, query: str, risk_profile: str) -> List[Dict]:
        """
        Retrieve products with knowledge enhancement
        """
        # Get knowledge context
        context = self.ks.get_knowledge_context(risk_profile, [])
        
        # For now, return the context as metadata
        return {
            "query": query,
            "risk_profile": risk_profile,
            "knowledge_context": {
                "financial_metrics": context.financial_metrics,
                "relevant_facts": context.relevant_facts,
                "reasoning_rules": len(context.reasoning_rules)
            }
        }


class KnowledgeEnhancedRiskAlignmentAgent:
    """
    Risk alignment agent enhanced with knowledge graph
    """
    
    def __init__(self, agent_ks: AgentKnowledgeSystem):
        self.ks = agent_ks
    
    def validate_with_knowledge(self, product: Dict, user_profile: str) -> Dict[str, Any]:
        """
        Validate product-user match using knowledge rules
        """
        risk_alignment = self.ks.apply_inflation_rule(product.get("expected_return", 0))
        time_horizon_recommendation = self.ks.apply_risk_time_horizon_rule()
        sharpe = self.ks.apply_sharpe_ratio_rule(
            product.get("expected_return", 0),
            product.get("volatility", 0)
        )
        
        return {
            "product": product.get("name"),
            "user_profile": user_profile,
            "inflation_analysis": risk_alignment,
            "sharpe_ratio": sharpe,
            "time_horizon_recommendation": time_horizon_recommendation,
            "is_suitable": risk_alignment["preserves_purchasing_power"]
        }


class KnowledgeEnhancedReasoningAgent:
    """
    Reasoning agent enhanced with knowledge graph explanations
    """
    
    def __init__(self, agent_ks: AgentKnowledgeSystem):
        self.ks = agent_ks
    
    def reason_with_knowledge(self, product: Dict, user_profile: str) -> str:
        """
        Generate explanation using knowledge graph
        """
        return self.ks.explain_recommendation(product, user_profile)


if __name__ == "__main__":
    from knowledge_graph import initialize_financial_knowledge_graph
    
    # Initialize
    kg = initialize_financial_knowledge_graph()
    ks = AgentKnowledgeSystem(kg)
    
    print("\n" + "="*70)
    print("AGENT KNOWLEDGE SYSTEM EXAMPLES")
    print("="*70)
    
    # Example 1: Time horizon rule
    print("\n1. Time Horizon Rule:")
    recommended_risk = ks.apply_risk_time_horizon_rule(user_age=35)
    print(f"   For 35-year-old: Recommended risk = {recommended_risk}")
    
    # Example 2: Inflation rule
    print("\n2. Inflation Analysis:")
    product = {"name": "Treasury Bond", "expected_return": 0.03}
    analysis = ks.apply_inflation_rule(product["expected_return"])
    print(f"   Treasury Bond: Real return = {analysis['real_return']:.1%}")
    
    # Example 3: Sharpe ratio
    print("\n3. Sharpe Ratio (Risk-Adjusted Return):")
    sharpe = ks.apply_sharpe_ratio_rule(0.10, 0.15)
    print(f"   Stock portfolio: Sharpe = {sharpe:.2f}")
    
    # Example 4: Knowledge context
    print("\n4. Knowledge Context for Agent:")
    context = ks.get_knowledge_context("Medium", [])
    print(f"   Risk-free rate: {context.financial_metrics['risk_free_rate']}")
    print(f"   Inflation rate: {context.financial_metrics['inflation_rate']}")
    print(f"   Available reasoning rules: {len(context.reasoning_rules)}")
    print(f"   Available facts: {len(context.relevant_facts)}")
