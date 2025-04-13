"use client";

import React from 'react';
import Link from 'next/link';

export default function StaffLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <div className="w-64 bg-white shadow-lg">
                <div className="p-4">
                    <h2 className="text-xl font-bold text-gray-800">Nhân viên phục vụ</h2>
                </div>
                <nav className="mt-4">
                    <Link
                        href="/staff/tables"
                        className="flex items-center px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
                        </svg>
                        Danh sách bàn ăn
                    </Link>
                    <Link
                        href="/staff/notifications"
                        className="flex items-center px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                        </svg>
                        Thông báo yêu cầu hỗ trợ
                    </Link>
                </nav>
            </div>

            {/* Main content */}
            <div className="flex-1 overflow-auto p-8">
                {children}
            </div>
        </div>
    );
}