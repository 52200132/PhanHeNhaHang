"use client";

import React, { useState } from 'react';
import { useParams } from 'next/navigation';

type OrderItem = {
    id: number;
    name: string;
    quantity: number;
    status: 'pending' | 'cooking' | 'completed' | 'cancelled';
    price: number;
    image: string;
};

export default function TableDetailPage() {
    const params = useParams();
    const tableId = parseInt(params.id as string);

    const [orderItems, setOrderItems] = useState<OrderItem[]>([
        {
            id: 1,
            name: 'Salad rau củ',
            quantity: 1,
            status: 'cooking',
            price: 35000,
            image: '/images/salad.jpg'
        },
        {
            id: 2,
            name: 'Bò bít tết',
            quantity: 2,
            status: 'pending',
            price: 150000,
            image: '/images/beefsteak.jpg'
        },
        {
            id: 3,
            name: 'Rau xào',
            quantity: 2,
            status: 'completed',
            price: 25000,
            image: '/images/vegetables.jpg'
        }
    ]);

    const getStatusColor = (status: OrderItem['status']) => {
        switch (status) {
            case 'pending':
                return 'bg-yellow-100 text-yellow-800';
            case 'cooking':
                return 'bg-blue-100 text-blue-800';
            case 'completed':
                return 'bg-green-100 text-green-800';
            case 'cancelled':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const getStatusText = (status: OrderItem['status']) => {
        switch (status) {
            case 'pending':
                return 'Chờ chế biến';
            case 'cooking':
                return 'Đang chế biến';
            case 'completed':
                return 'Hoàn thành';
            case 'cancelled':
                return 'Đã hủy';
            default:
                return status;
        }
    };

    const updateItemStatus = (itemId: number, newStatus: OrderItem['status']) => {
        setOrderItems(items =>
            items.map(item =>
                item.id === itemId ? { ...item, status: newStatus } : item
            )
        );
    };

    const getTotalAmount = () => {
        return orderItems.reduce((total, item) => total + (item.price * item.quantity), 0);
    };

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold">Chi tiết Bàn {tableId}</h1>
                <div className="text-gray-600">
                    <p>Tổng tiền: {getTotalAmount().toLocaleString('vi-VN')}đ</p>
                </div>
            </div>

            <div className="bg-white rounded-lg shadow-md overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Món ăn</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Số lượng</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Đơn giá</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Thành tiền</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trạng thái</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Thao tác</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {orderItems.map((item) => (
                            <tr key={item.id}>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        <div className="h-10 w-10 flex-shrink-0">
                                            <img className="h-10 w-10 rounded-full object-cover" src={item.image} alt={item.name} />
                                        </div>
                                        <div className="ml-4">
                                            <div className="text-sm font-medium text-gray-900">{item.name}</div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {item.quantity}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {item.price.toLocaleString('vi-VN')}đ
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {(item.price * item.quantity).toLocaleString('vi-VN')}đ
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(item.status)}`}>
                                        {getStatusText(item.status)}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    {item.status === 'pending' && (
                                        <button
                                            onClick={() => updateItemStatus(item.id, 'cooking')}
                                            className="text-blue-600 hover:text-blue-900 mr-2"
                                        >
                                            Bắt đầu chế biến
                                        </button>
                                    )}
                                    {item.status === 'cooking' && (
                                        <button
                                            onClick={() => updateItemStatus(item.id, 'completed')}
                                            className="text-green-600 hover:text-green-900 mr-2"
                                        >
                                            Hoàn thành
                                        </button>
                                    )}
                                    {(item.status === 'pending' || item.status === 'cooking') && (
                                        <button
                                            onClick={() => updateItemStatus(item.id, 'cancelled')}
                                            className="text-red-600 hover:text-red-900"
                                        >
                                            Hủy
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}