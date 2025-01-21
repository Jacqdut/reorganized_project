import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css"; // Import separate CSS file for styling
import { getUserStatus } from "../api"; // Placeholder for API call to check user status

const Home = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Simulate an API call to check user status
    const checkUserStatus = async () => {
      try {
        const status = await getUserStatus(); // Assume an API call here
        setIsAuthenticated(status.authenticated);
      } catch (err) {
        setError("Error fetching user status");
      } finally {
        setIsLoading(false);
      }
    };

    checkUserStatus();
  }, []);

  const handleLoginRedirect = () => {
    navigate("/login");
  };

  const handleDashboardRedirect = () => {
    navigate("/dashboard");
  };

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Welcome to Quality Assistant</h1>
        <p>
          Predict quality issues and optimize project performance for better
          outcomes.
        </p>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="actions-container">
        {!isAuthenticated ? (
          <>
            <p>You are not logged in. Please login to continue.</p>
            <button onClick={handleLoginRedirect} className="action-btn">
              Login
            </button>
          </>
        ) : (
          <>
            <p>Welcome back! Proceed to your dashboard.</p>
            <button onClick={handleDashboardRedirect} className="action-btn">
              Go to Dashboard
            </button>
          </>
        )}
      </div>

      <footer className="home-footer">
        <p>&copy; 2024 Quality Assistant. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;
