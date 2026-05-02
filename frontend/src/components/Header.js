import React from 'react';

function Header() {
  return (
    <div className="header">
      <h1>🏦 FinAgent-Rec</h1>
      <p className="subtitle">
        AI-Powered Multi-Agent RAG System for Financial Recommendations
      </p>
      <p className="description">
        This system uses a Knowledge Graph, Vector Embeddings, and Multi-Agent reasoning to provide
        explainable financial product recommendations tailored to your risk profile.
      </p>
    </div>
  );
}

export default Header;
