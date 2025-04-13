"use client";

import React, { useState } from 'react';

type DishItem = {
    id: number;
    name: string;
    quantity: number;
    completed: boolean;
    priority: number;
};

export default function SummaryPage() {
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
    const [dishes, setDishes] = useState<DishItem[]>([
        { id: 1, name: 'Cơm chiên', quantity: 1, completed: false, priority: 1 },
        { id: 2, name: 'Canh cá chua', quantity: 3, completed: false, priority: 2 },
        { id: 3, name: 'Thịt kho tàu', quantity: 4, completed: true, priority: 3 },
        { id: 4, name: 'Chả cá kho trứng cút', quantity: 6, completed: true, priority: 4 },
        { id: 5, name: 'Gà xối mỡ', quantity: 9, completed: true, priority: 5 },
    ]);

    // Sort dishes first by status (preparing first), then by priority
    const sortedDishes = [...dishes].sort((a, b) => {
        // First sort by status (preparing/completed)
        if (a.completed !== b.completed) {
            return a.completed ? 1 : -1;
        }
        // Then sort by priority based on sortOrder
        return sortOrder === 'asc'
            ? a.priority - b.priority
            : b.priority - a.priority;
    });

    const handleStatusChange = (dishId: number, completed: boolean) => {
        setDishes(dishes.map(dish =>
            dish.id === dishId
                ? { ...dish, completed }
                : dish
        ));
    };

    return (
        <div className="p-6">
            <div className="mb-6">
                <div className="flex items-center gap-4 mb-4">
                    <h1 className="text-2xl font-bold">Danh sách món ăn cần làm</h1>
                    <div className="flex items-center gap-2">
                        <span>Sắp xếp theo:</span>
                        <button
                            onClick={() => setSortOrder('asc')}
                            className={`px-4 py-2 rounded ${sortOrder === 'asc'
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-gray-100'
                                }`}
                        >
                            Ưu tiên thấp - cao
                        </button>
                        <button
                            onClick={() => setSortOrder('desc')}
                            className={`px-4 py-2 rounded ${sortOrder === 'desc'
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-gray-100'
                                }`}
                        >
                            Ưu tiên cao - thấp
                        </button>
                    </div>
                </div>

                <div className="bg-white rounded-lg shadow-md">
                    <table className="min-w-full">
                        <thead>
                            <tr className="border-b">
                                <th className="text-left py-4 px-6">Món</th>
                                <th className="text-center py-4 px-6">Số phần ăn</th>
                                <th className="text-right py-4 px-6">Trạng thái</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sortedDishes.map((dish) => (
                                <tr
                                    key={dish.id}
                                    className={`border-b hover:bg-gray-50 ${dish.completed ? 'bg-gray-50' : ''
                                        }`}
                                >
                                    <td className="py-4 px-6">{dish.name}</td>
                                    <td className="py-4 px-6 text-center">{dish.quantity}</td>
                                    <td className="py-4 px-6 text-right">
                                        <select
                                            value={dish.completed ? 'completed' : 'preparing'}
                                            onChange={(e) => handleStatusChange(
                                                dish.id,
                                                e.target.value === 'completed'
                                            )}
                                            className={`px-3 py-1 border rounded-md ${dish.completed
                                                    ? 'bg-green-50 text-green-800 border-green-200'
                                                    : 'bg-yellow-50 text-yellow-800 border-yellow-200'
                                                }`}
                                        >
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
        </div>
    );
}