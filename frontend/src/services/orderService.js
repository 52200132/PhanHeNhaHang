import axios from 'axios';

const API_URL = 'http://localhost:8001/api/v1';

export const getAllTables = async () => {
  try {
    const response = await axios.get(`${API_URL}/tables`);
    return response.data;
  } catch (error) {
    console.error('Error fetching tables:', error);
    throw error;
  }
};

export const getTableById = async (tableId) => {
  try {
    const response = await axios.get(`${API_URL}/tables/${tableId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching table with ID ${tableId}:`, error);
    throw error;
  }
};

export const createTable = async (tableData) => {
  try {
    const response = await axios.post(`${API_URL}/tables`, tableData);
    return response.data;
  } catch (error) {
    console.error('Error creating table:', error);
    throw error;
  }
};

export const updateTable = async (tableId, tableData) => {
  try {
    const response = await axios.put(`${API_URL}/tables/${tableId}`, tableData);
    return response.data;
  } catch (error) {
    console.error(`Error updating table with ID ${tableId}:`, error);
    throw error;
  }
};

export const createOrder = async (orderData) => {
  try {
    const response = await axios.post(`${API_URL}/orders`, orderData);
    return response.data;
  } catch (error) {
    console.error('Error creating order:', error);
    throw error;
  }
};

export const getOrderById = async (orderId) => {
  try {
    const response = await axios.get(`${API_URL}/orders/${orderId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching order with ID ${orderId}:`, error);
    throw error;
  }
};

export const addDishesToOrder = async (orderId, dishesData) => {
  try {
    const response = await axios.post(`${API_URL}/orders/add-orderdetails/${orderId}`, dishesData);
    return response.data;
  } catch (error) {
    console.error(`Error adding dishes to order ${orderId}:`, error);
    throw error;
  }
};

export const deleteDishFromOrder = async (orderDetailId) => {
  try {
    const response = await axios.delete(`${API_URL}/orders/delete_orderdetail/${orderDetailId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting dish from order detail ${orderDetailId}:`, error);
    throw error;
  }
};

export const getAllShifts = async () => {
  try {
    const response = await axios.get(`${API_URL}/shifts`);
    return response.data;
  } catch (error) {
    console.error('Error fetching shifts:', error);
    throw error;
  }
};

export const processPayment = async (paymentData) => {
  try {
    const response = await axios.post(`${API_URL}/payments`, paymentData);
    return response.data;
  } catch (error) {
    console.error('Error processing payment:', error);
    throw error;
  }
};
