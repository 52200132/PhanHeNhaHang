import React, { useState, useEffect } from "react";
import {
    getKitchenOrders,
    updateOrderStatus,
} from "../../services/kitchenService";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";
import "./KitchenPage.css";

const KitchenPage = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState("not_prepared");
    const [sortBy, setSortBy] = useState("time"); // 'time' or 'priority'

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                setLoading(true);
                const response = await getKitchenOrders(activeTab);
                setOrders(response.data || []);
            } catch (err) {
                setError("Failed to load kitchen orders");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
        // Set up polling with more frequent updates for active orders
        const intervalId = setInterval(fetchOrders, activeTab === "in_progress" ? 15000 : 30000);

        return () => clearInterval(intervalId);
    }, [activeTab]);

    const handleUpdateStatus = async (orderId, newStatus) => {
        try {
            await updateOrderStatus(orderId, newStatus);
            // Update local state
            setOrders((prevOrders) =>
                prevOrders
                    .map((order) =>
                        order.kitchen_order_id === orderId
                            ? { ...order, status: newStatus }
                            : order
                    )
                    .filter((order) =>
                        activeTab === "not_prepared" && newStatus !== "Chưa chuẩn bị"
                            ? order.kitchen_order_id !== orderId
                            : true
                    )
            );
        } catch (err) {
            setError("Failed to update order status");
            console.error(err);
        }
    };

    const getActionButtons = (order) => {
        switch (order.status) {
            case "Chưa chuẩn bị":
                return (
                    <Button
                        variant="primary"
                        onClick={() =>
                            handleUpdateStatus(order.kitchen_order_id, "Đang chế biến")
                        }
                    >
                        Bắt đầu chế biến
                    </Button>
                );
            case "Đang chế biến":
                return (
                    <Button
                        variant="success"
                        onClick={() =>
                            handleUpdateStatus(order.kitchen_order_id, "Hoàn thành")
                        }
                    >
                        Hoàn thành
                    </Button>
                );
            case "Hoàn thành":
                return (
                    <div className="completed-time">
                        Hoàn thành lúc: {new Date(order.updated_at || Date.now()).toLocaleTimeString()}
                    </div>
                );
            default:
                return null;
        }
    };

    const getStatusBadge = (status) => {
        let badgeClass = "status-badge";
        
        switch (status) {
            case "Chưa chuẩn bị":
                badgeClass += " status-new";
                break;
            case "Đang chế biến":
                badgeClass += " status-progress";
                break;
            case "Hoàn thành":
                badgeClass += " status-completed";
                break;
            default:
                break;
        }
        
        return <span className={badgeClass}>{status}</span>;
    };

    const getTimeSince = (dateString) => {
        const created = new Date(dateString);
        const now = new Date();
        const diffMinutes = Math.floor((now - created) / (1000 * 60));
        
        if (diffMinutes < 1) return "Vừa xong";
        if (diffMinutes < 60) return `${diffMinutes} phút trước`;
        return `${Math.floor(diffMinutes / 60)} giờ ${diffMinutes % 60} phút trước`;
    };

    const sortOrders = (ordersToSort) => {
        if (sortBy === "time") {
            return [...ordersToSort].sort((a, b) => new Date(a.create_at) - new Date(b.create_at));
        } else if (sortBy === "priority") {
            return [...ordersToSort].sort((a, b) => (b.priority || 0) - (a.priority || 0));
        }
        return ordersToSort;
    };

    if (loading) return <div className="loading">Đang tải danh sách món ăn...</div>;
    if (error) return <div className="error">{error}</div>;

    const sortedOrders = sortOrders(orders);

    return (
        <div className="kitchen-page">
            <div className="kitchen-page__header">
                <h2>Hệ thống hiển thị bếp</h2>
            </div>

            <div className="kitchen-page__tabs">
                <button
                    className={activeTab === "not_prepared" ? "active" : ""}
                    onClick={() => setActiveTab("not_prepared")}
                >
                    Chưa chuẩn bị
                </button>
                <button
                    className={activeTab === "in_progress" ? "active" : ""}
                    onClick={() => setActiveTab("in_progress")}
                >
                    Đang chế biến
                </button>
                <button
                    className={activeTab === "completed" ? "active" : ""}
                    onClick={() => setActiveTab("completed")}
                >
                    Hoàn thành
                </button>
            </div>

            <div className="kitchen-page__sort">
                <span>Sắp xếp theo: </span>
                <button 
                    className={sortBy === "time" ? "active" : ""} 
                    onClick={() => setSortBy("time")}
                >
                    Thời gian
                </button>
                <button 
                    className={sortBy === "priority" ? "active" : ""} 
                    onClick={() => setSortBy("priority")}
                >
                    Ưu tiên
                </button>
            </div>

            <div className="kitchen-page__orders">
                {sortedOrders.length === 0 ? (
                    <p className="no-orders">Không có món ăn nào trong danh mục này</p>
                ) : (
                    sortedOrders.map((order) => (
                        <Card
                            key={order.kitchen_order_id}
                            title={`Đơn #${order.order_id}`}
                            subtitle={`${order.dish_name || `Món #${order.dish_id}`}`}
                            className={`order-card ${order.status === "Đang chế biến" ? "in-progress" : ""}`}
                        >
                            <div className="order-card__details">
                                <div className="order-header">
                                    <div className="order-quantity">
                                        <strong>Số lượng:</strong> {order.quantity}
                                    </div>
                                    <div className="order-status">
                                        {getStatusBadge(order.status)}
                                    </div>
                                </div>
                                
                                {order.note && (
                                    <div className="order-note">
                                        <strong>Ghi chú:</strong> {order.note}
                                    </div>
                                )}
                                
                                <div className="order-time">
                                    <div><strong>Đã tạo:</strong> {getTimeSince(order.create_at)}</div>
                                    <div className="time-exact">({new Date(order.create_at).toLocaleString()})</div>
                                </div>
                                
                                {order.status === "Đang chế biến" && (
                                    <div className="preparation-time">
                                        <strong>Thời gian chuẩn bị:</strong> {getTimeSince(order.updated_at || order.create_at)}
                                    </div>
                                )}
                            </div>
                            <div className="order-card__actions">
                                {getActionButtons(order)}
                            </div>
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
};

export default KitchenPage;
