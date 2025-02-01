// src/components/NavBar.js
import { Link } from 'react-router-dom';
import './NavBar.css';

const NavBar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-brand">NavBar</Link>
                <div className="nav-links">
                    <Link to="/signup" className="nav-link">Sign Up</Link>
                    <Link to="/login" className="nav-link">Login</Link>
                    <Link to="/feed" className="nav-link">Feed</Link>
                    <Link to="/profile" className="nav-link">Profile</Link>
                </div>
            </div>
        </nav>
    );
};

export default NavBar;



