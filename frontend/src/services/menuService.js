import axios from 'axios';

const API_URL = 'http://localhost:8002/api/v1';

export const getAllDishes = async () => {
  try {
    const response = await axios.get(`${API_URL}/dishes`);
    return response.data;
  } catch (error) {
    console.error('Error fetching dishes:', error);
    throw error;
  }
};

export const getDishById = async (dishId) => {
  try {
    const response = await axios.get(`${API_URL}/dishes/${dishId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching dish with ID ${dishId}:`, error);
    throw error;
  }
};

export const createDish = async (dishData) => {
  try {
    const response = await axios.post(`${API_URL}/dishes`, dishData);
    return response.data;
  } catch (error) {
    console.error('Error creating dish:', error);
    throw error;
  }
};

export const updateDish = async (dishId, dishData) => {
  try {
    const response = await axios.patch(`${API_URL}/dishes/${dishId}`, dishData);
    return response.data;
  } catch (error) {
    console.error(`Error updating dish with ID ${dishId}:`, error);
    throw error;
  }
};

export const deleteDish = async (dishId) => {
  try {
    const response = await axios.delete(`${API_URL}/dishes/${dishId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting dish with ID ${dishId}:`, error);
    throw error;
  }
};

export const getAllCategories = async () => {
  try {
    const response = await axios.get(`${API_URL}/categories`);
    return response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw error;
  }
};

export const getCategoryById = async (categoryId) => {
  try {
    const response = await axios.get(`${API_URL}/categories/${categoryId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching category with ID ${categoryId}:`, error);
    throw error;
  }
};

export const createCategory = async (categoryData) => {
  try {
    const response = await axios.post(`${API_URL}/categories`, categoryData);
    return response.data;
  } catch (error) {
    console.error('Error creating category:', error);
    throw error;
  }
};

export const getDishesByCategory = async (categoryId) => {
  try {
    const response = await axios.get(`${API_URL}/dishes/categories/${categoryId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching dishes for category ${categoryId}:`, error);
    throw error;
  }
};

export const toggleDishAvailability = async (dishId, isAvailable) => {
  try {
    const response = await axios.patch(`${API_URL}/dishes/${dishId}`, {
      is_available: isAvailable
    });
    return response.data;
  } catch (error) {
    console.error(`Error toggling availability for dish ${dishId}:`, error);
    throw error;
  }
};
