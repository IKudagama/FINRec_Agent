# FinAgent-Rec: Multi-Agent RAG System for Financial Recommendations

## 🎯 Overview

**FinAgent-Rec** is a sophisticated AI-powered system for generating explainable, personalized financial product recommendations. It combines three key technologies:

1. **Knowledge Graph (RDF/SPARQL)**: Semantic representation of financial products, risk profiles, and relationships
2. **Vector Embeddings (FAISS)**: Semantic search over product descriptions  
3. **Multi-Agent Orchestration**: Coordinated AI agents for retrieval, validation, and reasoning

The system ensures recommendations are both **semantically relevant** and **ontology-safe** through a weighted scoring mechanism that prioritizes graph consistency (70%) over vector similarity (30%).

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  FinAgent-Rec System                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐        ┌──────────────┐                  │
│  │ RDF Ontology │        │ FAISS Store  │                  │
│  │   (fintech   │        │  (Vector     │                  │
│  │     .ttl)    │        │ embeddings)  │                  │
│  └──────┬───────┘        └──────┬───────┘                  │
│         │                       │                           │
│         └───────────┬───────────┘                           │
│                     │                                       │
│        ┌────────────▼────────────┐                         │
│        │  Retrieval Agent 🔍     │                         │
│        │  Fetches from both      │                         │
│        │  sources                │                         │
│        └────────────┬────────────┘                         │
│                     │                                       │
│        ┌────────────▼────────────┐                         │
│        │  Risk Alignment Agent ✓ │                         │
│        │  Validates risk match   │                         │
│        │  (Graph Consistency)    │                         │
│        └────────────┬────────────┘                         │
│                     │                                       │
│        ┌────────────▼────────────┐                         │
│        │  Reasoning Agent 💡     │                         │
│        │  Generates explanations │                         │
│        │  Cites RDF triples      │                         │
│        └────────────┬────────────┘                         │
│                     │                                       │
│        ┌────────────▼────────────┐                         │
│        │  Scoring Function       │                         │
│        │  Score = 0.3×VS +       │                         │
│        │          0.7×GC         │                         │
│        └────────────┬────────────┘                         │
│                     │                                       │
│        ┌────────────▼────────────┐                         │
│        │  Ranked Recommendations │                         │
│        │  with Explanations      │                         │
│        └────────────────────────┘                         │
│                     │                                       │
│        ┌────────────▼────────────┐                         │
│        │   Gradio Web UI 🎨      │                         │
│        │   Interactive interface │                         │
│        └────────────────────────┘                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Key Concepts

### Scoring Formula

The recommendation algorithm prioritizes **ontology-verified recommendations** (safe) over merely similar ones:

$$\text{Score} = (w_1 \times \text{VectorSimilarity}) + (w_2 \times \text{GraphConsistency})$$

Where:
- $w_1 = 0.3$ (Vector Similarity weight - semantic relevance)
- $w_2 = 0.7$ (Graph Consistency weight - ontology alignment)

This ensures that only products aligned with the user's risk profile in the knowledge graph are prioritized, even if other products are semantically similar.

### Cold Start Problem Solution

The ontology solves the **cold-start problem** by:
- Pre-defining semantic rules for risk profiles
- Mapping new users to products via ontology classes (e.g., "Student" → "Low Risk Products")
- Eliminating dependency on historical user data
- Providing immediate, rule-based recommendations

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project
cd FinRec_Agent

# Create virtual environment (recommended)
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize the System

```bash
# Initialize ontology and vector store (creates data files)
python src/ontology.py
python src/vector_store.py
```

This creates:
- `data/fintech.ttl` - RDF ontology file
- `data/vector_index.faiss` - FAISS vector index
- `data/vector_index_metadata.json` - Vector metadata

### 3. Run the Web Interface

```bash
python app.py
```

Then open your browser to `http://localhost:7860`

### 4. Test Programmatically

