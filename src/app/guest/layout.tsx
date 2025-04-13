'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function ClientLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();

    const menuItems = [
        { href: '/guest/menu', label: 'Thực đơn' },
        { href: '/guest/orders', label: 'Đơn hàng' },
        { href: '/guest/support', label: 'Yêu cầu nhân viên hỗ trợ' },
    ];

    return (
        <div className="flex min-h-screen">
            {/* Sidebar */}
            <aside className="w-64 bg-gray-800 text-white p-4">
                <nav className="space-y-2">
                    {menuItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`block px-4 py-2 rounded hover:bg-gray-700 transition-colors ${pathname === item.href ? 'bg-gray-700' : ''}`}
                        >
                            {item.label}
                        </Link>
                    ))}
                </nav>
            </aside>

            {/* Main content */}
            <main className="flex-1 p-8">
                {children}
            </main>
        </div>
    );
}