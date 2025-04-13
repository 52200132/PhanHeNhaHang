import axios from 'axios';

const API_URL = 'http://localhost:8003/api/v1';

export const getKitchenOrders = async (statusFilter = '') => {
    try {
        let url = `${API_URL}/kitchen_orders`;

        if (statusFilter) {
            // Map frontend status to backend status
            const statusMap = {
                'not_prepared': 'Chưa chuẩn bị',
                'in_progress': 'Đang chế biến',
                'completed': 'Hoàn thành'
            };

            const backendStatus = statusMap[statusFilter];
            if (backendStatus) {
                url = `${API_URL}/kitchen_orders/status/${backendStatus}`;
            }
        }

        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error('Error fetching kitchen orders:', error);
        throw error;
    }
};

export const getKitchenOrderById = async (kitchenOrderId) => {
    try {
        const response = await axios.get(`${API_URL}/kitchen_orders/${kitchenOrderId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching kitchen order with ID ${kitchenOrderId}:`, error);
        throw error;
    }
};

export const createKitchenOrder = async (kitchenOrderData) => {
    try {
        const response = await axios.post(`${API_URL}/kitchen_orders`, kitchenOrderData);
        return response.data;
    } catch (error) {
        console.error('Error creating kitchen order:', error);
        throw error;
    }
};

export const updateOrderStatus = async (kitchenOrderId, newStatus) => {
    try {
        const response = await axios.patch(
            `${API_URL}/kitchen_orders/${kitchenOrderId}`, 
            { status: newStatus }
        );
        return response.data;
    } catch (error) {
        console.error(`Error updating status for kitchen order ${kitchenOrderId}:`, error);
        throw error;
    }
};

export const callMenuService = async (endpoint) => {
    try {
        const response = await axios.get(`${API_URL}/call-menu-service${endpoint}`);
        return response.data;
    } catch (error) {
        console.error(`Error calling menu service at ${endpoint}:`, error);
        throw error;
    }
};

export const toggleDishAvailability = async (dishId, isAvailable) => {
    try {
        const endpoint = isAvailable ? 'turn-on-dish' : 'turn-off-dish';
        const response = await axios.patch(`${API_URL}/call-menu-service/${endpoint}/${dishId}`);
        return response.data;
    } catch (error) {
        console.error(`Error toggling availability for dish ${dishId}:`, error);
        throw error;
    }
};

export const updateOrderServiceStatus = async (orderId, status) => {
    try {
        const response = await axios.patch(
            `${API_URL}/call-order-payment-service/orders/${orderId}`, 
            { status }
        );
        return response.data;
    } catch (error) {
        console.error(`Error updating order service status for order ${orderId}:`, error);
        throw error;
    }
};
