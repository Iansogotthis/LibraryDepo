import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import BorrowedBooks from './components/BorrowedBooks';
import PrivateRoute from './components/PrivateRoute';

const App = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if user is logged in
    axios.get('/api/current_user')
      .then(response => setUser(response.data))
      .catch(() => setUser(null));
  }, []);

  const login = (username, password) => {
    return axios.post('/api/login', { username, password })
      .then(response => {
        setUser(response.data);
        return response.data;
      });
  };

  const logout = () => {
    return axios.post('/api/logout')
      .then(() => setUser(null));
  };

  const register = (username, password, role) => {
    return axios.post('/api/register', { username, password, role })
      .then(response => response.data);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        
        <Route path="/login" element={user ? <Navigate to="/" /> : <Login login={login} />} />
        
        <Route path="/register" element={user ? <Navigate to="/" /> : <Register register={register} />} />
        
        <Route path="/borrowed" element={user ? <BorrowedBooks user={user} logout={logout} /> : <Navigate to="/login" />} />
        
        <Route path="/dashboard" element={user ? <PrivateRoute><Dashboard user={user} logout={logout} /></PrivateRoute> : <Navigate to="/login" />} />
        
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;