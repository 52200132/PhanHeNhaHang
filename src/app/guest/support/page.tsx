'use client';

import { useState } from 'react';

export default function SupportPage() {
    const [message, setMessage] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Xử lý gửi yêu cầu hỗ trợ
        console.log('Yêu cầu hỗ trợ:', message);
        setMessage('');
    };

    return (
        <div className="container mx-auto">
            <h1 className="text-2xl font-bold mb-6">Yêu cầu hỗ trợ</h1>
            <div className="max-w-2xl mx-auto">
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                            Nội dung yêu cầu
                        </label>
                        <textarea
                            id="message"
                            rows={4}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="Nhập yêu cầu của bạn..."
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
                    >
                        Gửi yêu cầu
                    </button>
                </form>
            </div>
        </div>
    );
}