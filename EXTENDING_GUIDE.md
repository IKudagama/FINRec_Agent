"""
Guide for extending FinAgent-Rec

This file demonstrates how to add new products, customize the system,
and integrate with external data sources.
"""

# ==============================================================================
# 1. ADDING NEW FINANCIAL PRODUCTS
# ==============================================================================

from src.ontology import FinanceOntology
from src.vector_store import initialize_vector_store
from src.config import ONTOLOGY_FILE
import os

def add_new_products():
    """
    Example: Adding new financial products to the system
    """
    ontology = FinanceOntology()
    ontology.load_ontology()
    
    # Define new products
    new_products = [
        {
            "id": "real_estate_fund",
            "name": "Real Estate Investment Fund",
            "description": "REIT fund providing exposure to commercial and residential real estate",
            "risk_level": "Medium",
            "volatility": 0.12,
            "expected_return": 0.06
        },
        {
            "id": "crypto_etf",
            "name": "Crypto Index ETF",
            "description": "Diversified exposure to major cryptocurrencies with basket approach",
            "risk_level": "High",
            "volatility": 0.85,
            "expected_return": 0.35
        },
        {
            "id": "dividend_aristocrats",
            "name": "Dividend Aristocrats ETF",
            "description": "Companies with 25+ years of consecutive dividend increases",
            "risk_level": "Low",
            "volatility": 0.10,
            "expected_return": 0.05
        }
    ]
    
    # Add to ontology
    for product in new_products:
        ontology.add_product(
            product_id=product["id"],
            name=product["name"],
            description=product["description"],
            risk_level=product["risk_level"],
            volatility=product["volatility"],
            expected_return=product["expected_return"]
        )
        print(f"✓ Added: {product['name']}")
    
    # Save updated ontology
    ontology.save_ontology()
    
    # Update vector store
    from src.config import MOCK_PRODUCTS
    all_products = MOCK_PRODUCTS + new_products
    vector_store = initialize_vector_store(force_recreate=True)
    vector_store.add_products(all_products)
    
    print("\n✓ Products added successfully!")
    print(f"✓ Vector store updated with {vector_store.get_index_size()} products")


# ==============================================================================
# 2. INTEGRATING WITH EXTERNAL DATA SOURCES
# ==============================================================================

def fetch_products_from_api():
    """
    Example: Fetch products from external financial API
    """
    import requests
    
    # Example: Alpha Vantage API
    API_KEY = "YOUR_API_KEY"
    
    # Fetch stock data
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
    
    products = []
    for symbol in symbols:
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            product = {
                "id": symbol.lower(),
                "name": f"{data.get('Name', symbol)} Stock",
                "description": f"Stock in {data.get('Name', symbol)} - {data.get('Sector', 'Technology')} sector",
                "risk_level": "Medium",
                "volatility": 0.15,
                "expected_return": 0.10
            }
            products.append(product)
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
    
    return products


# ==============================================================================
# 3. CUSTOM RISK PROFILING
# ==============================================================================

def create_custom_user_profile():
    """
    Example: Create a detailed user profile with custom risk assessment
    """
    from src.ontology import FinanceOntology
    
    ontology = FinanceOntology()
    ontology.load_ontology()
    
    # User with extended attributes
    user_data = {
        "user_id": "user_advanced_001",
        "name": "Jane Smith",
        "age": 35,
        "income": 150000,
        "savings": 500000,
        "time_horizon": "20 years",
        "investment_experience": "advanced"
    }
    
    # Calculate risk profile based on multiple factors
    def calculate_risk_profile(user):
        score = 0
        
        # Time horizon factor
        if user["time_horizon"] == "20 years":
            score += 0.3  # Long horizon = higher risk capacity
        
        # Experience factor
        if user["investment_experience"] == "advanced":
            score += 0.2
        
        # Income stability factor
        score += 0.2
        
        if score >= 0.6:
            return "High"
        elif score >= 0.35:
            return "Medium"
        else:
            return "Low"
    
    risk_profile = calculate_risk_profile(user_data)
    print(f"Calculated risk profile for {user_data['name']}: {risk_profile}")
    
    # Add user to ontology
    ontology.add_user(
        user_id=user_data["user_id"],
        name=user_data["name"],
        risk_profile=risk_profile
    )
    ontology.save_ontology()


# ==============================================================================
# 4. CUSTOM SCORING WEIGHTS
# ==============================================================================

def adjust_scoring_weights():
    """
    Example: Customize scoring weights for different use cases
    """
    
    # Conservative approach (prioritize graph consistency heavily)
    conservative_weights = {
        "vector_similarity": 0.2,
        "graph_consistency": 0.8
    }
    
    # Aggressive approach (balance both signals)
    balanced_weights = {
        "vector_similarity": 0.5,
        "graph_consistency": 0.5
    }
    
    # Edit config.py to use different weights:
    # WEIGHTS = conservative_weights  # or balanced_weights
    
    print("Weights defined. Edit src/config.py WEIGHTS variable to apply.")


