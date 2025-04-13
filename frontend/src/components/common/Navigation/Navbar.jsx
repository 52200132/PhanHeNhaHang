import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
    return (
        <nav className="navbar">
            <div className="container">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/menu" className="nav-link">Thực Đơn</Link>
                <Link to="/contact" className="nav-link">Contact</Link>
            </div>
        </nav>
    );
};

export default Navigation;