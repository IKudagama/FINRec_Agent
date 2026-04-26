"""
Demo and test script for FinAgent-Rec
Verifies all components are working correctly
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ontology import initialize_ontology
from vector_store import initialize_vector_store
from agents import create_orchestrator, RecommendationRequest


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_ontology():
    """Test ontology initialization and querying"""
    print_section("TEST 1: RDF Ontology")
    
    try:
        ontology = initialize_ontology()
        print(f"✓ Ontology initialized")
        print(f"  - Total triples: {ontology.get_graph_size()}")
        
        # Test query
        products = ontology.query_products_by_risk("Medium")
        print(f"✓ Query successful: Found {len(products)} Medium-risk products")
        
        for product in products:
            print(f"  - {product['name']}")
        
        return True
    except Exception as e:
        print(f"✗ Ontology test failed: {str(e)}")
        return False


def test_vector_store():
    """Test vector store initialization and search"""
    print_section("TEST 2: FAISS Vector Store")
    
    try:
        vector_store = initialize_vector_store()
        print(f"✓ Vector store initialized")
        print(f"  - Products in index: {vector_store.get_index_size()}")
        
        # Test search
        query = "safe conservative investments"
        results = vector_store.search(query, k=3)
        print(f"✓ Search successful: Found {len(results)} results for '{query}'")
        
        for result in results:
            print(f"  - {result['name']}: {result['similarity_score']:.2%} match")
        
        return True
    except Exception as e:
        print(f"✗ Vector store test failed: {str(e)}")
        return False


def test_agents():
    """Test multi-agent orchestration"""
    print_section("TEST 3: Multi-Agent Orchestration")
    
    try:
        # Initialize components
        ontology = initialize_ontology()
        vector_store = initialize_vector_store()
        orchestrator = create_orchestrator(ontology, vector_store)
        print(f"✓ Orchestrator initialized")
        
        # Test recommendations for Low risk
        print("\n--- Low Risk Profile ---")
        request_low = RecommendationRequest(
            user_id="test_user_low",
            risk_profile="Low",
            description="I need safe, stable investments with minimal risk"
        )
        
        recommendations = orchestrator.get_recommendations(request_low)
        print(f"✓ Generated {len(recommendations)} recommendations")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n  {i}. {rec.product_name}")
            print(f"     Overall Score: {rec.overall_score:.1%}")
            print(f"     Vector Similarity: {rec.vector_similarity:.1%}")
            print(f"     Graph Consistency: {rec.graph_consistency:.1%}")
            print(f"     Risk Level: {rec.risk_level}")
        
        # Test recommendations for Medium risk
        print("\n--- Medium Risk Profile ---")
        request_medium = RecommendationRequest(
            user_id="test_user_medium",
            risk_profile="Medium",
            description="Balanced portfolio with moderate growth"
        )
        
        recommendations = orchestrator.get_recommendations(request_medium)
        print(f"✓ Generated {len(recommendations)} recommendations")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n  {i}. {rec.product_name}")
            print(f"     Overall Score: {rec.overall_score:.1%}")
            print(f"     Vector Similarity: {rec.vector_similarity:.1%}")
            print(f"     Graph Consistency: {rec.graph_consistency:.1%}")
        
        # Test recommendations for High risk
        print("\n--- High Risk Profile ---")
        request_high = RecommendationRequest(
            user_id="test_user_high",
            risk_profile="High",
            description="I'm interested in growth-oriented, high-volatility investments"
        )
        
        recommendations = orchestrator.get_recommendations(request_high)
        print(f"✓ Generated {len(recommendations)} recommendations")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n  {i}. {rec.product_name}")
            print(f"     Overall Score: {rec.overall_score:.1%}")
            print(f"     Vector Similarity: {rec.vector_similarity:.1%}")
            print(f"     Graph Consistency: {rec.graph_consistency:.1%}")
        
        return True
    except Exception as e:
        print(f"✗ Agent test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_explanation_quality():
    """Test explanation generation quality"""
    print_section("TEST 4: Explanation Quality")
    
    try:
        ontology = initialize_ontology()
        vector_store = initialize_vector_store()
        orchestrator = create_orchestrator(ontology, vector_store)
        
        request = RecommendationRequest(
            user_id="test_explain",
            risk_profile="Medium",
            description="Portfolio with dividend income"
        )
        
        recommendations = orchestrator.get_recommendations(request)
        
        if recommendations:
            rec = recommendations[0]
            print(f"✓ Sample Recommendation: {rec.product_name}")
            print(f"\nExplanation:")
            print(f"  {rec.explanation}")
            print(f"\nJustification (RDF Triples):")
            for triple in rec.justification.get("ontology_triples", []):
                if triple:
                    print(f"  {triple}")
            return True
        else:
            print("✗ No recommendations generated")
            return False
    except Exception as e:
        print(f"✗ Explanation test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                     FinAgent-Rec Test Suite                        ║")
    print("║              Multi-Agent RAG for Financial Recommendations         ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Run tests
    results.append(("Ontology", test_ontology()))
    results.append(("Vector Store", test_vector_store()))
    results.append(("Multi-Agent System", test_agents()))
    results.append(("Explanation Quality", test_explanation_quality()))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status:10} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! FinAgent-Rec is ready to use.")
        print("\nNext steps:")
        print("  1. Run: python app.py")
        print("  2. Open: http://localhost:7860")
        print("  3. Select a risk profile and get personalized recommendations!")
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please check the errors above.")
    
    print("\n" + "="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
