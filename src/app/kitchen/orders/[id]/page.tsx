"use client";

import { useParams } from 'next/navigation';
import React, { useState } from 'react';

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

export default function OrderDetailPage() {
    const params = useParams();
    const orderId = parseInt(params.id as string);

    const [order, setOrder] = useState<Order>({
        id: orderId,
        tableId: 1,
        items: [
            { id: 1, name: 'Phở', quantity: 3, completed: false },
            { id: 2, name: 'Hủ tiếu', quantity: 1, completed: true },
            { id: 3, name: 'Cơm chiên', quantity: 1, completed: true },
            { id: 4, name: 'Rau xào', quantity: 4, completed: true },
            { id: 5, name: 'Canh khổ qua', quantity: 2, completed: true }
        ],
        status: 'preparing',
        timestamp: '2024-03-15T10:30:00'
    });

    const toggleItemStatus = (itemId: number) => {
        setOrder(prev => ({
            ...prev,
            items: prev.items.map(item =>
                item.id === itemId ? { ...item, completed: !item.completed } : item
            )
        }));
    };

    return (
        <div className="p-6">
            <div className="bg-gray-100 rounded-lg p-6">
                <h2 className="text-xl font-bold mb-4">Hóa đơn: HD{order.id.toString().padStart(2, '0')}</h2>
                <div className="bg-white rounded-lg p-4">
                    <table className="min-w-full">
                        <thead>
                            <tr className="border-b border-gray-200">
                                <th className="text-left pb-4">Món</th>
                                <th className="text-left pb-4">Trạng thái</th>
                                <th className="text-center pb-4">Số phần ăn</th>
                                <th className="text-left pb-4">Ghi chú</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {order.items.map((item) => (
                                <tr key={item.id} className="hover:bg-gray-50">
                                    <td className="py-4">{item.name}</td>
                                    <td className="py-4">
                                        <select
                                            value={item.completed ? 'completed' : 'preparing'}
                                            onChange={() => toggleItemStatus(item.id)}
                                            className={`px-3 py-1 border rounded-md ${item.completed
                                                    ? 'bg-green-50 text-green-800 border-green-200'
                                                    : 'bg-yellow-50 text-yellow-800 border-yellow-200'
                                                }`}
                                        >
                                            <option value="preparing">Đang chế biến</option>
                                            <option value="completed">Đã hoàn thành</option>
                                        </select>
                                    </td>
                                    <td className="py-4 text-center">{item.quantity}</td>
                                    <td className="py-4">{item.note || '-'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}