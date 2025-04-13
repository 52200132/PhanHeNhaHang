import axios from 'axios';

const API_URL = process.env.REACT_APP_MENU_SERVICE_URL || 'http://localhost:8001/api';

export const menuService = {
    // Fetch all food categories
    getCategories: async () => {
        try {
            const response = await axios.get(`${API_URL}/categories`);
            // console.log('Response from categories:', response);
            let catagories_data = response.data['data'];
            // console.log(catagories_data);
            return catagories_data;
        } catch (error) {
            console.error('Error fetching categories:', error);
            throw error;
        }
    },

    // Fetch menu items by category
    // getMenuItemsByCategory: async (categoryId) => {
    //     try {
    //         const response = await axios.get(`${API_URL}/menu-items?categoryId=${categoryId}`);
    //         return response.data;
    //     } catch (error) {
    //         console.error('Error fetching menu items:', error);
    //         throw error;
    //     }
    // },

    // Fetch all menu items
    getAllDishes: async () => {
        try {
            const response = await axios.get(`${API_URL}/dishes`);
            let dishes_data = response.data['data'];
            return dishes_data;
        } catch (error) {
            console.error('Error fetching all menu items:', error);
            throw error;
        }
    }
};
