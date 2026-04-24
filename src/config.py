"""
Configuration and constants for FinAgent-Rec
"""

# Scoring weights for the recommendation algorithm
WEIGHTS = {
    "vector_similarity": 0.3,   # Weight for vector similarity
    "graph_consistency": 0.7    # Weight for graph consistency (higher priority for ontology-verified)
}

# Risk levels
RISK_LEVELS = {
    "Low": 0.2,      # Conservative
    "Medium": 0.5,   # Balanced
    "High": 0.9      # Aggressive
}

# Model configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DIMENSION = 384
VECTOR_INDEX_PATH = "data/vector_index.faiss"

# Ontology paths
ONTOLOGY_FILE = "data/fintech.ttl"
ONTOLOGY_FORMAT = "turtle"

# Database paths
RDF_STORE = "data/rdf_store"

# Mock data
MOCK_PRODUCTS = [
    {
        "id": "bitcoin",
        "name": "Bitcoin",
        "description": "Decentralized digital currency with high volatility and growth potential",
        "risk_level": "High",
        "volatility": 0.95,
        "expected_return": 0.25
    },
    {
        "id": "treasury_bonds",
        "name": "US Treasury Bonds",
        "description": "Government-backed bonds with low risk and stable returns",
        "risk_level": "Low",
        "volatility": 0.05,
        "expected_return": 0.03
    },
    {
        "id": "sp500_etf",
        "name": "S&P 500 ETF",
        "description": "Exchange-traded fund tracking the S&P 500 index with moderate risk",
        "risk_level": "Medium",
        "volatility": 0.15,
        "expected_return": 0.10
    },
    {
        "id": "high_yield_bonds",
        "name": "High-Yield Bonds",
        "description": "High-Yield Bond with sensitivity to interest rate hikes and default risk",
        "risk_level": "High",
        "volatility": 0.25,
        "expected_return": 0.07
    },
    {
        "id": "savings_account",
        "name": "Savings Account",
        "description": "FDIC-insured savings account with minimal risk and liquid returns",
        "risk_level": "Low",
        "volatility": 0.0,
        "expected_return": 0.045
    }
]

# Threshold for recommendation
RECOMMENDATION_THRESHOLD = 0.5
