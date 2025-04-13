import React from 'react';
// Make sure you've installed this package
import { QRCodeSVG } from 'qrcode.react';
import './QRCodeModal.css';

const QRCodeModal = ({ tableId, tableName, onClose, onConfirm }) => {
    // Encode the table ID for the URL
    const encodedTableId = btoa(tableId.toString());
    const menuUrl = `/guest-menu?id=${encodedTableId}`;
    const fullUrl = `${window.location.origin}${menuUrl}`;

    return (
        <div className="qr-modal-overlay">
            <div className="qr-modal">
                <div className="qr-modal__header">
                    <h2>QR Code cho {tableName}</h2>
                    <button className="close-button" onClick={onClose}>×</button>
                </div>
                <div className="qr-modal__content">
                    <div className="qr-code-container">
                        {/* Use QRCodeSVG component */}
                        <QRCodeSVG value={fullUrl} size={200} />
                    </div>
                    <div className="qr-url">
                        <p>URL: <a href={fullUrl} target="_blank" rel="noopener noreferrer">{fullUrl}</a></p>
                        <p>Quét mã QR để truy cập menu</p>
                    </div>
                </div>
                <div className="qr-modal__footer">
                    <button className="cancel-button" onClick={onClose}>Hủy</button>
                    <button className="confirm-button" onClick={onConfirm}>Xác nhận phục vụ</button>
                </div>
            </div>
        </div>
    );
};

export default QRCodeModal;