# ==============================================================================
# 5. QUERYING THE KNOWLEDGE GRAPH DIRECTLY
# ==============================================================================

def advanced_sparql_queries():
    """
    Example: Run custom SPARQL queries on the knowledge graph
    """
    from src.ontology import FinanceOntology
    
    ontology = FinanceOntology()
    ontology.load_ontology()
    
    # Query 1: Find all products with volatility > 0.2
    query_high_volatility = """
    PREFIX fintech: <http://example.com/fintech/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?product ?name ?volatility
    WHERE {
        ?product a fintech:Product ;
                 rdfs:label ?name ;
                 fintech:has_volatility ?volatility .
        FILTER (?volatility > 0.2)
    }
    """
    
    print("High Volatility Products:")
    for row in ontology.graph.query(query_high_volatility):
        print(f"  - {row.name}: {float(row.volatility):.2f}")
    
    # Query 2: Find products suitable for multiple risk levels
    query_products_by_return = """
    PREFIX fintech: <http://example.com/fintech/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?product ?name ?return
    WHERE {
        ?product a fintech:Product ;
                 rdfs:label ?name ;
                 fintech:has_expected_return ?return .
    }
    ORDER BY DESC(?return)
    """
    
    print("\nProducts by Expected Return:")
    for row in ontology.graph.query(query_products_by_return):
        print(f"  - {row.name}: {float(row['return'])*100:.1f}%")


# ==============================================================================
# 6. SWAPPING TO GRAPHDB (ENTERPRISE)
# ==============================================================================

def migrate_to_graphdb():
    """
    Example: How to migrate from local RDF to GraphDB
    """
    
    example_code = """
    # Instead of using rdflib, use GraphDB API:
    
    from graphdb import GraphDB
    from rdflib import Namespace
    
    # Connect to GraphDB
    graphdb = GraphDB(endpoint="http://localhost:7200/repositories/fintech")
    
    # SPARQL query (same syntax as rdflib)
    results = graphdb.query(
        \"\"\"
        PREFIX fintech: <http://example.com/fintech/>
        SELECT ?product WHERE {
            ?product a fintech:Product .
        }
        \"\"\"
    )
    
    # Update ontology.py to use graphdb instead of rdflib
    # Change class FinanceOntology to use GraphDB backend
    """
    
    print("GraphDB Migration Guide:")
    print(example_code)


# ==============================================================================
# 7. TESTING RECOMMENDATION QUALITY
# ==============================================================================

def evaluate_recommendations():
    """
    Example: Evaluate recommendation quality
    """
    from src.agents import create_orchestrator
    from src.ontology import initialize_ontology
    from src.vector_store import initialize_vector_store
    
    ontology = initialize_ontology()
    vector_store = initialize_vector_store()
    orchestrator = create_orchestrator(ontology, vector_store)
    
    # Test cases
    test_cases = [
        {"risk": "Low", "description": "Safety first"},
        {"risk": "Medium", "description": "Balanced growth"},
        {"risk": "High", "description": "Maximum growth"},
    ]
    
    results = {}
    
    for test in test_cases:
        from src.agents import RecommendationRequest
        
        request = RecommendationRequest(
            user_id="test",
            risk_profile=test["risk"],
            description=test["description"]
        )
        
        recommendations = orchestrator.get_recommendations(request)
        results[test["risk"]] = {
            "count": len(recommendations),
            "avg_score": sum(r.overall_score for r in recommendations) / len(recommendations) if recommendations else 0,
            "products": [r.product_name for r in recommendations]
        }
    
    print("\nRecommendation Quality Metrics:")
    for risk_level, data in results.items():
        print(f"\n{risk_level} Risk Profile:")
        print(f"  Recommendations: {data['count']}")
        print(f"  Avg Score: {data['avg_score']:.1%}")
        print(f"  Products: {', '.join(data['products'])}")


# ==============================================================================
# 8. MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("FinAgent-Rec Extension Guide")
    print("="*50)
    print("\nChoose an operation:")
    print("1. Add new products")
    print("2. Create custom user profile")
    print("3. Adjust scoring weights")
    print("4. Run custom SPARQL queries")
    print("5. Evaluate recommendations")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        add_new_products()
    elif choice == "2":
        create_custom_user_profile()
    elif choice == "3":
        adjust_scoring_weights()
    elif choice == "4":
        advanced_sparql_queries()
    elif choice == "5":
        evaluate_recommendations()
    else:
        print("Invalid choice!")
