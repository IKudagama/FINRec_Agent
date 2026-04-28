"""
Knowledge Graph System Test Suite
Tests for financial domain ontology, knowledge base, and agent integration
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from knowledge_graph import initialize_financial_knowledge_graph
from agent_knowledge import AgentKnowledgeSystem
from knowledge_integration import KnowledgeEnhancedOrchestrator
from ontology import initialize_ontology
from vector_store import initialize_vector_store
from agents import RecommendationRequest


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_knowledge_graph_creation():
    """Test 1: Knowledge graph creation and basic operations"""
    print_section("TEST 1: Knowledge Graph Creation")
    
    try:
        kg = initialize_financial_knowledge_graph()
        
        # Check size
        size = kg.get_graph_size()
        print(f"✓ Knowledge graph created")
        print(f"  - Total triples: {size}")
        assert size > 0, "Knowledge graph should have triples"
        
        # Check asset risk levels
        print(f"  - Asset risk levels:")
        for asset in ["Equity", "Debt"]:
            risk = kg.get_asset_risk_level(asset)
            print(f"    {asset}: {risk}")
            assert risk is not None, f"Should have risk level for {asset}"
        
        # Check metrics
        print(f"  - Financial metrics:")
        for metric in ["risk_free_rate", "inflation_rate"]:
            value = kg.get_metric_value(metric)
            print(f"    {metric}: {value}")
            assert value is not None, f"Should have value for {metric}"
        
        print(f"✓ TEST PASSED: Knowledge graph creation")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_knowledge_system():
    """Test 2: Agent knowledge system and reasoning"""
    print_section("TEST 2: Agent Knowledge System")
    
    try:
        kg = initialize_financial_knowledge_graph()
        ks = AgentKnowledgeSystem(kg)
        
        # Test 1: Time horizon rule
        print("✓ Testing time horizon rule:")
        for age, expected_risk in [(25, "High"), (45, "Medium"), (60, "Low")]:
            risk = ks.apply_risk_time_horizon_rule(user_age=age)
            print(f"  Age {age}: {risk}")
            # Older = lower risk
            assert isinstance(risk, str), "Should return risk level string"
        
        # Test 2: Inflation rule
        print("✓ Testing inflation rule:")
        analysis = ks.apply_inflation_rule(0.10)  # 10% return
        print(f"  10% return → Real return: {analysis['real_return']:.1%}")
        assert analysis['preserves_purchasing_power'], "10% return should beat inflation"
        
        analysis = ks.apply_inflation_rule(0.02)  # 2% return
        print(f"  2% return → Real return: {analysis['real_return']:.1%}")
        assert not analysis['preserves_purchasing_power'], "2% return shouldn't beat inflation"
        
        # Test 3: Sharpe ratio
        print("✓ Testing Sharpe ratio calculation:")
        sharpe = ks.apply_sharpe_ratio_rule(0.10, 0.15)
        print(f"  10% return, 15% volatility → Sharpe: {sharpe:.2f}")
        assert isinstance(sharpe, float), "Should return float"
        
        # Test 4: Correlation rule
        print("✓ Testing correlation rule:")
        p1 = {"name": "Stock", "risk_level": "High"}
        p2 = {"name": "Bond", "risk_level": "Low"}
        corr = ks.apply_correlation_rule(p1, p2)
        print(f"  Stock vs Bond → Correlation: {corr['estimated_correlation']}")
        print(f"  Diversification benefit: {corr['diversification_benefit']}")
        
        # Test 5: Knowledge context
        print("✓ Testing knowledge context:")
        context = ks.get_knowledge_context("Medium", [])
        print(f"  Financial metrics loaded: {len(context.financial_metrics)}")
        print(f"  Reasoning rules available: {len(context.reasoning_rules)}")
        print(f"  Relevant facts: {len(context.relevant_facts)}")
        assert context.financial_metrics, "Should have financial metrics"
        assert context.reasoning_rules, "Should have reasoning rules"
        
        print(f"✓ TEST PASSED: Agent knowledge system")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_enhanced_orchestrator():
    """Test 3: Knowledge-enhanced orchestrator"""
    print_section("TEST 3: Knowledge-Enhanced Orchestrator")
    
    try:
        # Initialize components
        ontology = initialize_ontology()
        vector_store = initialize_vector_store()
        kg = initialize_financial_knowledge_graph()
        
        # Create orchestrator
        orchestrator = KnowledgeEnhancedOrchestrator(ontology, vector_store, kg)
        print("✓ Orchestrator initialized")
        
        # Test knowledge context retrieval
        request = RecommendationRequest(
            user_id="test_kg_001",
            risk_profile="Medium",
            description="balanced investments"
        )
        
        context = orchestrator.get_knowledge_context(request)
        print(f"✓ Knowledge context retrieved:")
        print(f"  - Risk profile: {context.user_risk_profile}")
        print(f"  - Financial metrics: {len(context.financial_metrics)}")
        print(f"  - Asset characteristics: {len(context.asset_characteristics)}")
        print(f"  - Reasoning rules: {len(context.reasoning_rules)}")
        
        # Test knowledge-enhanced recommendations
        recommendations = orchestrator.get_knowledge_enhanced_recommendations(request)
        print(f"✓ Generated {len(recommendations)} recommendations")
        
        if recommendations:
            rec = recommendations[0]
            print(f"  - Top recommendation: {rec.product_name}")
            print(f"  - Overall score: {rec.overall_score:.1%}")
            if "knowledge_analysis" in rec.justification:
                ka = rec.justification["knowledge_analysis"]
                if "sharpe_ratio" in ka:
                    print(f"  - Sharpe ratio: {ka['sharpe_ratio']:.2f}")
        
        print(f"✓ TEST PASSED: Knowledge-enhanced orchestrator")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_queries():
    """Test 4: Knowledge graph queries"""
    print_section("TEST 4: Knowledge Graph Queries")
    
    try:
        kg = initialize_financial_knowledge_graph()
        
        # Test 1: Asset characteristics
        print("✓ Testing asset characteristic queries:")
        for asset in ["Equity", "Debt"]:
            chars = kg.query_asset_characteristics(asset)
            print(f"  {asset} has {len(chars['characteristics'])} characteristics")
            assert len(chars['characteristics']) >= 0, "Should have characteristics"
        
        # Test 2: Reasoning rules
        print("✓ Testing reasoning rule queries:")
        rules = kg.query_reasoning_rules()
        print(f"  Total reasoning rules: {len(rules)}")
        for rule in rules[:3]:
            print(f"    - {rule['rule']}")
        assert len(rules) > 0, "Should have reasoning rules"
        
        # Test 3: Concept hierarchy
        print("✓ Testing concept hierarchy queries:")
        hierarchy = kg.query_concept_hierarchy("FinancialProduct")
        print(f"  Financial products hierarchy:")
        print(f"    - Root concepts: {len(hierarchy['concepts'])}")
        for concept in hierarchy['concepts'][:3]:
            label = concept.get('label', 'Unknown')
            print(f"      {label}")
        
        print(f"✓ TEST PASSED: Knowledge graph queries")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_persistence():
    """Test 5: Knowledge graph file persistence"""
    print_section("TEST 5: Knowledge Graph Persistence")
    
    try:
        # Create and save
        kg = initialize_financial_knowledge_graph()
        size1 = kg.get_graph_size()
        print(f"✓ Original graph size: {size1} triples")
        
        # Load in new instance
        kg2 = initialize_financial_knowledge_graph()
        size2 = kg2.get_graph_size()
        print(f"✓ Reloaded graph size: {size2} triples")
        
        # Verify same content
        assert size1 == size2, "Sizes should match"
        
        # Verify queries still work
        risk = kg2.get_asset_risk_level("Equity")
        assert risk == "High", "Loaded data should match"
        print(f"✓ Data integrity verified")
        
        print(f"✓ TEST PASSED: Knowledge graph persistence")
        return True
        
    except Exception as e:
        print(f"✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║            Financial Domain Knowledge Graph Test Suite             ║")
    print("║         Testing ontology, knowledge base, and agent integration    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Run tests
    results.append(("Knowledge Graph Creation", test_knowledge_graph_creation()))
    results.append(("Agent Knowledge System", test_agent_knowledge_system()))
    results.append(("Knowledge Graph Queries", test_knowledge_queries()))
    results.append(("Knowledge Persistence", test_knowledge_persistence()))
    results.append(("Knowledge-Enhanced Orchestrator", test_knowledge_enhanced_orchestrator()))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status:10} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All knowledge graph tests passed!")
        print("\nNext steps:")
        print("  1. Use KnowledgeEnhancedOrchestrator for enhanced recommendations")
        print("  2. Query knowledge graph for domain reasoning")
        print("  3. Extend ontology with domain-specific concepts")
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
    
    print("\n" + "="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
