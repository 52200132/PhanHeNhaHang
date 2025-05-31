import React from 'react';
import './OrderDetailsModal.css';

const OrderDetailsModal = ({ order, tableName, onClose }) => {
    // Calculate the total amount
    const calculateTotal = () => {
        if (!order || !order.items) return 0;
        
        return order.items.reduce((total, item) => {
            return total + (parseFloat(item.price || 0) * item.quantity);
        }, 0).toLocaleString('vi-VN');
    };

    // Format date
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleString('vi-VN', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    };

    if (!order) return null;

    return (
        <div className="order-details-modal-overlay">
            <div className="order-details-modal">
                <div className="order-details-header">
                    <h2>Chi tiết đơn hàng</h2>
                    <button className="close-button" onClick={onClose}>×</button>
                </div>
                
                <div className="order-details-content">
                    <div className="order-info">
                        <p><strong>Bàn:</strong> {tableName}</p>
                        <p><strong>Thời gian đặt:</strong> {formatDate(order.timestamp)}</p>
                        <p><strong>Mã đơn hàng:</strong> #{order.orderId}</p>
                    </div>
                    
                    <div className="order-items">
                        <h3>Danh sách món đã đặt</h3>
                        <table className="items-table">
                            <thead>
                                <tr>
                                    <th>Tên món</th>
                                    <th>SL</th>
                                    <th>Đơn giá</th>
                                    <th>Thành tiền</th>
                                </tr>
                            </thead>
                            <tbody>
                                {order.items.map((item, idx) => (
                                    <tr key={idx}>
                                        <td className="item-name">
                                            {item.name}
                                            {item.note && <div className="item-note">Ghi chú: {item.note}</div>}
                                        </td>
                                        <td className="item-quantity">{item.quantity}</td>
                                        <td className="item-price">{parseInt(item.price || 0).toLocaleString('vi-VN')} đ</td>
                                        <td className="item-subtotal">
                                            {(item.quantity * parseFloat(item.price || 0)).toLocaleString('vi-VN')} đ
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    
                    <div className="order-total">
                        <span>Tổng cộng:</span>
                        <span className="total-amount">{calculateTotal()} đ</span>
                    </div>
                    
                    <div className="order-actions">
                        <button className="process-order-btn">Hoàn thành</button>
                        <button className="print-order-btn">In hóa đơn</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OrderDetailsModal;
