import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css'; // Optional: If you want to add some styling

const Home = () => {
  return (
    <div className="home-container">
      <h1>Welcome to the Library</h1>
      <p>Discover a world of knowledge at your fingertips. Please log in or register to continue.</p>
      <div className="home-buttons">
        <Link to="/login" className="home-button">Login</Link>
        <Link to="/register" className="home-button">Register</Link>
      </div>
    </div>
  );
};

export default Home;