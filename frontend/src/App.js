import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:5000/recommend',
        { query },
        { headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
      );
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  return (
    <div className="container">
      <h1>Grocery Recommendation System</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="query" className="form-label">Search:</label>
          <input type="text" id="query" className="form-control" value={query} onChange={handleQueryChange} />
        </div>
        <button type="submit" className="btn btn-primary">Get Recommendations</button>
      </form>
      <div className="row mt-3">
        {recommendations.map((recommendation, index) => (
          <div key={index} className="col-md-4 mb-4">
            <div className="card">
              <img src={recommendation.Images_url} className="card-img-top" alt={recommendation.Name} />
              <div className="card-body">
                <h5 className="card-title">{recommendation.Name}</h5>
                <p className="card-text">Price: {recommendation.Price}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