```python
from src.ontology import initialize_ontology
from src.vector_store import initialize_vector_store
from src.agents import create_orchestrator, RecommendationRequest

# Initialize
ontology = initialize_ontology()
vector_store = initialize_vector_store()
orchestrator = create_orchestrator(ontology, vector_store)

# Get recommendations
request = RecommendationRequest(
    user_id="user_001",
    risk_profile="Medium",
    description="Looking for balanced growth investments"
)

recommendations = orchestrator.get_recommendations(request)

for rec in recommendations:
    print(f"\n{rec.product_name}")
    print(f"Score: {rec.overall_score:.1%}")
    print(f"Explanation: {rec.explanation}")
```

## 📁 Project Structure

```
FinRec_Agent/
├── src/
│   ├── config.py              # Configuration and constants
│   ├── ontology.py            # RDF ontology (rdflib)
│   ├── vector_store.py        # FAISS vector embeddings
│   ├── agents.py              # Multi-agent orchestration
│   └── __init__.py
├── data/
│   ├── fintech.ttl           # RDF ontology file (generated)
│   ├── vector_index.faiss    # FAISS index (generated)
│   └── vector_index_metadata.json  # Vector metadata
├── tests/
│   └── test_agents.py        # Unit tests (optional)
├── app.py                     # Gradio UI
├── requirements.txt           # Dependencies
├── README.md                  # This file
└── .gitignore
```

## 🔑 Core Components

### 1. Ontology (`src/ontology.py`)

- **Classes**: Product, RiskLevel, User
- **Properties**: 
  - `is_suitable_for` (Product → RiskLevel)
  - `has_volatility` (Product → Float)
  - `has_expected_return` (Product → Float)
  - `has_risk_profile` (User → RiskLevel)

**Format**: Turtle (.ttl) - easy to view and edit

**Example Triple**:
```turtle
fintech:Product_sp500_etf a fintech:Product ;
    rdfs:label "S&P 500 ETF" ;
    fintech:has_description "Exchange-traded fund tracking S&P 500..." ;
    fintech:is_suitable_for fintech:RiskLevel_Medium ;
    fintech:has_volatility 0.15 ;
    fintech:has_expected_return 0.10 .
```

### 2. Vector Store (`src/vector_store.py`)

- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Index Type**: FAISS (Flat L2 distance)
- **Dimension**: 384
- **Search**: Semantic similarity over product descriptions

### 3. Multi-Agent System (`src/agents.py`)

#### Retrieval Agent
- Queries RDF graph by risk level
- Searches vector store by semantic similarity
- Merges results from both sources

#### Risk Alignment Agent
- Calculates alignment between user risk and product risk
- Validates products against ontology constraints
- Produces `graph_consistency` score (0-1)

#### Reasoning Agent
- Generates natural language explanations
- Cites specific RDF triples
- Produces human-readable justifications

#### Orchestrator
- Coordinates the three agents
- Calculates final recommendation score
- Filters by recommendation threshold (0.5)
- Returns ranked results

### 4. Gradio UI (`app.py`)

- **Input**: Risk level (Low/Medium/High) + optional description
- **Output**: Top 3 recommendations with:
  - Product name and risk level
  - Scores (Vector Similarity, Graph Consistency, Overall)
  - Natural language explanation
  - Expandable RDF triple justifications

## 💼 Use Cases

### 1. Financial Advisory
Provide personalized recommendations to investors based on their risk tolerance

### 2. Robo-Advisor
Automated system for portfolio suggestions with explainability

### 3. Investment Education
Demonstrate how AI reasoning works with financial products

### 4. Regulatory Compliance
Show audit trail of recommendations through ontology triples

## 🔄 Workflow Examples

### Example 1: Conservative Investor
```
Input: Risk Profile = "Low"
       Description = "I need stability and safety"

Output:
1. US Treasury Bonds (98% match)
   - Graph Consistency: 95% (Perfect alignment with Low risk)
   - Vector Similarity: 92% (Semantically matches "stability")

2. Savings Account (95% match)
   - Graph Consistency: 100% (Lowest risk product)
   - Vector Similarity: 80% (Good semantic match)
```

