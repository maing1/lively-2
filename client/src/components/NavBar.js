// src/components/NavBar.js
import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import './NavBar.css';

const NavBar = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const history = useHistory();

    useEffect(() => {
        // Check if user is logged in by verifying if token exists
        const token = localStorage.getItem('token');
        setIsAuthenticated(!!token);

        // Add event listener for storage changes
        const handleStorageChange = () => {
            const token = localStorage.getItem('token');
            setIsAuthenticated(!!token);
        };

        window.addEventListener('storage', handleStorageChange);
        
        // Also listen for a custom event that we'll dispatch after login
        window.addEventListener('authChange', handleStorageChange);

        return () => {
            window.removeEventListener('storage', handleStorageChange);
            window.removeEventListener('authChange', handleStorageChange);
        };
    }, []);

    const handleLogout = (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        setIsAuthenticated(false);
        history.push('/login');
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-brand">Lively</Link>
                <div className="nav-links">
                    {!isAuthenticated ? (
                        <>
                            <Link to="/signup" className="nav-link">Sign Up</Link>
                            <Link to="/login" className="nav-link">Login</Link>
                        </>
                    ) : (
                        <>
                            <Link to="/feed" className="nav-link">Feed</Link>
                            <Link to="/profile" className="nav-link">Profile</Link>
                            <a href="#" onClick={handleLogout} className="nav-link">Logout</a>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default NavBar;



