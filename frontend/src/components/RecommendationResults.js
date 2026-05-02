import React, { useState } from 'react';

function RecommendationResults({ recommendations }) {
  const [expandedCards, setExpandedCards] = useState({});

  const toggleExpanded = (index) => {
    setExpandedCards((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const getRiskBadgeClass = (riskLevel) => {
    switch (riskLevel) {
      case 'Low':
        return 'low';
      case 'Medium':
        return 'medium';
      case 'High':
        return 'high';
      default:
        return 'medium';
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '30px' }}>
        <h2 style={{ color: 'white', textAlign: 'center', marginBottom: '10px' }}>
          🎯 Personalized Recommendations
        </h2>
        <p style={{ color: 'rgba(255, 255, 255, 0.9)', textAlign: 'center', fontSize: '0.95em' }}>
          Based on your risk profile and preferences
        </p>
      </div>

      <div className="results-container">
        {recommendations.map((rec, index) => (
          <div key={index} className="recommendation-card">
            <span className="card-rank">#{index + 1} Recommendation</span>

            <h3 className="card-title">{rec.product_name}</h3>

            <span className={`risk-badge ${getRiskBadgeClass(rec.risk_level)}`}>
              {rec.risk_level} Risk
            </span>

            {/* Score Breakdown */}
            <div className="score-breakdown">
              <div className="score-item">
                <span className="score-label">Overall Score</span>
                <span className="score-value">{(rec.overall_score * 100).toFixed(1)}%</span>
              </div>
              <div className="score-bar">
                <div
                  className="score-bar-fill"
                  style={{ width: `${rec.overall_score * 100}%` }}
                ></div>
              </div>

              <div style={{ marginTop: '15px', borderTop: '1px solid #e0e0e0', paddingTop: '15px' }}>
                <div className="score-item">
                  <span className="score-label">Vector Similarity</span>
                  <span className="score-value">{(rec.vector_similarity * 100).toFixed(1)}%</span>
                </div>
                <div className="score-bar">
                  <div
                    className="score-bar-fill"
                    style={{
                      width: `${rec.vector_similarity * 100}%`,
                      background: 'linear-gradient(90deg, #4ecdc4, #44a08d)',
                    }}
                  ></div>
                </div>

                <div className="score-item" style={{ marginTop: '12px' }}>
                  <span className="score-label">Graph Consistency</span>
                  <span className="score-value">{(rec.graph_consistency * 100).toFixed(1)}%</span>
                </div>
                <div className="score-bar">
                  <div
                    className="score-bar-fill"
                    style={{
                      width: `${rec.graph_consistency * 100}%`,
                      background: 'linear-gradient(90deg, #f093fb, #f5576c)',
                    }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Explanation */}
            <div className="explanation-section">
              <h4>💡 Explanation</h4>
              <p className="explanation-text">{rec.explanation}</p>
            </div>

            {/* Justification Collapsible */}
            <div className="justification-section">
              <button
                className="justification-toggle"
                onClick={() => toggleExpanded(index)}
              >
                {expandedCards[index] ? '▼' : '▶'} View Ontology Justification
              </button>

              {expandedCards[index] && (
                <div className="justification-content">
                  {rec.justification.ontology_triples && rec.justification.ontology_triples.length > 0 && (
                    <>
                      <h5>🔗 RDF Triples</h5>
                      <ul>
                        {rec.justification.ontology_triples.map((triple, i) => (
                          <li key={i}>{triple}</li>
                        ))}
                      </ul>
                    </>
                  )}

                  {rec.justification.matching_criteria &&
                    Object.keys(rec.justification.matching_criteria).length > 0 && (
                      <>
                        <h5 style={{ marginTop: '15px' }}>✓ Matching Criteria</h5>
                        <ul className="matching-criteria">
                          {Object.entries(rec.justification.matching_criteria).map(
                            ([criterion, description], i) => (
                              <li key={i}>
                                <strong>{criterion.replace(/_/g, ' ').toUpperCase()}:</strong> {description}
                              </li>
                            )
                          )}
                        </ul>
                      </>
                    )}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Disclaimer */}
      <div
        style={{
          background: 'rgba(255, 255, 255, 0.95)',
          borderRadius: '15px',
          padding: '20px',
          marginTop: '30px',
          textAlign: 'center',
          boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
        }}
      >
        <p style={{ fontSize: '0.9em', color: '#666', lineHeight: '1.6' }}>
          <strong>⚠️ Disclaimer:</strong> These recommendations are generated by AI and are for
          informational and educational purposes only. They should NOT be considered as financial advice.
          Always consult with a qualified financial advisor before making investment decisions.
        </p>
      </div>
    </div>
  );
}

export default RecommendationResults;
