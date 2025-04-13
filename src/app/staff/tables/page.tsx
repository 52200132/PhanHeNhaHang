"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

type Table = {
    id: number;
    name: string;
    status: 'available' | 'occupied';  // Removed 'reserved'
    capacity: number;
};

export default function TablesPage() {
    const router = useRouter();
    const [tables, setTables] = useState<Table[]>([
        { id: 1, name: 'Bàn 1', status: 'available', capacity: 4 },
        { id: 2, name: 'Bàn 2', status: 'occupied', capacity: 6 },
        { id: 3, name: 'Bàn 3', status: 'available', capacity: 2 },
        { id: 4, name: 'Bàn 4', status: 'available', capacity: 8 },
        { id: 5, name: 'Bàn 5', status: 'occupied', capacity: 4 },
        { id: 6, name: 'Bàn 6', status: 'available', capacity: 6 },
    ]);

    const getStatusColor = (status: Table['status']) => {
        switch (status) {
            case 'available':
                return 'bg-green-100 text-green-800';
            case 'occupied':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const getStatusText = (status: Table['status']) => {
        switch (status) {
            case 'available':
                return 'Trống';
            case 'occupied':
                return 'Đang phục vụ';
            default:
                return status;
        }
    };

    // In the JSX, remove the currentGuests display
    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Danh sách bàn ăn</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {tables.map((table) => (
                    <div
                        key={table.id}
                        className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
                    >
                        <div className="flex justify-between items-start mb-4">
                            <h2 className="text-xl font-semibold">{table.name}</h2>
                            <span
                                className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                                    table.status
                                )}`}
                            >
                                {getStatusText(table.status)}
                            </span>
                        </div>
                        <div className="space-y-2 text-gray-600">
                            <p>Sức chứa: {table.capacity} người</p>
                        </div>
                        <div className="mt-4 flex justify-end">
                            {table.status === 'occupied' && (
                                <button
                                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
                                    onClick={() => router.push(`/staff/tables/${table.id}`)}
                                >
                                    Xem chi tiết
                                </button>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}