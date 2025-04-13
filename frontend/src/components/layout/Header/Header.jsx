import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
    return (
        <header className="app-header">
            <div className="app-header__logo">
                <h1>Restaurant Management</h1>
            </div>
            <nav className="app-header__nav">
                <ul>
                    <li>
                        <Link to="/menu">Menu</Link>
                    </li>
                    <li>
                        <Link to="/orders">Orders</Link>
                    </li>
                    <li>
                        <Link to="/kitchen">Kitchen</Link>
                    </li>
                </ul>
            </nav>
            <div className="app-header__actions">
                {/* Add user information, notification, etc. later */}
            </div>
        </header>
    );
};

export default Header;
