import React from 'react';
import './TableCard.css';

const TableCard = ({ tableId, name, status, type, capacity, onTableClick }) => {
    // Xác định class CSS dựa vào trạng thái của bàn
    const getStatusClass = () => {
        switch (status) {
            case 0:
            case 'Đang phục vụ':
                return 'table-card--busy';
            case 1:
            case 'Trống':
                return 'table-card--available';
            default:
                return '';
        }
    };

    const isAvailable = status === 'Trống' || status === 1;

    return (
        <div 
            className={`table-card ${getStatusClass()}`}
            onClick={() => onTableClick(tableId)}
        >
            <div className="table-card__header">
                <h3>{name}</h3>
                <span className={`table-status ${getStatusClass()}`}>{status}</span>
            </div>
            
            <div className="table-card__content">
                <div className="table-info">
                    <div className="info-row">
                        <span className="info-label">ID:</span>
                        <span className="info-value">{tableId}</span>
                    </div>
                    <div className="info-row">
                        <span className="info-label">Trạng thái:</span>
                        <span className="info-value">{status}</span>
                    </div>
                    <div className="info-row">
                        <span className="info-label">Loại bàn:</span>
                        <span className="info-value">{type}</span>
                    </div>
                    <div className="info-row">
                        <span className="info-label">Số người tối đa:</span>
                        <span className="info-value">{capacity}</span>
                    </div>
                </div>
            </div>
            
            <div className="table-card__footer">
                {isAvailable ? (
                    <button className="view-detail-btn available-btn">Tạo QR Order</button>
                ) : (
                    <button className="view-detail-btn busy-btn">Xem chi tiết</button>
                )}
            </div>
        </div>
    );
};

export default TableCard;
