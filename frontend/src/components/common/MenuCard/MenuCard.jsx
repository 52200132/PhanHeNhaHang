import React, { useState } from "react";

export const MenuCard = ({
    dishId,
    imageUrl,
    itemName = "Menu Item",
    price = "0",
    description = "",
    onOrder = () => { },
    className = ""
}) => {
    const [quantity, setQuantity] = useState(1);

    const increaseQuantity = () => setQuantity(prev => prev + 1);
    const decreaseQuantity = () => setQuantity(prev => Math.max(1, prev - 1));

    return (
        <article className={`card bg-white rounded shadow-sm overflow-hidden ${className}`} style={{ height: "100%" }}>
            <div className="position-relative d-flex flex-column" style={{ height: "100%" }}>
                <img
                    src={imageUrl}
                    className="card-img-top"
                    style={{ height: "160px", objectFit: "cover" }}
                    alt={itemName}
                />
                <div className="card-body p-3 d-flex flex-column">
                    <h5 className="card-title fw-bold mb-1" style={{ fontSize: "1.1rem" }}>{itemName}</h5>
                    <p className="card-text text-danger fw-bold mb-2">{parseInt(price).toLocaleString('vi-VN')} đ</p>
                    
                    {description && <p className="card-text small text-muted mb-3" style={{ fontSize: "0.85rem", lineHeight: "1.3" }}>{description}</p>}
                    
                    <div className="mt-auto pt-2 border-top">
                        <div className="d-flex justify-content-between align-items-center">
                            <div className="quantity-selector d-flex align-items-center">
                                <button 
                                    className="btn p-0 rounded-circle d-flex align-items-center justify-content-center" 
                                    style={{ width: "24px", height: "24px", backgroundColor: "#f2f2f2", border: "1px solid #e0e0e0" }}
                                    onClick={decreaseQuantity}
                                >
                                    <span style={{ fontSize: "0.9rem", lineHeight: "1" }}>-</span>
                                </button>
                                <span className="mx-2" style={{ fontSize: "0.9rem" }}>{quantity}</span>
                                <button 
                                    className="btn p-0 rounded-circle d-flex align-items-center justify-content-center" 
                                    style={{ width: "24px", height: "24px", backgroundColor: "#f2f2f2", border: "1px solid #e0e0e0" }}
                                    onClick={increaseQuantity}
                                >
                                    <span style={{ fontSize: "0.9rem", lineHeight: "1" }}>+</span>
                                </button>
                            </div>
                            <button
                                className="btn btn-primary rounded-pill px-3 py-0"
                                style={{ 
                                    backgroundColor: "#0D6EFD", 
                                    fontSize: "0.8rem", 
                                    height: "28px",
                                    boxShadow: "none",
                                    fontWeight: "500" 
                                }}
                                onClick={() => onOrder({ dishId, itemName, quantity, price })}
                            >
                                Đặt món
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </article>
    );
};

export default MenuCard;