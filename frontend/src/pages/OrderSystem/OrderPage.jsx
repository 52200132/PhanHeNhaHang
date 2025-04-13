// import React, { useState, useEffect } from 'react';
// import { getAllTables, createOrder } from '../../services/orderService';
// import { menuService } from '../../services/menuService';
// import Card from '../../components/common/Card';
// import Button from '../../components/common/Button';
// import './OrderPage.css';

// const OrderPage = () => {
//   const [tables, setTables] = useState([]);
//   const [dishes, setDishes] = useState([]);
//   const [selectedTable, setSelectedTable] = useState(null);
//   const [selectedDishes, setSelectedDishes] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         setLoading(true);
//         const [tablesData, dishesData] = await Promise.all([
//           getAllTables(),
//           menuService.getAllMenuItems()
//         ]);
//         setTables(tablesData.data || []);
//         setDishes(dishesData || []);
//       } catch (err) {
//         setError('Failed to load order data');
//         console.error(err);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchData();
//   }, []);

//   const handleSelectTable = (table) => {
//     setSelectedTable(table);
//   };

//   const handleAddDish = (dish) => {
//     const existingDish = selectedDishes.find(item => item.dish_id === dish.dish_id);
    
//     if (existingDish) {
//       setSelectedDishes(
//         selectedDishes.map(item => 
//           item.dish_id === dish.dish_id 
//             ? { ...item, quantity: item.quantity + 1 } 
//             : item
//         )
//       );
//     } else {
//       setSelectedDishes([...selectedDishes, { ...dish, quantity: 1, note: '' }]);
//     }
//   };

//   const handleRemoveDish = (dishId) => {
//     setSelectedDishes(selectedDishes.filter(dish => dish.dish_id !== dishId));
//   };

//   const handleUpdateQuantity = (dishId, quantity) => {
//     if (quantity < 1) return;
    
//     setSelectedDishes(
//       selectedDishes.map(item => 
//         item.dish_id === dishId ? { ...item, quantity } : item
//       )
//     );
//   };

//   const handleUpdateNote = (dishId, note) => {
//     setSelectedDishes(
//       selectedDishes.map(item => 
//         item.dish_id === dishId ? { ...item, note } : item
//       )
//     );
//   };

//   const handlePlaceOrder = async () => {
//     if (!selectedTable || selectedDishes.length === 0) {
//       setError('Please select a table and at least one dish');
//       return;
//     }
    
//     try {
//       const orderData = {
//         table_id: selectedTable.table_id,
//         items: selectedDishes.map(dish => ({
//           dish_id: dish.dish_id,
//           quantity: dish.quantity,
//           note: dish.note
//         }))
//       };
      
//       await createOrder(orderData);
      
//       // Reset order form
//       setSelectedTable(null);
//       setSelectedDishes([]);
      
//       alert('Order placed successfully!');
//     } catch (err) {
//       setError('Failed to place order');
//       console.error(err);
//     }
//   };

//   if (loading) return <div className="loading">Loading order data...</div>;
//   if (error) return <div className="error">{error}</div>;

//   return (
//     <div className="order-page">
//       <div className="order-page__header">
//         <h2>Place Order</h2>
//       </div>

//       <div className="order-page__content">
//         <div className="order-page__tables">
//           <h3>Select Table</h3>
//           <div className="tables-grid">
//             {tables.map(table => (
//               <div 
//                 key={table.table_id}
//                 className={`table-card ${selectedTable?.table_id === table.table_id ? 'table-card--selected' : ''} ${!table.is_available ? 'table-card--unavailable' : ''}`}
//                 onClick={() => table.is_available && handleSelectTable(table)}
//               >
//                 <div className="table-card__name">{table.name}</div>
//                 <div className="table-card__capacity">Capacity: {table.capacity}</div>
//                 <div className="table-card__status">
//                   {table.is_available ? 'Available' : 'Occupied'}
//                 </div>
//               </div>
//             ))}
//           </div>
//         </div>

//         <div className="order-page__menu">
//           <h3>Select Dishes</h3>
//           <div className="dishes-grid">
//             {dishes.filter(dish => dish.is_available).map(dish => (
//               <Card 
//                 key={dish.dish_id}
//                 title={dish.name}
//                 subtitle={`${dish.price} ${dish.unit_price}`}
//               >
//                 <Button 
//                   onClick={() => handleAddDish(dish)}
//                   disabled={!selectedTable}
//                 >
//                   Add to Order
//                 </Button>
//               </Card>
//             ))}
//           </div>
//         </div>

//         <div className="order-page__summary">
//           <Card title="Order Summary">
//             {selectedTable ? (
//               <div>
//                 <p><strong>Table:</strong> {selectedTable.name}</p>
                
//                 {selectedDishes.length > 0 ? (
//                   <div>
//                     <h4>Selected Dishes:</h4>
//                     <ul className="order-items">
//                       {selectedDishes.map(dish => (
//                         <li key={dish.dish_id} className="order-item">
//                           <div className="order-item__name">{dish.name}</div>
//                           <div className="order-item__price">{dish.price * dish.quantity} {dish.unit_price}</div>
//                           <div className="order-item__actions">
//                             <button onClick={() => handleUpdateQuantity(dish.dish_id, dish.quantity - 1)}>-</button>
//                             <span>{dish.quantity}</span>
//                             <button onClick={() => handleUpdateQuantity(dish.dish_id, dish.quantity + 1)}>+</button>
//                           </div>
//                           <input 
//                             type="text" 
//                             placeholder="Add note" 
//                             value={dish.note} 
//                             onChange={(e) => handleUpdateNote(dish.dish_id, e.target.value)}
//                           />
//                           <button onClick={() => handleRemoveDish(dish.dish_id)}>Remove</button>
//                         </li>
//                       ))}
//                     </ul>
                    
//                     <div className="order-total">
//                       <strong>Total:</strong> {selectedDishes.reduce((sum, dish) => sum + (dish.price * dish.quantity), 0)} VNĐ
//                     </div>
                    
//                     <Button onClick={handlePlaceOrder} fullWidth>Place Order</Button>
//                   </div>
//                 ) : (
//                   <p>No dishes selected</p>
//                 )}
//               </div>
//             ) : (
//               <p>Please select a table first</p>
//             )}
//           </Card>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default OrderPage;
