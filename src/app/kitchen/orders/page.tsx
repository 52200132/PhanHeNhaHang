"use client";

import React, { useState } from 'react';
import Link from 'next/link';

type OrderItem = {
    id: number;
    name: string;
    quantity: number;
    note?: string;
    completed: boolean;
};

type Order = {
    id: number;
    tableId: number;
    items: OrderItem[];
    status: 'selecting' | 'pending' | 'preparing' | 'completed';
    timestamp: string;
};

export default function OrdersPage() {
    const [orders, setOrders] = useState<Order[]>([
        {
            id: 1,
            tableId: 1,
            items: [
                { id: 1, name: 'Phở bò', quantity: 2, completed: true },
                { id: 2, name: 'Gỏi cuốn', quantity: 1, note: 'Không hành', completed: true },
                { id: 3, name: 'Cơm sườn', quantity: 2, completed: false },
            ],
            status: 'preparing',
            timestamp: '2024-03-15T10:30:00',
        },
        {
            id: 2,
            tableId: 2,
            items: [
                { id: 4, name: 'Cơm sườn', quantity: 3, completed: true },
                { id: 5, name: 'Chả giò', quantity: 2, completed: true },
            ],
            status: 'completed',
            timestamp: '2024-03-15T10:25:00',
        },
    ]);

    const getStatusColor = (status: Order['status']) => {
        switch (status) {
            case 'selecting':
                return 'bg-purple-100 text-purple-800';
            case 'pending':
                return 'bg-yellow-100 text-yellow-800';
            case 'preparing':
                return 'bg-blue-100 text-blue-800';
            case 'completed':
                return 'bg-green-100 text-green-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const getStatusText = (status: Order['status']) => {
        switch (status) {
            case 'selecting':
                return 'Đang chọn món';
            case 'pending':
                return 'Chờ xử lí';
            case 'preparing':
                return 'Đang chế biến';
            case 'completed':
                return 'Hoàn thành';
            default:
                return status;
        }
    };

    const updateOrderStatus = (orderId: number) => {
        setOrders(orders.map(order => {
            if (order.id === orderId) {
                const statusFlow: Order['status'][] = ['selecting', 'pending', 'preparing', 'completed'];
                const currentIndex = statusFlow.indexOf(order.status);
                const nextStatus = statusFlow[currentIndex + 1];

                return nextStatus ? { ...order, status: nextStatus } : order;
            }
            return order;
        }));
    };

    return (
        <div className="p-6">
            <div className="bg-gray-100 rounded-lg p-6">
                <table className="min-w-full">
                    <thead>
                        <tr className="border-b border-gray-200">
                            <th className="text-left pb-4">Mã hóa đơn</th>
                            <th className="text-left pb-4">Bàn</th>
                            <th className="text-left pb-4">Món đã hoàn thành</th>
                            <th className="text-left pb-4">Món lại</th>
                            <th className="text-right pb-4">Trạng thái</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {orders.map((order) => (
                            <tr key={order.id} className="hover:bg-gray-50">
                                <td className="py-4">
                                    <Link href={`/kitchen/orders/${order.id}`} className="text-blue-600 hover:text-blue-800">
                                        HD{order.id.toString().padStart(2, '0')}
                                    </Link>
                                </td>
                                <td className="py-4">{order.tableId.toString().padStart(2, '0')}</td>
                                <td className="py-4">
                                    {order.items.filter(item => item.completed).length}/{order.items.length}
                                </td>
                                <td className="py-4">
                                    {order.items.filter(item => !item.completed).length}/{order.items.length}
                                </td>
                                <td className="py-4 text-right">
                                    <select
                                        value={order.status}
                                        onChange={(e) => updateOrderStatus(order.id)}
                                        className="px-3 py-1 border rounded-md bg-white"
                                    >
                                        <option value="selecting">Đang chọn món</option>
                                        <option value="pending">Chờ xử lí</option>
                                        <option value="preparing">Đang chế biến</option>
                                        <option value="completed">Hoàn thành</option>
                                    </select>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}