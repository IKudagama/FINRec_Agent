# FinAgent-Rec Setup & Deployment Guide

## Quick Start (5 minutes)

### 1. Clone and Setup
```bash
cd FinRec_Agent
python -m venv venv
source venv/Scripts/activate  # On Windows
pip install -r requirements.txt
```

### 2. Initialize Data
```bash
python src/ontology.py
python src/vector_store.py
```

### 3. Run the App
```bash
python app.py
```

Open browser: `http://localhost:7860`

---

## Step-by-Step Installation

### Prerequisites
- Python 3.10+
- pip or conda
- ~500MB disk space for models

### Step 1: Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **rdflib** (7.0.0) - RDF ontology management
- **faiss-cpu** (1.7.4) - Vector similarity search
- **sentence-transformers** (2.2.2) - Text embeddings
- **gradio** (4.19.1) - Web interface
- **torch** (2.0.1) - ML framework
- **numpy** (1.24.3) - Numerical computing
- **langchain** (0.1.0) - LLM orchestration (optional, for future extensions)

### Step 3: Initialize Knowledge Graph & Vector Store

```bash
# Create RDF ontology
python src/ontology.py

# Create FAISS vector index
python src/vector_store.py
```

This generates:
- `data/fintech.ttl` - RDF Knowledge Graph
- `data/vector_index.faiss` - FAISS vector index
- `data/vector_index_metadata.json` - Vector metadata

### Step 4: Run Tests (Optional but Recommended)

```bash
# Run comprehensive test suite
python test_demo.py
```

Expected output:
```
✓ Ontology initialized
✓ Vector store initialized  
✓ Agents working correctly
✓ All tests passed!
```

### Step 5: Launch Application

```bash
python app.py
```

Expected output:
```
Running on local URL:  http://0.0.0.0:7860

To create a public link, set `share=True` in `launch()`.
```

Open browser: `http://localhost:7860`

---

## Testing & Validation

### Test Suite
```bash
python test_demo.py
```

Tests:
- RDF Ontology initialization
- FAISS vector indexing
- Multi-agent orchestration
- Recommendation generation
- Explanation quality

### Manual Testing

```python
from src.agents import create_orchestrator, RecommendationRequest
from src.ontology import initialize_ontology
from src.vector_store import initialize_vector_store

# Initialize
ontology = initialize_ontology()
vector_store = initialize_vector_store()
orchestrator = create_orchestrator(ontology, vector_store)

# Test
request = RecommendationRequest(
    user_id="test",
    risk_profile="Medium",
    description="Looking for balanced investments"
)

recommendations = orchestrator.get_recommendations(request)
for rec in recommendations:
    print(f"{rec.product_name}: {rec.overall_score:.1%}")
```

---

## Deployment Options

### Option 1: Local Deployment (Development)

```bash
python app.py
```

- ✓ Full control
- ✓ Easy debugging
- ✓ No cloud costs
- ✗ Not accessible remotely
- ✗ Server must be running

### Option 2: Hugging Face Spaces (Free, Easy)

**Requirements:**
- HF account (free at huggingface.co)
- Docker knowledge (basic)

**Steps:**

1. **Create new Space:**
   - Go to huggingface.co/spaces/new
   - Name: `finagent-rec`
   - License: MIT
   - SDK: Docker

2. **Create `Dockerfile`:**
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   RUN apt-get update && apt-get install -y build-essential
   COPY . .
   RUN pip install --no-cache-dir -r requirements.txt
   EXPOSE 7860
   CMD ["python", "app.py"]
   ```

3. **Push code:**
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/finagent-rec
   git push hf main
   ```

4. **HF automatically builds & deploys!**

**Benefits:**
- ✓ Free hosting
- ✓ Automatic deployment
- ✓ Shareable link
- ✓ No server maintenance
- ✗ Cold start delays (~30s)

### Option 3: AWS (Production)

**Architecture:**
```
API Gateway → Lambda → RDS/DynamoDB
              ↓
           FAISS Index (EBS)
           RDF Graph (S3)
```

**Deployment:**

```bash
# Using AWS SAM (Serverless Application Model)
sam init finagent-rec

# Or Docker + ECS
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker build -t finagent-rec .
docker tag finagent-rec:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/finagent-rec:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/finagent-rec:latest
```

### Option 4: Google Cloud Run

```bash
# Build and deploy
gcloud run deploy finagent-rec \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Configuration

### Customize Scoring Weights

Edit `src/config.py`:

```python
WEIGHTS = {
    "vector_similarity": 0.2,    # Emphasize graph safety
    "graph_consistency": 0.8     # Over semantic similarity
}
```

### Add More Products

Edit `src/config.py` → `MOCK_PRODUCTS`, or:

```python
from src.ontology import FinanceOntology

ontology = FinanceOntology()
ontology.load_ontology()

