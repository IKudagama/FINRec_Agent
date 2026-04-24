"""
FAISS Vector Store for storing and retrieving product embeddings
Handles semantic similarity search for financial product descriptions
"""

import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import json
from config import (
    EMBEDDING_MODEL, VECTOR_DIMENSION, VECTOR_INDEX_PATH, MOCK_PRODUCTS
)


class FAISSVectorStore:
    """
    FAISS-based vector store for product embeddings
    """
    
    def __init__(self, model_name: str = EMBEDDING_MODEL, index_path: str = VECTOR_INDEX_PATH):
        self.model_name = model_name
        self.index_path = index_path
        self.embedding_model = SentenceTransformer(model_name)
        self.index = None
        self.product_metadata = []  # List of product metadata (id, name, description)
        self.id_mapping = {}  # Maps index position to product id
        
    def _create_new_index(self):
        """
        Create a new FAISS index
        """
        self.index = faiss.IndexFlatL2(VECTOR_DIMENSION)
    
    def _load_index(self):
        """
        Load an existing FAISS index
        """
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            # Load metadata
            metadata_path = self.index_path.replace('.faiss', '_metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    data = json.load(f)
                    self.product_metadata = data['metadata']
                    self.id_mapping = {int(k): v for k, v in data['id_mapping'].items()}
            print(f"Loaded FAISS index from {self.index_path}")
        else:
            print("Index file not found, creating new index...")
            self._create_new_index()
    
    def _save_index(self):
        """
        Save the FAISS index to disk
        """
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        
        # Save metadata
        metadata_path = self.index_path.replace('.faiss', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump({
                'metadata': self.product_metadata,
                'id_mapping': {str(k): v for k, v in self.id_mapping.items()}
            }, f, indent=2)
        
        print(f"Saved FAISS index to {self.index_path}")
    
    def add_products(self, products: List[Dict]):
        """
        Add products to the vector store
        
        Args:
            products: List of product dictionaries with 'id', 'name', 'description'
        """
        self._create_new_index()
        
        for idx, product in enumerate(products):
            # Embed the product description
            text = f"{product['name']}. {product['description']}"
            embedding = self.embedding_model.encode(text, normalize_embeddings=True)
            embedding = np.array([embedding], dtype=np.float32)
            
            # Add to FAISS index
            self.index.add(embedding)
            
            # Store metadata
            self.product_metadata.append({
                "id": product["id"],
                "name": product["name"],
                "description": product["description"],
                "risk_level": product.get("risk_level", "Unknown"),
                "volatility": product.get("volatility", 0.0),
                "expected_return": product.get("expected_return", 0.0)
            })
            
            # Create mapping
            self.id_mapping[idx] = product["id"]
        
        self._save_index()
        print(f"Added {len(products)} products to vector store")
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Search for similar products
        
        Args:
            query: Search query string
            k: Number of results to return
            
        Returns:
            List of product results with similarity scores
        """
        if self.index is None:
            self._load_index()
        
        # Embed the query
        query_embedding = self.embedding_model.encode(query, normalize_embeddings=True)
        query_embedding = np.array([query_embedding], dtype=np.float32)
        
        # Search the index (L2 distance, so smaller is better)
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for distance, idx in zip(distances[0], indices):
            if idx == -1:  # Invalid index
                continue
            
            # Convert L2 distance to similarity (0-1 range)
            # L2 distance ranges from 0 to 2 for normalized vectors
            similarity = 1 - (distance / 2)
            
            product_id = self.id_mapping.get(int(idx))
            if product_id is not None:
                metadata = self.product_metadata[int(idx)]
                results.append({
                    "product_id": metadata["id"],
                    "name": metadata["name"],
                    "description": metadata["description"],
                    "risk_level": metadata["risk_level"],
                    "volatility": metadata["volatility"],
                    "expected_return": metadata["expected_return"],
                    "similarity_score": float(similarity)
                })
        
        return results
    
    def get_product(self, product_id: str) -> Dict:
        """
        Get a specific product by ID
        """
        for metadata in self.product_metadata:
            if metadata["id"] == product_id:
                return metadata
        return None
    
    def get_all_products(self) -> List[Dict]:
        """
        Get all products in the store
        """
        return self.product_metadata
    
    def get_index_size(self) -> int:
        """
        Get the number of products in the index
        """
        if self.index is None:
            return 0
        return self.index.ntotal


def initialize_vector_store(force_recreate: bool = False) -> FAISSVectorStore:
    """
    Initialize or load the FAISS vector store
    
    Args:
        force_recreate: If True, recreate the index even if it exists
        
    Returns:
        FAISSVectorStore instance
    """
    vector_store = FAISSVectorStore()
    
    if force_recreate or not os.path.exists(vector_store.index_path):
        print("Creating new FAISS index with mock products...")
        vector_store.add_products(MOCK_PRODUCTS)
    else:
        print("Loading existing FAISS index...")
        vector_store._load_index()
    
    return vector_store


if __name__ == "__main__":
    # Test the vector store
    store = FAISSVectorStore()
    store.add_products(MOCK_PRODUCTS)
    
    print(f"\nVector store created with {store.get_index_size()} products")
    
    # Test search
    query = "low risk stable investments"
    results = store.search(query, k=3)
    print(f"\nSearch results for '{query}':")
    for result in results:
        print(f"  - {result['name']}: similarity={result['similarity_score']:.3f}")
