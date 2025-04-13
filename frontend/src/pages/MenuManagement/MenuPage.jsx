import React, { useState, useEffect } from 'react';
import { getAllDishes, getAllCategories } from '../../services/menuService';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import './MenuPage.css';

const MenuPage = () => {
  const [dishes, setDishes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [dishesData, categoriesData] = await Promise.all([
          getAllDishes(),
          getAllCategories()
        ]);
        setDishes(dishesData.data || []);
        setCategories(categoriesData.data || []);
      } catch (err) {
        setError('Failed to load menu data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const filteredDishes = selectedCategory 
    ? dishes.filter(dish => dish.category_id === selectedCategory) 
    : dishes;

  if (loading) return <div className="loading">Loading menu data...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="menu-page">
      <div className="menu-page__header">
        <h2>Menu Management</h2>
        <Button variant="primary">Add New Dish</Button>
      </div>

      <div className="menu-page__categories">
        <Button 
          variant={selectedCategory === null ? "primary" : "secondary"}
          onClick={() => setSelectedCategory(null)}
        >
          All Categories
        </Button>
        {categories.map(category => (
          <Button
            key={category.category_id}
            variant={selectedCategory === category.category_id ? "primary" : "secondary"}
            onClick={() => setSelectedCategory(category.category_id)}
          >
            {category.name}
          </Button>
        ))}
      </div>

      <div className="menu-page__dishes">
        {filteredDishes.length === 0 ? (
          <p>No dishes found in this category</p>
        ) : (
          filteredDishes.map(dish => (
            <Card 
              key={dish.dish_id}
              title={dish.name}
              subtitle={`${dish.price} ${dish.unit_price}`}
              className={!dish.is_available ? "dish-card--unavailable" : ""}
            >
              <div className="dish-card__content">
                <p>{dish.description || 'No description available'}</p>
                <div className="dish-card__status">
                  Status: {dish.is_available ? 'Available' : 'Unavailable'}
                </div>
                <div className="dish-card__actions">
                  <Button variant="secondary" size="small">Edit</Button>
                  <Button variant="danger" size="small">Delete</Button>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default MenuPage;