ontology.add_product(
    product_id="your_product",
    name="Your Product Name",
    description="Description...",
    risk_level="Medium",
    volatility=0.15,
    expected_return=0.08
)

ontology.save_ontology()
```

### Change Embedding Model

Edit `src/config.py`:

```python
# Faster (384 dimensions)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Better quality (384 dimensions)
EMBEDDING_MODEL = "sentence-transformers/paraphrase-MiniLM-L6-v2"

# Best quality (768 dimensions)
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
VECTOR_DIMENSION = 768
```

Then recreate vector store:

```python
from src.vector_store import initialize_vector_store
store = initialize_vector_store(force_recreate=True)
```

---

## Troubleshooting

### Issue: FAISS installation fails
**Solution:**
```bash
pip install faiss-cpu==1.7.4 --no-binary :all:
# Or use GPU version if you have CUDA:
pip install faiss-gpu
```

### Issue: Out of memory with sentence-transformers
**Solution:** Use smaller model
```python
# In config.py
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

### Issue: Port 7860 already in use
**Solution:**
```bash
# Find process using port
netstat -ano | findstr :7860

# Kill it (Windows)
taskkill /PID <PID> /F

# Or use different port in app.py
demo.launch(server_port=7861)
```

### Issue: Gradio not launching
**Solution:**
```bash
# Update Gradio
pip install --upgrade gradio

# Or specify version
pip install gradio==4.19.1
```

### Issue: Knowledge graph empty
**Solution:**
```bash
# Recreate ontology
python src/ontology.py

# Verify:
from src.ontology import initialize_ontology
o = initialize_ontology()
print(o.get_graph_size())  # Should show > 0
```

---

## Performance Optimization

### For Large Datasets (>1000 products)

1. **Use indexed FAISS:**
   ```python
   # In vector_store.py, change:
   index = faiss.IndexIVFFlat(quantizer, VECTOR_DIMENSION, 100)
   # Instead of:
   index = faiss.IndexFlatL2(VECTOR_DIMENSION)
   ```

2. **Enable GPU:**
   ```bash
   pip uninstall faiss-cpu
   pip install faiss-gpu
   ```

3. **Use GraphDB instead of local RDF:**
   ```python
   # See EXTENDING_GUIDE.md for migration
   ```

### For High Concurrency

Use Gunicorn with multiple workers:

```bash
pip install gunicorn

gunicorn app:demo.app -w 4 -b 0.0.0.0:7860
```

---

## Database Migration (Local → GraphDB)

### Prerequisites
- GraphDB (download from ontotext.com)
- GraphDB running on http://localhost:7200

### Steps

1. **Export current ontology:**
   ```python
   from src.ontology import FinanceOntology
   ontology = FinanceOntology()
   ontology.load_ontology()
   ontology.graph.serialize("fintech_backup.ttl")
   ```

2. **Import to GraphDB:**
   - Open http://localhost:7200
   - Create new repository: `fintech`
   - Paste TTL content
   - Save

3. **Update ontology.py:**
   ```python
   # Replace local RDF with GraphDB queries
   from graphdb_client import GraphDBClient
   
   class FinanceOntology:
       def __init__(self):
           self.client = GraphDBClient("http://localhost:7200/repositories/fintech")
   ```

---

## Monitoring & Logging

### Enable Debug Logging

```python
# In app.py, add:
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Monitor Performance

```python
import time

start = time.time()
recommendations = orchestrator.get_recommendations(request)
elapsed = time.time() - start

print(f"Recommendation time: {elapsed:.2f}s")
```

---

## Security Considerations

### Before Production Deployment

1. **Add authentication:**
   ```python
   # demo.launch(auth=("username", "password"))
   ```

2. **Rate limiting:**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

3. **Input validation:**
   ```python
   if not risk_level in ["Low", "Medium", "High"]:
       return "Invalid risk level"
   ```

4. **HTTPS/TLS:**
   - Use reverse proxy (nginx)
   - Enable SSL certificates

5. **Data privacy:**
   - Don't log user queries
   - Anonymize inputs
   - Regular backups

---

## Next Steps

1. ✅ Run `python test_demo.py` to verify everything works
2. ✅ Customize products in `src/config.py`
3. ✅ Adjust weights in `src/config.py` for your use case
4. ✅ Deploy to HF Spaces or AWS for sharing
5. ✅ Integrate into your thesis/CV
6. ✅ Add your own financial data sources

---

## Support & Resources

- **Documentation**: See `README.md`
- **Extension Guide**: See `EXTENDING_GUIDE.md`
- **RDFLib Docs**: https://rdflib.readthedocs.io/
- **FAISS Guide**: https://github.com/facebookresearch/faiss/wiki
- **Gradio Docs**: https://gradio.app/

---

**Version**: 1.0.0  
**Last Updated**: April 2024
