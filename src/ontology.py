"""
RDF Ontology Creation and Management using rdflib
Defines the financial knowledge graph structure
"""

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import os
from config import ONTOLOGY_FILE, ONTOLOGY_FORMAT, MOCK_PRODUCTS

class FinanceOntology:
    """
    Creates and manages the financial ontology using RDF
    """
    
    def __init__(self, ontology_file: str = ONTOLOGY_FILE):
        self.ontology_file = ontology_file
        self.graph = Graph()
        
        # Define namespaces
        self.FINTECH = Namespace("http://example.com/fintech/")
        self.FOAF = Namespace("http://xmlns.com/foaf/0.1/")
        
        # Bind namespaces
        self.graph.bind("fintech", self.FINTECH)
        self.graph.bind("foaf", self.FOAF)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        
    def create_ontology_schema(self):
        """
        Create the base ontology schema with classes and properties
        """
        # Define classes
        self.graph.add((self.FINTECH.Product, RDF.type, RDFS.Class))
        self.graph.add((self.FINTECH.Product, RDFS.label, Literal("Financial Product")))
        self.graph.add((self.FINTECH.Product, RDFS.comment, Literal("A financial instrument or investment product")))
        
        self.graph.add((self.FINTECH.RiskLevel, RDF.type, RDFS.Class))
        self.graph.add((self.FINTECH.RiskLevel, RDFS.label, Literal("Risk Level")))
        self.graph.add((self.FINTECH.RiskLevel, RDFS.comment, Literal("Classification of investment risk")))
        
        self.graph.add((self.FINTECH.User, RDF.type, RDFS.Class))
        self.graph.add((self.FINTECH.User, RDFS.label, Literal("User")))
        self.graph.add((self.FINTECH.User, RDFS.comment, Literal("An investor or user of financial products")))
        
        # Define properties
        self.graph.add((self.FINTECH.is_suitable_for, RDF.type, RDFS.Property))
        self.graph.add((self.FINTECH.is_suitable_for, RDFS.domain, self.FINTECH.Product))
        self.graph.add((self.FINTECH.is_suitable_for, RDFS.range, self.FINTECH.RiskLevel))
        self.graph.add((self.FINTECH.is_suitable_for, RDFS.label, Literal("Is Suitable For")))
        
        self.graph.add((self.FINTECH.has_volatility, RDF.type, RDFS.Property))
        self.graph.add((self.FINTECH.has_volatility, RDFS.domain, self.FINTECH.Product))
        self.graph.add((self.FINTECH.has_volatility, RDFS.range, XSD.float))
        self.graph.add((self.FINTECH.has_volatility, RDFS.label, Literal("Has Volatility")))
        
        self.graph.add((self.FINTECH.has_expected_return, RDF.type, RDFS.Property))
        self.graph.add((self.FINTECH.has_expected_return, RDFS.domain, self.FINTECH.Product))
        self.graph.add((self.FINTECH.has_expected_return, RDFS.range, XSD.float))
        
        self.graph.add((self.FINTECH.has_description, RDF.type, RDFS.Property))
        self.graph.add((self.FINTECH.has_description, RDFS.domain, self.FINTECH.Product))
        self.graph.add((self.FINTECH.has_description, RDFS.range, XSD.string))
        
        self.graph.add((self.FINTECH.has_risk_profile, RDF.type, RDFS.Property))
        self.graph.add((self.FINTECH.has_risk_profile, RDFS.domain, self.FINTECH.User))
        self.graph.add((self.FINTECH.has_risk_profile, RDFS.range, self.FINTECH.RiskLevel))
        
    def create_risk_levels(self):
        """
        Create risk level instances
        """
        risk_levels = ["Low", "Medium", "High"]
        for level in risk_levels:
            risk_uri = self.FINTECH[f"RiskLevel_{level}"]
            self.graph.add((risk_uri, RDF.type, self.FINTECH.RiskLevel))
            self.graph.add((risk_uri, RDFS.label, Literal(level)))
    
    def add_product(self, product_id: str, name: str, description: str, 
                   risk_level: str, volatility: float, expected_return: float):
        """
        Add a product instance to the ontology
        """
        product_uri = self.FINTECH[f"Product_{product_id}"]
        risk_uri = self.FINTECH[f"RiskLevel_{risk_level}"]
        
        # Add product triples
        self.graph.add((product_uri, RDF.type, self.FINTECH.Product))
        self.graph.add((product_uri, RDFS.label, Literal(name)))
        self.graph.add((product_uri, self.FINTECH.has_description, Literal(description)))
        self.graph.add((product_uri, self.FINTECH.is_suitable_for, risk_uri))
        self.graph.add((product_uri, self.FINTECH.has_volatility, Literal(volatility, datatype=XSD.float)))
        self.graph.add((product_uri, self.FINTECH.has_expected_return, Literal(expected_return, datatype=XSD.float)))
        
    def add_user(self, user_id: str, name: str, risk_profile: str):
        """
        Add a user instance to the ontology
        """
        user_uri = self.FINTECH[f"User_{user_id}"]
        risk_uri = self.FINTECH[f"RiskLevel_{risk_profile}"]
        
        self.graph.add((user_uri, RDF.type, self.FINTECH.User))
        self.graph.add((user_uri, RDFS.label, Literal(name)))
        self.graph.add((user_uri, self.FINTECH.has_risk_profile, risk_uri))
    
    def query_products_by_risk(self, risk_level: str) -> list:
        """
        Query products suitable for a specific risk level
        """
        query = f"""
        PREFIX fintech: <http://example.com/fintech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?product ?name ?description ?volatility ?return
        WHERE {{
            ?product a fintech:Product ;
                     rdfs:label ?name ;
                     fintech:has_description ?description ;
                     fintech:has_volatility ?volatility ;
                     fintech:has_expected_return ?return ;
                     fintech:is_suitable_for fintech:RiskLevel_{risk_level} .
        }}
        """
        results = []
        for row in self.graph.query(query):
            results.append({
                "product": str(row.product),
                "name": str(row.name),
                "description": str(row.description),
                "volatility": float(row.volatility),
                "expected_return": float(row['return'])
            })
        return results
    
    def get_all_products(self) -> dict:
        """
        Get all products from the ontology
        """
        query = """
        PREFIX fintech: <http://example.com/fintech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?product ?name ?description ?volatility ?return ?riskLevel
        WHERE {
            ?product a fintech:Product ;
                     rdfs:label ?name ;
                     fintech:has_description ?description ;
                     fintech:has_volatility ?volatility ;
                     fintech:has_expected_return ?return ;
                     fintech:is_suitable_for ?riskURI .
            ?riskURI rdfs:label ?riskLevel .
        }
        """
        products = {}
        for row in self.graph.query(query):
            product_id = str(row.product).split("/")[-1]
            products[product_id] = {
                "id": product_id,
                "name": str(row.name),
                "description": str(row.description),
                "volatility": float(row.volatility),
                "expected_return": float(row['return']),
                "risk_level": str(row.riskLevel)
            }
        return products
    
    def save_ontology(self):
        """
        Save the ontology to a file
        """
        os.makedirs(os.path.dirname(self.ontology_file), exist_ok=True)
        self.graph.serialize(destination=self.ontology_file, format=ONTOLOGY_FORMAT)
        print(f"Ontology saved to {self.ontology_file}")
    
    def load_ontology(self):
        """
        Load the ontology from a file
        """
        if os.path.exists(self.ontology_file):
            self.graph.parse(self.ontology_file, format=ONTOLOGY_FORMAT)
            print(f"Ontology loaded from {self.ontology_file}")
        else:
            print(f"Ontology file not found: {self.ontology_file}")
    
    def initialize_with_mock_data(self):
        """
        Initialize the ontology with mock data
        """
        self.create_ontology_schema()
        self.create_risk_levels()
        
        for product in MOCK_PRODUCTS:
            self.add_product(
                product["id"],
                product["name"],
                product["description"],
                product["risk_level"],
                product["volatility"],
                product["expected_return"]
            )
        
        # Add a sample user
        self.add_user("user_001", "John Doe", "Medium")
        
        self.save_ontology()
    
    def get_graph(self):
        """
        Return the RDF graph
        """
        return self.graph
    
    def get_graph_size(self) -> int:
        """
        Return the number of triples in the graph
        """
        return len(self.graph)


def initialize_ontology():
    """
    Initialize or load the ontology
    """
    ontology = FinanceOntology()
    
    if not os.path.exists(ontology.ontology_file):
        print("Creating new ontology with mock data...")
        ontology.initialize_with_mock_data()
    else:
        print("Loading existing ontology...")
        ontology.load_ontology()
    
    return ontology


if __name__ == "__main__":
    ontology = FinanceOntology()
    ontology.initialize_with_mock_data()
    print(f"Ontology created with {ontology.get_graph_size()} triples")
    
    # Example query
    results = ontology.query_products_by_risk("Medium")
    print("\nProducts suitable for Medium risk level:")
    for product in results:
        print(f"  - {product['name']}: volatility={product['volatility']}")
