"use client";

import React, { useState } from 'react';

type Notification = {
    id: string;
    tableId: number;
    type: 'support' | 'order' | 'payment';
    status: 'pending' | 'processing' | 'completed';
    message: string;
    timestamp: string;
};

export default function NotificationsPage() {
    const [notifications, setNotifications] = useState<Notification[]>([
        {
            id: 'N001',
            tableId: 2,
            type: 'support',
            status: 'pending',
            message: 'Yêu cầu thêm đũa và khăn giấy',
            timestamp: '2024-03-15T10:30:00'
        },
        {
            id: 'N002',
            tableId: 5,
            type: 'order',
            status: 'processing',
            message: 'Gọi thêm món',
            timestamp: '2024-03-15T10:25:00'
        },
        {
            id: 'N003',
            tableId: 1,
            type: 'payment',
            status: 'pending',
            message: 'Yêu cầu thanh toán',
            timestamp: '2024-03-15T10:20:00'
        }
    ]);

    const getTypeIcon = (type: Notification['type']) => {
        switch (type) {
            case 'support':
                return (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                );
            case 'order':
                return (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                    </svg>
                );
            case 'payment':
                return (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                );
        }
    };

    const getStatusColor = (status: Notification['status']) => {
        switch (status) {
            case 'pending':
                return 'bg-yellow-100 text-yellow-800';
            case 'processing':
                return 'bg-blue-100 text-blue-800';
            case 'completed':
                return 'bg-green-100 text-green-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const getStatusText = (status: Notification['status']) => {
        switch (status) {
            case 'pending':
                return 'Chờ xử lý';
            case 'processing':
                return 'Đang xử lý';
            case 'completed':
                return 'Hoàn thành';
            default:
                return status;
        }
    };

    const handleNotification = (notificationId: string, newStatus: Notification['status']) => {
        setNotifications(notifications.map(notification => {
            if (notification.id === notificationId) {
                return { ...notification, status: newStatus };
            }
            return notification;
        }));
    };

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Thông báo yêu cầu hỗ trợ</h1>
            <div className="space-y-4">
                {notifications.map((notification) => (
                    <div
                        key={notification.id}
                        className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow"
                    >
                        <div className="flex items-start gap-4">
                            <div className="flex-shrink-0 p-2 rounded-full bg-gray-100">
                                {getTypeIcon(notification.type)}
                            </div>
                            <div className="flex-grow">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="font-medium">Bàn {notification.tableId}</h3>
                                        <p className="text-gray-600">{notification.message}</p>
                                    </div>
                                    <span
                                        className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                                            notification.status
                                        )}`}
                                    >
                                        {getStatusText(notification.status)}
                                    </span>
                                </div>
                                <div className="mt-2 flex items-center justify-between">
                                    <span className="text-sm text-gray-500">
                                        {new Date(notification.timestamp).toLocaleString('vi-VN')}
                                    </span>
                                    {notification.status === 'pending' && (
                                        <button
                                            onClick={() => handleNotification(notification.id, 'processing')}
                                            className="px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors text-sm"
                                        >
                                            Tiếp nhận
                                        </button>
                                    )}
                                    {notification.status === 'processing' && (
                                        <button
                                            onClick={() => handleNotification(notification.id, 'completed')}
                                            className="px-4 py-1 bg-green-500 text-white rounded hover:bg-green-600 transition-colors text-sm"
                                        >
                                            Hoàn thành
                                        </button>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}