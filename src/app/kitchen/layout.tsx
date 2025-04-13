"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function KitchenLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();

    const menuItems = [
        { href: '/kitchen/dishes', label: 'Danh sách món' },
        { href: '/kitchen/ingredients', label: 'Danh sách nguyên liệu' },
        { href: '/kitchen/orders', label: 'Danh sách hóa đơn' },
        { href: '/kitchen/summary', label: 'Tổng món' },
    ];

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <div className="w-64 bg-white shadow-md">
                <div className="p-4">
                    <h1 className="text-xl font-bold text-gray-800">Quản lý bếp</h1>
                </div>
                <nav className="mt-4">
                    {menuItems.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={`flex items-center px-4 py-3 text-sm ${isActive
                                    ? 'bg-blue-50 text-blue-600 border-r-4 border-blue-600'
                                    : 'text-gray-600 hover:bg-gray-50'}`}
                            >
                                {item.label}
                            </Link>
                        );
                    })}
                </nav>
            </div>

            {/* Main content */}
            <div className="flex-1 overflow-auto p-8">
                {children}
            </div>
        </div>
    );
}