### Example 2: Balanced Investor
```
Input: Risk Profile = "Medium"
       Description = "Looking for growth with moderation"

Output:
1. S&P 500 ETF (92% match)
   - Graph Consistency: 85% (Well-aligned)
   - Vector Similarity: 88% (Good semantic match)

2. High-Yield Bonds (71% match)
   - Graph Consistency: 60% (Moderately aligned)
   - Vector Similarity: 75% (Relevant but riskier)
```

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
# Scoring weights (must sum to 1.0)
WEIGHTS = {
    "vector_similarity": 0.3,
    "graph_consistency": 0.7
}

# Risk level scale (0-1)
RISK_LEVELS = {
    "Low": 0.2,
    "Medium": 0.5,
    "High": 0.9
}

# Recommendation threshold
RECOMMENDATION_THRESHOLD = 0.5
```

## 📈 Extending the System

### Adding Products
```python
ontology.add_product(
    product_id="gold_etf",
    name="Gold ETF",
    description="Commodity ETF tracking gold prices...",
    risk_level="Medium",
    volatility=0.18,
    expected_return=0.04
)
ontology.save_ontology()
```

### Swapping to GraphDB
Replace `ontology.py` with GraphDB SPARQL queries:
```python
# Instead of rdflib
from graphdb_client import GraphDBClient

client = GraphDBClient(endpoint="http://localhost:7200")
results = client.query("SELECT ?product WHERE { ?product a fintech:Product }")
```

### Custom Embedding Model
```python
# In src/config.py
EMBEDDING_MODEL = "all-mpnet-base-v2"  # Larger model
VECTOR_DIMENSION = 768  # Adjust accordingly
```

## 🧪 Testing

Run basic tests:
```bash
python -m pytest tests/ -v
```

Or manually test agents:
```python
python src/agents.py
```

## 📊 Visualization

### View RDF Ontology in Protégé
1. Download Protégé: https://protege.stanford.edu/
2. Open `data/fintech.ttl`
3. Select "Window → Tabs → OntoGraf" for visualization
4. Take screenshots for your thesis/CV

### Vector Store Analysis
```python
from src.vector_store import initialize_vector_store

store = initialize_vector_store()
print(f"Products in store: {store.get_index_size()}")
print(f"Vector dimension: {store.index.d}")
```

## 🎓 Academic Significance

### Cold Start Problem
- **Problem**: New users have no history; traditional recommenders fail
- **Solution**: Ontology-based semantic rules map user profiles to products
- **Advantage**: Immediate recommendations without historical data

### Explainability
- **Output**: Natural language + RDF triple citations
- **Advantage**: Meets regulatory requirements (GDPR, fintech regulations)
- **Audit Trail**: Full justification for every recommendation

### Hybrid Approach
- **Vector Search**: Captures semantic similarity
- **RDF Graph**: Enforces domain logic and constraints
- **Weighted Scoring**: Balances both signals intelligently

## 🚀 Deployment

### Local Deployment
```bash
python app.py
```

### Hugging Face Spaces (Docker)
1. Create repo on HF: `your-username/finagent-rec`
2. Create `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```
3. Push to HF Spaces with Docker SDK

### AWS Deployment
```bash
# Install AWS CLI and configure credentials
aws deploy push --s3-location s3://your-bucket/ --application-name finagent-rec

# Deploy with CodeDeploy or Elastic Beanstalk
```

## 📝 Citation

If you use FinAgent-Rec in your research:

```bibtex
@software{finagent_rec_2024,
  title={FinAgent-Rec: Multi-Agent RAG for Explainable Financial Recommendations},
  author={Your Name},
  year={2024},
  url={https://github.com/your-username/FinRec_Agent}
}
```

## 📄 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check the documentation
- Review example code in `src/`

## 🙏 Acknowledgments

Built with:
- [rdflib](https://github.com/RDFLib/rdflib) - RDF ontology management
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search
- [Sentence-Transformers](https://www.sbert.net/) - Text embeddings
- [Gradio](https://gradio.app/) - Web interface

## 🔐 Disclaimer

**IMPORTANT**: These recommendations are generated by AI and are for **educational and informational purposes only**. They should NOT be considered financial advice. Always consult with a qualified financial advisor before making investment decisions.

---

**Last Updated**: April 2024  
**Version**: 1.0.0  
**Status**: Production Ready
