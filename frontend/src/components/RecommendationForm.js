import React from 'react';

function RecommendationForm({
  riskLevel,
  setRiskLevel,
  description,
  setDescription,
  onSubmit,
  loading,
}) {
  return (
    <>
      <div className="form-container">
        <h2>📊 Your Investment Profile</h2>
        <form onSubmit={onSubmit}>
          <div className="form-group">
            <label htmlFor="risk-level">Risk Profile</label>
            <span className="info-text">Select your investment risk tolerance</span>
            <div className="radio-group">
              {['Low', 'Medium', 'High'].map((level) => (
                <div key={level} className="radio-option">
                  <input
                    type="radio"
                    id={`risk-${level}`}
                    name="risk-level"
                    value={level}
                    checked={riskLevel === level}
                    onChange={(e) => setRiskLevel(e.target.value)}
                  />
                  <label htmlFor={`risk-${level}`}>{level}</label>
                </div>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="criteria">Additional Criteria (Optional)</label>
            <span className="info-text">
              Describe any specific preferences or constraints (e.g., "I prefer liquid assets with dividend
              income" or "I'm looking for growth potential")
            </span>
            <textarea
              id="criteria"
              rows="4"
              placeholder="Enter your investment preferences..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={loading}
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? (
              <>
                <span className="loading-spinner"></span>
                Getting Recommendations...
              </>
            ) : (
              '🚀 Get Recommendations'
            )}
          </button>
        </form>
      </div>

      <div className="how-it-works">
        <h2>ℹ️ How It Works</h2>
        <p style={{ marginBottom: '20px', color: '#666', lineHeight: '1.6' }}>
          <strong>FinAgent-Rec</strong> uses a sophisticated multi-agent system to provide personalized
          financial recommendations:
        </p>
        <div className="how-it-works-grid">
          <div className="how-it-works-item">
            <h3>🔍 Retrieval Agent</h3>
            <p>
              Fetches products from both the RDF Knowledge Graph and Vector Store to ensure comprehensive
              coverage of available options.
            </p>
          </div>
          <div className="how-it-works-item">
            <h3>✓ Risk Alignment Agent</h3>
            <p>
              Validates products against your risk profile using ontology rules to ensure recommendations are
              safe and suitable.
            </p>
          </div>
          <div className="how-it-works-item">
            <h3>💡 Reasoning Agent</h3>
            <p>
              Generates natural language explanations citing specific knowledge graph relationships to justify
              each recommendation.
            </p>
          </div>
          <div className="how-it-works-item">
            <h3>📊 Smart Scoring</h3>
            <p>
              Combines Vector Similarity (30%) for semantic relevance with Graph Consistency (70%) for
              ontology alignment.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}

export default RecommendationForm;
