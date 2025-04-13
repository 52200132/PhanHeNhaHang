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
        // Set up polling
        const intervalId = setInterval(fetchOrders, 30000);

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
                        Start Preparing
                    </Button>
                );
            case "Đang chế biến":
                return (
                    <Button
                        variant="primary"
                        onClick={() =>
                            handleUpdateStatus(order.kitchen_order_id, "Hoàn thành")
                        }
                    >
                        Mark as Complete
                    </Button>
                );
            default:
                return null;
        }
    };

    if (loading) return <div className="loading">Loading kitchen orders...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="kitchen-page">
            <div className="kitchen-page__header">
                <h2>Kitchen Display</h2>
            </div>

            <div className="kitchen-page__tabs">
                <button
                    className={activeTab === "not_prepared" ? "active" : ""}
                    onClick={() => setActiveTab("not_prepared")}
                >
                    Not Prepared
                </button>
                <button
                    className={activeTab === "in_progress" ? "active" : ""}
                    onClick={() => setActiveTab("in_progress")}
                >
                    In Progress
                </button>
                <button
                    className={activeTab === "completed" ? "active" : ""}
                    onClick={() => setActiveTab("completed")}
                >
                    Completed
                </button>
            </div>

            <div className="kitchen-page__orders">
                {orders.length === 0 ? (
                    <p className="no-orders">No orders in this category</p>
                ) : (
                    orders.map((order) => (
                        <Card
                            key={order.kitchen_order_id}
                            title={`Order #${order.order_id}`}
                            subtitle={`Dish ID: ${order.dish_id}`}
                            className="order-card"
                        >
                            <div className="order-card__details">
                                <div>
                                    <strong>Quantity:</strong> {order.quantity}
                                </div>
                                <div>
                                    <strong>Status:</strong> {order.status}
                                </div>
                                {order.note && (
                                    <div>
                                        <strong>Note:</strong> {order.note}
                                    </div>
                                )}
                                <div>
                                    <strong>Created:</strong>{" "}
                                    {new Date(order.create_at).toLocaleString()}
                                </div>
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
