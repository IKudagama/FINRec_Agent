"""
Financial Domain Knowledge Graph
Comprehensive ontology and knowledge base for financial concepts, relationships, and facts

Uses preferred knowledge resources:
- SKOS (Simple Knowledge Organization System) for concept hierarchy
- FIBO (Financial Industry Business Ontology) concepts
- Domain-specific relationships
"""

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, SKOS
import os
import json
from typing import List, Dict, Set, Tuple
from config import ONTOLOGY_FILE

class FinancialDomainKnowledge:
    """
    Builds and manages the financial domain knowledge graph
    Contains financial concepts, relationships, facts, and reasoning rules
    """
    
    def __init__(self):
        self.graph = Graph()
        
        # Define namespaces
        self.FINTECH = Namespace("http://example.com/fintech/")
        self.FIBO = Namespace("http://spec.edmcouncil.org/fibo/")
        self.SKOS_NS = SKOS
        
        # Bind namespaces
        self.graph.bind("fintech", self.FINTECH)
        self.graph.bind("fibo", self.FIBO)
        self.graph.bind("skos", self.SKOS_NS)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        
        # Knowledge graph file
        self.kg_file = "data/financial_domain_kg.ttl"
    
    # ===========================================================================
    # FINANCIAL CONCEPTS HIERARCHY
    # ===========================================================================
    
    def build_concept_hierarchy(self):
        """
        Build SKOS-based concept hierarchy for financial products
        """
        # Top-level concept: Financial Product
        self.graph.add((self.FINTECH.FinancialProduct, RDF.type, SKOS.Concept))
        self.graph.add((self.FINTECH.FinancialProduct, SKOS.prefLabel, Literal("Financial Product")))
        self.graph.add((self.FINTECH.FinancialProduct, SKOS.definition, 
                       Literal("A financial instrument that represents value and can be traded or invested")))
        
        # Asset Classes
        asset_classes = {
            "Equity": "Ownership stake in a company or fund",
            "Debt": "Obligation to repay borrowed money with interest",
            "Commodity": "Raw material or primary agricultural product",
            "Currency": "Medium of exchange issued by a government",
            "Derivative": "Financial contract derived from underlying asset",
            "RealEstate": "Property and land with buildings"
        }
        
        for asset_class, definition in asset_classes.items():
            asset_uri = self.FINTECH[f"AssetClass_{asset_class}"]
            self.graph.add((asset_uri, RDF.type, SKOS.Concept))
            self.graph.add((asset_uri, SKOS.prefLabel, Literal(asset_class)))
            self.graph.add((asset_uri, SKOS.definition, Literal(definition)))
            self.graph.add((asset_uri, SKOS.broader, self.FINTECH.FinancialProduct))
        
        # Equity Products
        equity_products = {
            "Stock": "Share representing ownership in a company",
            "ETF": "Exchange-traded fund holding multiple securities",
            "MutualFund": "Pooled investment fund managed by professionals",
            "Index": "Composite measure of market performance"
        }
        
        for product, definition in equity_products.items():
            product_uri = self.FINTECH[f"Equity_{product}"]
            self.graph.add((product_uri, RDF.type, SKOS.Concept))
            self.graph.add((product_uri, SKOS.prefLabel, Literal(product)))
            self.graph.add((product_uri, SKOS.definition, Literal(definition)))
            self.graph.add((product_uri, SKOS.broader, self.FINTECH.AssetClass_Equity))
        
        # Debt Products
        debt_products = {
            "Bond": "Fixed-income security representing a loan",
            "GovernmentBond": "Bond issued by a government",
            "CorporateBond": "Bond issued by a corporation",
            "HighYieldBond": "Bond with higher yield but greater default risk",
            "TreasuryBond": "US government bond backed by full faith and credit"
        }
        
        for product, definition in debt_products.items():
            product_uri = self.FINTECH[f"Debt_{product}"]
            self.graph.add((product_uri, RDF.type, SKOS.Concept))
            self.graph.add((product_uri, SKOS.prefLabel, Literal(product)))
            self.graph.add((product_uri, SKOS.definition, Literal(definition)))
            self.graph.add((product_uri, SKOS.broader, self.FINTECH.AssetClass_Debt))
    
    # ===========================================================================
    # FINANCIAL CONCEPTS & DEFINITIONS
    # ===========================================================================
    
    def build_financial_concepts(self):
        """
        Build comprehensive financial concept definitions
        """
        concepts = {
            "Volatility": {
                "definition": "Measure of price fluctuation; standard deviation of returns",
                "range": "0.0 to 1.0+",
                "interpretation": "Higher = more unpredictable, higher risk",
                "implications": ["Higher potential returns", "Higher risk", "Harder to predict"]
            },
            "Liquidity": {
                "definition": "Ability to quickly convert asset to cash without loss",
                "levels": ["High (stocks, ETFs)", "Medium (bonds)", "Low (real estate)"],
                "implications": ["Access to capital", "Flexibility", "Transaction costs"]
            },
            "Risk": {
                "definition": "Probability and magnitude of potential loss",
                "types": ["Market risk", "Credit risk", "Liquidity risk", "Inflation risk"],
                "measurement": "Standard deviation, Beta, Value at Risk (VaR)"
            },
            "Return": {
                "definition": "Profit or gain from an investment",
                "types": ["Capital gains", "Dividends", "Interest"],
                "measurement": "Percentage gain or absolute dollars"
            },
            "Diversification": {
                "definition": "Spreading investments across multiple assets",
                "benefit": "Reduces unsystematic risk",
                "rule": "Don't put all eggs in one basket"
            },
            "Correlation": {
                "definition": "Degree to which two assets move together",
                "range": "-1.0 to 1.0",
                "interpretation": "Lower = better for diversification"
            },
            "SharpeRatio": {
                "definition": "Risk-adjusted return; excess return per unit of risk",
                "formula": "(Return - RiskFreeRate) / Volatility",
                "use": "Comparing risk-adjusted performance"
            },
            "Beta": {
                "definition": "Asset's sensitivity to market movements",
                "range": "Relative to market (1.0 = market)",
                "interpretation": "Beta > 1 = more volatile than market"
            }
        }
        
        for concept_name, concept_data in concepts.items():
            concept_uri = self.FINTECH[f"Concept_{concept_name}"]
            self.graph.add((concept_uri, RDF.type, SKOS.Concept))
            self.graph.add((concept_uri, SKOS.prefLabel, Literal(concept_name)))
            self.graph.add((concept_uri, SKOS.definition, 
                           Literal(concept_data["definition"])))
            
            # Add additional properties as literals
            if "range" in concept_data:
                self.graph.add((concept_uri, self.FINTECH.hasRange, 
                               Literal(concept_data["range"])))
            
            if "interpretation" in concept_data and isinstance(concept_data["interpretation"], str):
                self.graph.add((concept_uri, self.FINTECH.hasInterpretation, 
                               Literal(concept_data["interpretation"])))
    
    # ===========================================================================
    # RELATIONSHIPS & RULES
    # ===========================================================================
    
    def build_financial_relationships(self):
        """
        Build domain relationships that capture financial knowledge
        """
        relationships = [
            # Risk-Return Relationship
            {
                "subject": self.FINTECH.AssetClass_Equity,
                "predicate": self.FINTECH.hasTypicalRiskLevel,
                "object": "High"
            },
            {
                "subject": self.FINTECH.AssetClass_Debt,
                "predicate": self.FINTECH.hasTypicalRiskLevel,
                "object": "Low"
            },
            {
                "subject": self.FINTECH.AssetClass_Commodity,
                "predicate": self.FINTECH.hasTypicalRiskLevel,
                "object": "High"
            },
            
            # Volatility Characteristics
            {
                "subject": self.FINTECH.Equity_Stock,
                "predicate": self.FINTECH.hasTypicalVolatility,
                "object": "0.18"
            },
            {
                "subject": self.FINTECH.Equity_ETF,
                "predicate": self.FINTECH.hasTypicalVolatility,
                "object": "0.12"
            },
            {
                "subject": self.FINTECH.Debt_TreasuryBond,
                "predicate": self.FINTECH.hasTypicalVolatility,
                "object": "0.05"
            },
            
            # Liquidity Rankings
            {
                "subject": self.FINTECH.Equity_Stock,
                "predicate": self.FINTECH.hasLiquidity,
                "object": "High"
            },
            {
                "subject": self.FINTECH.Equity_ETF,
                "predicate": self.FINTECH.hasLiquidity,
                "object": "High"
            },
            {
                "subject": self.FINTECH.Debt_Bond,
                "predicate": self.FINTECH.hasLiquidity,
                "object": "Medium"
            }
        ]
        
        for rel in relationships:
            obj = Literal(rel["object"]) if isinstance(rel["object"], str) else rel["object"]
            self.graph.add((rel["subject"], rel["predicate"], obj))
    
    # ===========================================================================
    # REASONING RULES
    # ===========================================================================
    
    def build_reasoning_rules(self):
        """
        Define rules that guide agent reasoning
        """
        rules = {
            "conservative_investor": {
                "rule": "Conservative investor should prefer low-volatility assets",
                "conditions": ["risk_profile == 'Low'"],
                "actions": ["Prioritize bonds and stable assets", "Avoid stocks and commodities"],
                "exceptions": ["If time horizon > 20 years, equity acceptable"]
            },
            "diversification_rule": {
                "rule": "Well-diversified portfolio reduces unsystematic risk",
                "conditions": ["Portfolio has multiple asset classes"],
                "minimum_diversity": 3,
                "target_correlation": "< 0.3 between assets"
            },
            "risk_return_tradeoff": {
                "rule": "Higher expected returns come with higher risk",
                "conditions": ["Seeking higher returns"],
                "implications": ["Must accept higher volatility", "Potential for larger losses"]
            },
            "liquidity_rule": {
                "rule": "Keep emergency fund in liquid assets",
                "conditions": ["Emergency fund planning"],
                "assets": ["Cash", "Money market", "High-liquidity stocks"],
                "amount": "3-6 months of expenses"
            },
            "inflation_rule": {
                "rule": "Returns must exceed inflation to preserve purchasing power",
                "inflation_rate": "~2-3% per year",
                "implication": "Pure bonds may not beat inflation long-term"
            },
            "time_horizon_rule": {
                "rule": "Investment horizon determines risk capacity",
                "long_term": {
                    "years": "> 10",
                    "capacity": "High risk",
                    "reasoning": "Time to recover from downturns"
                },
                "medium_term": {
                    "years": "5-10",
                    "capacity": "Medium risk"
                },
                "short_term": {
                    "years": "< 5",
                    "capacity": "Low risk",
                    "assets": ["Bonds", "Cash"]
                }
            }
        }
        
        # Store rules as JSON for easy querying
        for rule_name, rule_data in rules.items():
            rule_uri = self.FINTECH[f"Rule_{rule_name}"]
            self.graph.add((rule_uri, RDF.type, self.FINTECH.ReasoningRule))
            self.graph.add((rule_uri, RDFS.label, Literal(rule_name)))
            self.graph.add((rule_uri, self.FINTECH.hasRuleDefinition, 
                           Literal(json.dumps(rule_data))))
    
    # ===========================================================================
    # FINANCIAL METRICS & BENCHMARKS
    # ===========================================================================
    
    def build_financial_metrics(self):
        """
        Define financial metrics and benchmarks
        """
        metrics = {
            "risk_free_rate": {
                "current": 0.045,  # ~4.5% for 10-year Treasury
                "description": "Return on safest investment (US Treasury)"
            },
            "inflation_rate": {
                "current": 0.03,   # ~3%
                "description": "Annual increase in price levels"
            },
            "market_return": {
                "long_term_average": 0.10,  # 10% historical average
                "description": "Average return of broad market index"
            },
            "market_volatility": {
                "long_term_average": 0.15,  # 15% standard deviation
                "description": "Market beta = 1.0"
            }
        }
        
        for metric_name, metric_data in metrics.items():
            metric_uri = self.FINTECH[f"Metric_{metric_name}"]
            self.graph.add((metric_uri, RDF.type, self.FINTECH.FinancialMetric))
            self.graph.add((metric_uri, RDFS.label, Literal(metric_name)))
            self.graph.add((metric_uri, self.FINTECH.hasValue, 
                           Literal(str(metric_data.get("current", metric_data.get("long_term_average"))), 
                                  datatype=XSD.float)))
            self.graph.add((metric_uri, RDFS.comment, 
                           Literal(metric_data["description"])))
    
    # ===========================================================================
    # FACTS DATABASE
    # ===========================================================================
    
    def build_facts_database(self):
        """
        Build a database of financial facts
        """
        facts = [
            # Fact: Stocks are equity
            {
                "triple": ("Stocks", "isTypeOf", "Equity"),
                "context": "Stocks represent ownership in companies"
            },
            # Fact: Bonds are debt
            {
                "triple": ("Bonds", "isTypeOf", "Debt"),
                "context": "Bonds are fixed-income securities"
            },
            # Fact: Historical stock returns
            {
                "triple": ("SP500", "hasHistoricalReturn", 0.10),
                "context": "S&P 500 has returned ~10% annually long-term"
            },
            # Fact: Treasury volatility
            {
                "triple": ("TreasuryBonds", "hasVolatility", 0.05),
                "context": "US Treasuries are very stable"
            },
            # Fact: Diversification reduces risk
            {
                "triple": ("Diversification", "reduces", "UnsystematicRisk"),
                "context": "Spreading across uncorrelated assets reduces idiosyncratic risk"
            },
            # Fact: Younger investors can take more risk
            {
                "triple": ("Age", "inverselyCorrelated", "RiskTolerance"),
                "context": "Longer time horizons allow recovery from downturns"
            },
            # Fact: Market crash recovery
            {
                "triple": ("MarketCrash", "recoversIn", "3-5 years"),
                "context": "Historically, markets recover from major crashes"
            }
        ]
        
        for fact in facts:
            subject, predicate, obj = fact["triple"]
            fact_uri = self.FINTECH[f"Fact_{subject}_{predicate}"]
            self.graph.add((fact_uri, RDF.type, self.FINTECH.FinancialFact))
            self.graph.add((fact_uri, self.FINTECH.hasSubject, Literal(subject)))
            self.graph.add((fact_uri, self.FINTECH.hasPredicate, Literal(predicate)))
            self.graph.add((fact_uri, self.FINTECH.hasObject, Literal(str(obj))))
            self.graph.add((fact_uri, RDFS.comment, Literal(fact["context"])))
    
    # ===========================================================================
    # QUERY METHODS
    # ===========================================================================
    
    def query_concept_hierarchy(self, root_concept: str) -> Dict:
        """
        Query concept hierarchy (SKOS broader/narrower)
        """
        query = f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX fintech: <http://example.com/fintech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?concept ?label ?definition
        WHERE {{
            ?concept skos:broader* fintech:{root_concept} .
            ?concept skos:prefLabel ?label .
            OPTIONAL {{ ?concept skos:definition ?definition }}
        }}
        """
        
        results = {"root": root_concept, "concepts": []}
        for row in self.graph.query(query):
            results["concepts"].append({
                "concept": str(row.concept),
                "label": str(row.label),
                "definition": str(row.definition) if row.definition else None
            })
        return results
    
    def query_asset_characteristics(self, asset_class: str) -> Dict:
        """
        Query characteristics of an asset class
        """
        query = f"""
        PREFIX fintech: <http://example.com/fintech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?property ?value
        WHERE {{
            fintech:AssetClass_{asset_class} ?property ?value .
        }}
        """
        
        results = {"asset_class": asset_class, "characteristics": {}}
        for row in self.graph.query(query):
            prop = str(row.property).split("/")[-1]
            results["characteristics"][prop] = str(row.value)
        return results
    
    def query_reasoning_rules(self, rule_type: str = None) -> List[Dict]:
        """
        Query reasoning rules
        """
        query = """
        PREFIX fintech: <http://example.com/fintech/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?rule ?label ?definition
        WHERE {
            ?rule a fintech:ReasoningRule ;
                  rdfs:label ?label ;
                  fintech:hasRuleDefinition ?definition .
        }
        """
        
        results = []
        for row in self.graph.query(query):
            rule_data = json.loads(str(row.definition))
            results.append({
                "rule": str(row.label),
                "data": rule_data
            })
        return results
    
    def get_metric_value(self, metric_name: str) -> float:
        """
        Get a financial metric value
        """
        query = f"""
        PREFIX fintech: <http://example.com/fintech/>
        
        SELECT ?value
        WHERE {{
            fintech:Metric_{metric_name} fintech:hasValue ?value .
        }}
        """
        
        for row in self.graph.query(query):
            return float(row.value)
        return None
    
    def get_asset_risk_level(self, asset_class: str) -> str:
        """
        Get typical risk level for an asset class
        """
        query = f"""
        PREFIX fintech: <http://example.com/fintech/>
        
        SELECT ?risk
        WHERE {{
            fintech:AssetClass_{asset_class} fintech:hasTypicalRiskLevel ?risk .
        }}
        """
        
        for row in self.graph.query(query):
            return str(row.risk)
        return "Unknown"
    
    # ===========================================================================
    # FILE OPERATIONS
    # ===========================================================================
    
    def save_knowledge_graph(self):
        """
        Save the knowledge graph to file
        """
        os.makedirs(os.path.dirname(self.kg_file), exist_ok=True)
        self.graph.serialize(destination=self.kg_file, format="turtle")
        print(f"✓ Knowledge graph saved to {self.kg_file}")
    
    def load_knowledge_graph(self):
        """
        Load the knowledge graph from file
        """
        if os.path.exists(self.kg_file):
            self.graph.parse(self.kg_file, format="turtle")
            print(f"✓ Knowledge graph loaded from {self.kg_file}")
            return True
        return False
    
    def initialize_knowledge_graph(self):
        """
        Build complete knowledge graph from scratch
        """
        print("Building financial domain knowledge graph...")
        
        self.build_concept_hierarchy()
        print("  ✓ Concept hierarchy built")
        
        self.build_financial_concepts()
        print("  ✓ Financial concepts built")
        
        self.build_financial_relationships()
        print("  ✓ Relationships built")
        
        self.build_reasoning_rules()
        print("  ✓ Reasoning rules built")
        
        self.build_financial_metrics()
        print("  ✓ Financial metrics built")
        
        self.build_facts_database()
        print("  ✓ Facts database built")
        
        self.save_knowledge_graph()
        print(f"\n✓ Knowledge graph complete: {len(self.graph)} triples")
    
    def get_graph(self):
        """
        Return the RDF graph
        """
        return self.graph
    
    def get_graph_size(self) -> int:
        """
        Return the number of triples
        """
        return len(self.graph)


def initialize_financial_knowledge_graph():
    """
    Factory function to initialize or load the knowledge graph
    """
    kg = FinancialDomainKnowledge()
    
    if not os.path.exists(kg.kg_file):
        print("Creating new financial domain knowledge graph...")
        kg.initialize_knowledge_graph()
    else:
        print("Loading existing financial domain knowledge graph...")
        kg.load_knowledge_graph()
    
    return kg


if __name__ == "__main__":
    # Initialize knowledge graph
    kg = FinancialDomainKnowledge()
    kg.initialize_knowledge_graph()
    
    print("\n" + "="*70)
    print("KNOWLEDGE GRAPH EXAMPLES")
    print("="*70)
    
    # Example queries
    print("\n1. Asset Characteristics (Equity):")
    result = kg.query_asset_characteristics("Equity")
    for key, value in result["characteristics"].items():
        print(f"   {key}: {value}")
    
    print("\n2. Asset Risk Levels:")
    for asset in ["Equity", "Debt", "Commodity"]:
        risk = kg.get_asset_risk_level(asset)
        print(f"   {asset}: {risk}")
    
    print("\n3. Financial Metrics:")
    metrics = ["risk_free_rate", "inflation_rate", "market_return"]
    for metric in metrics:
        value = kg.get_metric_value(metric)
        print(f"   {metric}: {value}")
    
    print("\n4. Reasoning Rules:")
    rules = kg.query_reasoning_rules()
    for rule in rules[:3]:
        print(f"   - {rule['rule']}")
