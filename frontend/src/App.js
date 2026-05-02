import React, { useState, useEffect } from 'react';
import './App.css';
import RecommendationForm from './components/RecommendationForm';
import RecommendationResults from './components/RecommendationResults';
import Header from './components/Header';

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [riskLevel, setRiskLevel] = useState('Medium');
  const [description, setDescription] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const API_BASE_URL = 'http://localhost:5000/api';

  const handleGetRecommendations = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSubmitted(true);

    try {
      const response = await fetch(`${API_BASE_URL}/recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          risk_level: riskLevel,
          description: description,
          num_recommendations: 3,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.status === 'success') {
        setRecommendations(data.data);
      } else {
        setError(data.message || 'Failed to get recommendations');
        setRecommendations([]);
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.message || 'An error occurred while fetching recommendations');
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />
      <main className="main-container">
        <div className="content-wrapper">
          <RecommendationForm
            riskLevel={riskLevel}
            setRiskLevel={setRiskLevel}
            description={description}
            setDescription={setDescription}
            onSubmit={handleGetRecommendations}
            loading={loading}
          />

          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}

          {submitted && !loading && recommendations.length === 0 && !error && (
            <div className="no-results">
              <p>No recommendations found. Try adjusting your criteria.</p>
            </div>
          )}

          {recommendations.length > 0 && (
            <RecommendationResults recommendations={recommendations} />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
