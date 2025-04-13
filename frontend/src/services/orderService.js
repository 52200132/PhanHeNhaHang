import axios from 'axios';

const API_URL = process.env.REACT_APP_ORDER_SERVICE_URL; //|| 'http://localhost:8002/api';

export const tableService = {
    getAllTables: async () => {
        try {
            const response = await axios.get(`${API_URL}/tables`);
            return response.data;
        } catch (error) {
            console.error('Error fetching tables:', error);
            throw error;
        }
    },
    
    getTableById: async (tableId) => {
        try {
            const response = await axios.get(`${API_URL}/tables/${tableId}`);
            return response.data;
        } catch (error) {
            console.error(`Error fetching table with ID ${tableId}:`, error);
            throw error;
        }
    },
    
    createTable: async (tableData) => {
        try {
            const response = await axios.post(`${API_URL}/tables`, tableData);
            return response.data;
        } catch (error) {
            console.error('Error creating table:', error);
            throw error;
        }
    },
    
    updateTable: async (tableId, tableData) => {
        try {
            const response = await axios.put(`${API_URL}/tables/${tableId}`, tableData);
            return response.data;
        } catch (error) {
            console.error(`Error updating table with ID ${tableId}:`, error);
            throw error;
        }
    }
};

export const orderService = {
    createOrder: async (orderData) => {
        try {
            const response = await axios.post(`${API_URL}/orders`, orderData);
            // console.log('Order created:', response);
            return response;
        } catch (error) {
            console.log('Error creating order:', error);
            return error.request;
            // throw error;
        }
    },
    
    getOrderById: async (orderId) => {
        try {
            const response = await axios.get(`${API_URL}/orders/${orderId}`);
            return response.data;
        } catch (error) {
            console.error(`Error fetching order with ID ${orderId}:`, error);
            throw error;
        }
    },
    
    addDishesToOrder: async (orderId, dishesData) => {
        try {
            const response = await axios.post(`${API_URL}/orders/add-orderdetails/${orderId}`, dishesData);
            return response.data;
        } catch (error) {
            console.error(`Error adding dishes to order ${orderId}:`, error);
            throw error;
        }
    },
    
    deleteDishFromOrder: async (orderDetailId) => {
        try {
            const response = await axios.delete(`${API_URL}/orders/delete_orderdetail/${orderDetailId}`);
            return response.data;
        } catch (error) {
            console.error(`Error deleting dish from order detail ${orderDetailId}:`, error);
            throw error;
        }
    }
};

export const shiftService = {
    getAllShifts: async () => {
        try {
            const response = await axios.get(`${API_URL}/shifts`);
            return response.data;
        } catch (error) {
            console.error('Error fetching shifts:', error);
            throw error;
        }
    }
};

export const paymentService = {
    processPayment: async (paymentData) => {
        try {
            const response = await axios.post(`${API_URL}/payments`, paymentData);
            return response.data;
        } catch (error) {
            console.error('Error processing payment:', error);
            throw error;
        }
    }
};
