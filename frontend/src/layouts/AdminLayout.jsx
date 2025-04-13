import React from 'react';
import { Outlet } from 'react-router-dom';
import AdminHeader from '../components/layout/AdminHeader';

const AdminLayout = () => {
    return (
        <div className="admin-container">
            <AdminHeader />
            <main className="admin-content">
                <Outlet />
            </main>
            <footer className="admin-footer">
                &copy; 2023 Restaurant Management System - Admin
            </footer>
        </div>
    );
};

export default AdminLayout;
