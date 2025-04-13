import React from 'react';
import { menuService } from '../../services/menuService';
import { orderService, tableService } from '../../services/orderService';
import { useState, useEffect } from 'react';
import './GuestMenu.css';
import SearchBar from '../../components/common/SearchBar';
import MenuCard from '../../components/common/MenuCard/MenuCard';
import { useLocation } from 'react-router-dom';

const GuestMenu = () => {
    const [dishes, setDishes] = useState([]);
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [orderedItems, setOrderedItems] = useState([]);
    const [notes, setNotes] = useState({});
    const [table, setTable] = useState(null);

    // Get the table ID from the URL query parameter
    const useQuery = () => new URLSearchParams(useLocation().search);
    const query = useQuery();
    const encodedTableId = query.get('id');

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [categoriesData, dishesData, tableData] = await Promise.all([
                    menuService.getCategories(),
                    menuService.getAllDishes(),
                    encodedTableId ? tableService.getTableByEncodedId(encodedTableId) : null,
                ]);

                setCategories(categoriesData || []);
                setDishes(dishesData || []);
                setTable(tableData);

            } catch (err) {
                setError('Failed to load menu data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [encodedTableId]);

    const handleOrder = (item) => {
        const { dishId, itemName, quantity, price } = item;

        // Check if the item already exists in the ordered items
        const existingItemIndex = orderedItems.findIndex(i => i.dishId === dishId);

        if (existingItemIndex !== -1) {
            // Update existing item quantity
            const updatedItems = [...orderedItems];
            updatedItems[existingItemIndex].quantity += quantity;
            setOrderedItems(updatedItems);
        } else {
            // Add new item to ordered items
            setOrderedItems([...orderedItems, {
                id: Date.now(), // unique id for the order item
                dishId: dishId,
                name: itemName,
                price: price,
                quantity: quantity
            }]);
        }
    };

    const updateItemQuantity = (itemId, newQuantity) => {
        if (newQuantity <= 0) {
            // Remove item if quantity is 0 or negative
            setOrderedItems(orderedItems.filter(item => item.id !== itemId));
        } else {
            // Update quantity
            setOrderedItems(orderedItems.map(item =>
                item.id === itemId ? { ...item, quantity: newQuantity } : item
            ));
        }
    };

    const handleNoteChange = (itemId, note) => {
        setNotes({
            ...notes,
            [itemId]: note
        });
    };

    const submitOrder = () => {
        if (!table) {
            alert('Vui lòng chọn bàn trước khi đặt món!');
            return;
        }

        // Prepare order data with items and their notes
        const orderData = orderedItems.map(item => ({
            dish_id: item.dishId,
            quantity: item.quantity,
            note: notes[item.id] || ''
        }));

        // TODO: Submit the order to the backend
        const order = {
            table_id: table.table_id,
            items: orderData,
        }

        orderService.createOrder(order)
            .then(response => {
                console.log('Order response:', response);
                if (response.status === 200) {
                    alert('Đặt món thành công!');
                    // Clear the order after submission
                    setOrderedItems([]);
                    setNotes({});
                } else {
                    alert('Đặt món thất bại! Vui lòng thử lại.');
                }
            });
        // console.log('Submitting order:', order);
        // Here you would implement the API call to submit the order
    };

    const getTotalAmount = () => {
        return orderedItems.reduce((total, item) => {
            return total + (parseFloat(item.price) * item.quantity);
        }, 0).toLocaleString('vi-VN');
    };

    const filteredDishes = selectedCategory
        ? dishes.filter(dish => dish.category_id === selectedCategory)
        : dishes;

    // Group dishes by category
    const dishesByCategory = categories.reduce((acc, category) => {
        acc[category.category_id] = dishes.filter(dish => dish.category_id === category.category_id);
        return acc;
    }, {});

    if (loading) return <div className="loading">Đang tải dữ liệu menu...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="guest-menu">
            <div className="guest-menu__header">
                <h2>Thực đơn nhà hàng</h2>
            </div>

            <div className="guest-menu__top-bar">
                <div className="guest-menu__table-number">
                    {table ? `${table.name}` : 'Bàn không xác định'}
                </div>
                <div className="search-bar-container">
                    <SearchBar placeholder="Tìm kiếm món ăn..."
                        className="m-0 flex-grow-1" />
                </div>
            </div>

            <div className="guest-menu__container">
                <div className="guest-menu__sidebar">
                    <h3>Danh mục món ăn</h3>
                    <ul className="category-list">
                        <li
                            className={selectedCategory === null ? "active" : ""}
                            onClick={() => setSelectedCategory(null)}
                        >
                            Tất cả các món
                        </li>
                        {categories.map(category => (
                            <li
                                key={category.category_id}
                                className={selectedCategory === category.category_id ? "active" : ""}
                                onClick={() => setSelectedCategory(category.category_id)}
                            >
                                {category.name}
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="guest-menu__content">
                    {selectedCategory !== null ? (
                        // Show specific category
                        <div className="category-section">
                            <div className="category-header">
                                <h3>{categories.find(c => c.category_id === selectedCategory)?.name || "Món ăn"}</h3>
                            </div>
                            <div className="menu-grid">
                                {filteredDishes.length === 0 ? (
                                    <p>Không tìm thấy món ăn trong danh mục này</p>
                                ) : (
                                    filteredDishes.map(dish => (
                                        <MenuCard
                                            key={dish.dish_id}
                                            dishId={dish.dish_id}
                                            imageUrl={dish.img_path || "https://via.placeholder.com/150"}
                                            itemName={dish.name}
                                            price={dish.price}
                                            description={dish.description}
                                            onOrder={handleOrder}
                                        />
                                    ))
                                )}
                            </div>
                        </div>
                    ) : (
                        // Show all categories
                        categories.map(category => (
                            <div key={category.category_id} className="category-section">
                                <div className="category-header">
                                    <h3>{category.name}</h3>
                                </div>
                                <div className="menu-grid">
                                    {dishesByCategory[category.category_id]?.map(dish => (
                                        <MenuCard
                                            key={dish.dish_id}
                                            dishId={dish.dish_id}
                                            imageUrl={dish.img_path}
                                            itemName={dish.name}
                                            price={dish.price}
                                            description={dish.description}
                                            onOrder={handleOrder}
                                        />
                                    ))}
                                </div>
                            </div>
                        ))
                    )}
                </div>

                {/* Order Summary as third column - more compact */}
                <div className="order-summary">
                    <h3>Món đã đặt</h3>
                    <div className="ordered-items-container">
                        {orderedItems.length === 0 ? (
                            <p className="no-items">Chưa có món nào được đặt</p>
                        ) : (
                            <div className="ordered-items-list">
                                {orderedItems.map((item) => (
                                    <div key={item.id} className="ordered-item">
                                        <div className="ordered-item-header">
                                            <h4>{item.name}</h4>
                                            <p className="ordered-item-price">{parseInt(item.price).toLocaleString('vi-VN')} đ</p>
                                        </div>

                                        <div className="ordered-item-controls">
                                            <div className="quantity-controls">
                                                <button onClick={() => updateItemQuantity(item.id, item.quantity - 1)}>-</button>
                                                <span>{item.quantity}</span>
                                                <button onClick={() => updateItemQuantity(item.id, item.quantity + 1)}>+</button>
                                            </div>
                                            <p className="item-subtotal">{(item.quantity * parseFloat(item.price)).toLocaleString('vi-VN')} đ</p>
                                        </div>

                                        <textarea
                                            className="item-note"
                                            placeholder="Ghi chú đặc biệt..."
                                            value={notes[item.id] || ''}
                                            onChange={(e) => handleNoteChange(item.id, e.target.value)}
                                        />
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {orderedItems.length > 0 && (
                        <div className="order-footer">
                            <div className="order-total">
                                <span>Tổng cộng:</span>
                                <span className="total-amount">{getTotalAmount()} đ</span>
                            </div>
                            <button className="order-button" onClick={submitOrder}>
                                Đặt món
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default GuestMenu;
