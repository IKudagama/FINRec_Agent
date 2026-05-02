"""
Flask API for FinAgent-Rec
Serves recommendations to the React frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ontology import initialize_ontology
from vector_store import initialize_vector_store
from agents import create_orchestrator, RecommendationRequest

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize components on startup
print("Initializing FinAgent-Rec system...")
ontology = initialize_ontology()
vector_store = initialize_vector_store()
orchestrator = create_orchestrator(ontology, vector_store)
print("System ready!")


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'FinAgent-Rec API'
    })


@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """
    Get recommendations based on user input
    
    Request body:
    {
        "risk_level": "Low" | "Medium" | "High",
        "description": "User's additional criteria",
        "num_recommendations": 3
    }
    
    Response:
    {
        "status": "success",
        "data": [
            {
                "product_name": "...",
                "risk_level": "...",
                "overall_score": 0.92,
                "vector_similarity": 0.88,
                "graph_consistency": 0.94,
                "explanation": "...",
                "justification": {
                    "ontology_triples": [...],
                    "matching_criteria": {...}
                }
            },
            ...
        ]
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        
        # Extract and validate inputs
        risk_level = data.get('risk_level', 'Medium')
        description = data.get('description', '')
        num_recommendations = data.get('num_recommendations', 3)
        
        # Validate risk level
        valid_risk_levels = ['Low', 'Medium', 'High']
        if risk_level not in valid_risk_levels:
            return jsonify({
                'status': 'error',
                'message': f'Invalid risk_level. Must be one of {valid_risk_levels}'
            }), 400
        
        # Create recommendation request
        req = RecommendationRequest(
            user_id=f"user_{datetime.now().timestamp()}",
            risk_profile=risk_level,
            description=description if description else "Looking for suitable investments",
            num_recommendations=num_recommendations
        )
        
        # Get recommendations
        recommendations = orchestrator.get_recommendations(req)
        
        if not recommendations:
            return jsonify({
                'status': 'success',
                'data': [],
                'message': 'No suitable recommendations found. Please adjust your criteria.'
            })
        
        # Format results for JSON response
        formatted_recs = []
        for rec in recommendations:
            formatted_recs.append({
                'product_name': rec.product_name,
                'risk_level': rec.risk_level,
                'overall_score': round(rec.overall_score, 3),
                'vector_similarity': round(rec.vector_similarity, 3),
                'graph_consistency': round(rec.graph_consistency, 3),
                'explanation': rec.explanation,
                'justification': {
                    'ontology_triples': rec.justification.get('ontology_triples', []),
                    'matching_criteria': rec.justification.get('matching_criteria', {})
                }
            })
        
        return jsonify({
            'status': 'success',
            'data': formatted_recs
        })
    
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Get list of all available products from the knowledge graph
    
    Response:
    {
        "status": "success",
        "data": [
            {
                "id": "...",
                "name": "...",
                "risk_level": "...",
                "description": "..."
            },
            ...
        ]
    }
    """
    try:
        # Query all products from the ontology
        products = ontology.get_all_products()
        
        formatted_products = []
        for product_id, product_data in products.items():
            formatted_products.append({
                'id': product_id,
                'name': product_data.get('name', ''),
                'risk_level': product_data.get('risk_level', ''),
                'description': product_data.get('description', ''),
                'volatility': product_data.get('volatility'),
                'expected_return': product_data.get('expected_return')
            })
        
        return jsonify({
            'status': 'success',
            'data': formatted_products
        })
    
    except Exception as e:
        print(f"Error in get_products: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/risk-levels', methods=['GET'])
def get_risk_levels():
    """
    Get available risk levels
    """
    return jsonify({
        'status': 'success',
        'data': ['Low', 'Medium', 'High']
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
