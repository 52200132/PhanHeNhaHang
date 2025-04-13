

"use client";

import React, { useState } from 'react';
import Link from 'next/link';

type OrderItem = {
  id: string;
  name: string;
  quantity: number;
  note?: string;
};

type Order = {
  id: string;
  status: 'pending' | 'completed';
  items: OrderItem[];
};

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([
    {
      id: 'DH001',
      status: 'pending',
      items: [
        {
          id: '1',
          name: 'Salad rau củ',
          quantity: 1,
          note: ''
        }
      ]
    }
  ]);

  const updateQuantity = (orderId: string, itemId: string, newQuantity: number) => {
    if (newQuantity < 1) return;
    setOrders(orders.map(order => {
      if (order.id === orderId) {
        return {
          ...order,
          items: order.items.map(item => {
            if (item.id === itemId) {
              return { ...item, quantity: newQuantity };
            }
            return item;
          })
        };
      }
      return order;
    }));
  };

  const removeItem = (orderId: string, itemId: string) => {
    setOrders(orders.map(order => {
      if (order.id === orderId) {
        return {
          ...order,
          items: order.items.filter(item => item.id !== itemId)
        };
      }
      return order;
    }));
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      {orders.map(order => (
        <div key={order.id} className="bg-gray-100 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-4">
            <span>Đơn hàng: {order.id}</span>
            <span className="bg-red-100 text-red-600 px-3 py-1 rounded-full text-sm">
              Chưa thanh toán
            </span>
            <button className="ml-auto bg-white text-black px-4 py-1 rounded-full">
              Thanh toán
            </button>
          </div>

          {order.items.length > 0 ? (
            <table className="w-full">
              <thead>
                <tr>
                  <th className="text-left">Ảnh</th>
                  <th className="text-left">Tên món</th>
                  <th className="text-left">Số lượng</th>
                  <th className="text-left">Ghi chú</th>
                  <th className="text-right">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                {order.items.map(item => (
                  <tr key={item.id} className="border-t">
                    <td className="py-2">
                      <div className="w-12 h-12 bg-gray-200 rounded"></div>
                    </td>
                    <td>{item.name}</td>
                    <td>
                      <div className="inline-flex items-center border rounded">
                        <button
                          className="px-2 py-1"
                          onClick={() => updateQuantity(order.id, item.id, item.quantity - 1)}
                        >
                          -
                        </button>
                        <span className="px-3">{item.quantity}</span>
                        <button
                          className="px-2 py-1"
                          onClick={() => updateQuantity(order.id, item.id, item.quantity + 1)}
                        >
                          +
                        </button>
                      </div>
                    </td>
                    <td>{item.note}</td>
                    <td className="text-right">
                      <button
                        onClick={() => removeItem(order.id, item.id)}
                        className="text-gray-600 hover:text-red-600"
                      >
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="text-center py-8">
              <p className="text-xl text-gray-600 mb-2">Vui lòng thêm món ở mục menu</p>
              <Link href="/guest/menu" className="text-blue-500 hover:underline">
                Đi đến menu
              </Link>
            </div>
          )}

          {order.items.length > 0 && (
            <div className="mt-4 text-center">
              <button className="bg-green-500 text-white px-6 py-2 rounded-full">
                Đặt đơn
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}