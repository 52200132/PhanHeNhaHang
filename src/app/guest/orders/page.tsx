

"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

type OrderItem = {
  id: string;
  name: string;
  quantity: number;
  note?: string;
};

// Add this type at the top with other types
type EditingNote = {
  orderId: string;
  itemId: string;
} | null;

// Update the Order type at the top with other types
type Order = {
  isPaid: any;
  id: string;
  status: 'pending' | 'completed' | 'processing';
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
      ],
      isPaid: undefined
    }
  ]);

  // Add the placeOrder function here with other functions
  const placeOrder = (orderId: string) => {
    setOrders(orders.map(order => {
      if (order.id === orderId) {
        return {
          ...order,
          status: 'processing'
        };
      }
      return order;
    }));
  };

  // Add these states at the component level
  const [editingNote, setEditingNote] = useState<EditingNote>(null);
  const [tempNote, setTempNote] = useState('');

  // Add this state for warning message
  const [noteWarning, setNoteWarning] = useState('');
  
  // Modify the update note function
  const updateNote = (orderId: string, itemId: string, newNote: string) => {
    const wordCount = newNote.trim().split(/\s+/).filter(word => word.length > 0).length;
    
    if (wordCount > 50) {
      setNoteWarning('Ghi chú không được vượt quá 50 từ, Vui lòng nhập lại!');
      return;
    }
    
    setOrders(orders.map(order => {
      if (order.id === orderId) {
        return {
          ...order,
          items: order.items.map(item => {
            if (item.id === itemId) {
              return { ...item, note: newNote };
            }
            return item;
          })
        };
      }
      return order;
    }));
    setEditingNote(null);
    setTempNote('');
    setNoteWarning('');
  };

  const updateQuantity = (orderId: string, itemId: string, newQuantity: number) => {
    if (newQuantity < 1) return;
    
    // Find the order and check its status
    const order = orders.find(o => o.id === orderId);
    if (order?.status === 'processing') return;

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
    const updatedOrders = orders.map(order => {
      if (order.id === orderId) {
        const updatedItems = order.items.filter(item => item.id !== itemId);
        return {
          ...order,
          items: updatedItems
        };
      }
      return order;
    }).filter(order => order.items.length > 0);
    
    setOrders(updatedOrders);
  };

  // Add new state for payment modal
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState('');
  const [currentOrderId, setCurrentOrderId] = useState<string | null>(null);
  
  // Add payment handler function
  const handlePayment = (orderId: string) => {
    setCurrentOrderId(orderId);
    setShowPaymentModal(true);
  };
  
  // Add payment processing function
  // Add new state for success modal
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  
  // Add useEffect for localStorage
  useEffect(() => {
    const savedOrders = localStorage.getItem('orders');
    if (savedOrders) {
      setOrders(JSON.parse(savedOrders));
    }
  }, []);
  
  // Update localStorage whenever orders change
  useEffect(() => {
    localStorage.setItem('orders', JSON.stringify(orders));
  }, [orders]);
  
  // Update the processPayment function
  const processPayment = () => {
    if (!selectedPaymentMethod) return;
    
    setOrders(orders.map(order => {
      if (order.id === currentOrderId) {
        return {
          ...order,
          status: 'processing', // Change status to processing when paid
          isPaid: true
        };
      }
      return order;
    }));
    
    setShowPaymentModal(false);
    setShowSuccessModal(true);
    
    setTimeout(() => {
      setShowSuccessModal(false);
      setSelectedPaymentMethod('');
      setCurrentOrderId(null);
    }, 2000);
  };
  
  // Add success modal to the JSX
  return (
    <>
      <div className="max-w-4xl mx-auto p-4">
        {orders.length > 0 ? (
          orders.map((order) => (
            <div key={order.id} className="bg-gray-100 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-4">
                <span>Đơn hàng: {order.id}</span>
                <div className="flex items-center justify-between w-full">
                  <div className="flex items-center gap-2">
                    <span className={`px-3 py-1 rounded-full text-sm ${
                      order.isPaid 
                        ? 'bg-green-100 text-green-600'
                        : 'bg-red-100 text-red-600'
                    }`}>
                      {order.isPaid ? 'Đã thanh toán' : 'Chưa thanh toán'}
                    </span>
                    {!order.isPaid && (
                      <button 
                        className="bg-white text-black px-4 py-1 rounded-full"
                        onClick={() => handlePayment(order.id)}
                      >
                        Thanh toán
                      </button>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    Trạng thái:
                    <span className={`px-3 py-1 rounded-full text-sm ${
                      order.status === 'pending' 
                        ? 'bg-gray-100 text-gray-600'
                        : 'bg-yellow-100 text-yellow-600'
                    }`}>
                      {order.status === 'pending' ? 'Chờ thao tác' : 'Chờ xử lí'}
                    </span>
                  </div>                  
                </div>
                <div className="flex-grow"></div>
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
                              className={`px-2 py-1 ${order.status === 'processing' ? 'opacity-50 cursor-not-allowed' : ''}`}
                              onClick={() => updateQuantity(order.id, item.id, item.quantity - 1)}
                              disabled={order.status === 'processing'}
                            >
                              -
                            </button>
                            <span className="px-3">{item.quantity}</span>
                            <button
                              className={`px-2 py-1 ${order.status === 'processing' ? 'opacity-50 cursor-not-allowed' : ''}`}
                              onClick={() => updateQuantity(order.id, item.id, item.quantity + 1)}
                              disabled={order.status === 'processing'}
                            >
                              +
                            </button>
                          </div>
                        </td>
                        <td>
                          {editingNote?.orderId === order.id && editingNote?.itemId === item.id ? (
                            <div className="flex gap-2">
                              <input
                                type="text"
                                value={tempNote}
                                onChange={(e) => {
                                  setTempNote(e.target.value);
                                  setNoteWarning('');
                                }}
                                className="border rounded px-2 py-1 text-sm w-full"
                                placeholder="Nhập ghi chú..."
                              />
                              <button
                                onClick={() => updateNote(order.id, item.id, tempNote)}
                                className="bg-green-500 text-white px-2 py-1 rounded text-sm"
                              >
                                Lưu
                              </button>
                              <button
                                onClick={() => {
                                  setEditingNote(null);
                                  setTempNote('');
                                  setNoteWarning('');
                                }}
                                className="bg-gray-500 text-white px-2 py-1 rounded text-sm"
                              >
                                Hủy
                              </button>
                            </div>
                          ) : (
                            <div className="flex items-center gap-2">
                              <span>{item.note || ''}</span>
                              {order.status !== 'processing' && (
                                <button
                                  onClick={() => {
                                    setEditingNote({ orderId: order.id, itemId: item.id });
                                    setTempNote(item.note || '');
                                  }}
                                  className="text-blue-500 text-sm hover:underline"
                                >
                                  {item.note ? 'Sửa ghi chú' : 'Thêm ghi chú'}
                                </button>
                              )}
                            </div>
                          )}
                        </td>
                        <td className="text-right">
                          {order.status !== 'processing' && (
                            <button
                              onClick={() => removeItem(order.id, item.id)}
                              className="text-gray-600 hover:text-red-600"
                            >
                              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                              </svg>
                            </button>
                          )}
                        </td>
                      </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="text-center py-8 bg-gray-50 rounded-lg">
              <p className="text-xl text-gray-600 mb-2">Vui lòng thêm món ở mục menu</p>
              <Link href="/guest/menu" className="text-blue-500 hover:underline">
                Đi đến menu
              </Link>
            </div>
          )}
    
          {order.items.length > 0 && (
            <div className="mt-4 text-center">
              {order.status !== 'processing' && (
                <button 
                  onClick={() => placeOrder(order.id)}
                  className="bg-green-500 text-white px-6 py-2 rounded-full cursor-pointer"
                >
                  Đặt đơn
                </button>
              )}
            </div>
          )}
        </div>
      ))
      ) : (
        <div className="text-center py-8 bg-gray-50 rounded-lg">
          <p className="text-xl text-gray-600 mb-2">Vui lòng thêm món ở mục menu</p>
          <Link href="/guest/menu" className="text-blue-500 hover:underline">
            Đi đến menu
          </Link>
        </div>
      )}
    </div>
  

    {/* Payment modal */}
    {showPaymentModal && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg w-96">
          <h2 className="text-xl font-semibold mb-4">Chọn phương thức thanh toán</h2>
          
          <div className="space-y-3">
            <label className="flex items-center gap-3 p-3 border rounded cursor-pointer">
              <input
                type="radio"
                name="payment"
                value="internet-banking"
                checked={selectedPaymentMethod === 'internet-banking'}
                onChange={(e) => setSelectedPaymentMethod(e.target.value)}
              />
              <div className="flex items-center gap-2">
              <img 
                  src="/vnpay-logo.png" 
                  alt="VNPay" 
                  className="w-6 h-6"
                />
                Internet banking
              </div>
            </label>

            <label className="flex items-center gap-3 p-3 border rounded cursor-pointer">
              <input
                type="radio"
                name="payment"
                value="momo"
                checked={selectedPaymentMethod === 'momo'}
                onChange={(e) => setSelectedPaymentMethod(e.target.value)}
              />
              <div className="flex items-center gap-2">
                <img 
                  src="/momo-logo.png" 
                  alt="Momo" 
                  className="w-6 h-6"
                />
                Momo
              </div>
            </label>
          </div>

          <div className="mt-6 flex justify-end gap-3">
            <button
              onClick={() => setShowPaymentModal(false)}
              className="px-4 py-2 text-gray-600 hover:text-gray-800"
            >
              Hủy
            </button>
            <button
              onClick={processPayment}
              disabled={!selectedPaymentMethod}
              className={`px-4 py-2 rounded ${
                selectedPaymentMethod 
                  ? 'bg-blue-500 text-white hover:bg-blue-600' 
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              Thanh toán ngay
            </button>
          </div>
        </div>
      </div>
    )}
    {/* Success modal */}
    {showSuccessModal && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg w-96 text-center">
          <div className="flex justify-center mb-4">
            <svg className="w-16 h-16 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth="2" 
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-green-600">Thanh toán thành công</h2>
        </div>
      </div>
    )}
  </>
  );
}
