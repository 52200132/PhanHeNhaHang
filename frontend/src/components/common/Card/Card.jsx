import React from 'react';
import './Card.css';

const Card = ({
    children,
    title,
    subtitle,
    className = '',
    elevation = 1
}) => {
    return (
        <div className={`card card--elevation-${elevation} ${className}`}>
            {(title || subtitle) && (
                <div className="card__header">
                    {title && <h3 className="card__title">{title}</h3>}
                    {subtitle && <div className="card__subtitle">{subtitle}</div>}
                </div>
            )}
            <div className="card__content">
                {children}
            </div>
        </div>
    );
};

export default Card;
