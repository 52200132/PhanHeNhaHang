import React, { useState, useEffect } from 'react';
import './StaffPage.css';
import TableCard from '../../components/staff/TableCard/TableCard';
import SearchBar from '../../components/common/SearchBar';
import QRCodeModal from '../../components/common/QRCodeModal/QRCodeModal';
import { tableService } from '../../services/orderService';

const StaffPage = () => {
    const [tables, setTables] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedStatus, setSelectedStatus] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [showQRModal, setShowQRModal] = useState(false);
    const [selectedTable, setSelectedTable] = useState(null);

    useEffect(() => {
        fetchTables();
    }, []);

    const fetchTables = async () => {
        try {
            setLoading(true);
            // Gọi service để lấy danh sách bàn
            const tablesData = await tableService.getAllTables();
            
            // Chuyển đổi dữ liệu từ API thành dạng dữ liệu mong muốn
            const formattedTables = tablesData.map(table => ({
                id: table.table_id,
                name: table.name,
                status: table.is_available ? 'Trống' : 'Đang phục vụ',
                type: table.table_type,
                capacity: table.capacity
            }));
            
            // Sắp xếp bàn theo ID
            const sortedTables = formattedTables.sort((a, b) => a.id - b.id);
            
            setTables(sortedTables);
            setLoading(false);
        } catch (err) {
            setError('Không thể tải dữ liệu bàn');
            setLoading(false);
            console.error(err);
        }
    };

    // Định nghĩa các trạng thái bàn để hiển thị trong sidebar
    const tableStatuses = [
        { id: 1, name: 'Tất cả' },
        { id: 2, name: 'Trống' },
        { id: 3, name: 'Đang phục vụ' }
    ];

    // Xử lý sự kiện khi chọn một bàn
    const handleTableClick = (tableId) => {
        const table = tables.find(t => t.id === tableId);
        
        if (table) {
            setSelectedTable(table);
            
            // Chỉ hiện QR code khi bàn đang trống
            if (table.status === 'Trống') {
                setShowQRModal(true);
            } else {
                console.log(`Đã chọn bàn có ID: ${tableId} - Đang phục vụ`);
                // Xử lý khác nếu bàn đang phục vụ
            }
        }
    };

    // Xử lý sự kiện khi xác nhận phục vụ bàn
    const handleConfirmService = async () => {
        if (!selectedTable) return;
        
        try {
            // Giả lập gọi API cập nhật trạng thái bàn
            // TODO: Thay thế bằng API thực tế
            console.log(`Cập nhật bàn ${selectedTable.id} thành trạng thái đang phục vụ`);
            await tableService.updateStatusTable(selectedTable.id, "Đang phục vụ");

            // Cập nhật state của bàn trong ứng dụng
            const updatedTables = tables.map(table => {
                if (table.id === selectedTable.id) {
                    return { ...table, status: 'Đang phục vụ' };
                }
                return table;
            });
            
            setTables(updatedTables);
            setShowQRModal(false);
            
            // Trong thực tế, bạn sẽ gọi API ở đây
            // await tableService.updateTableStatus(selectedTable.id, false);
        } catch (error) {
            console.error("Lỗi khi cập nhật trạng thái bàn:", error);
            alert("Không thể cập nhật trạng thái bàn. Vui lòng thử lại sau.");
        }
    };

    // Xử lý sự kiện tìm kiếm
    const handleSearch = (term) => {
        setSearchTerm(term);
    };

    // Lọc danh sách bàn theo trạng thái và từ khóa tìm kiếm
    const filteredTables = tables.filter(table => {
        // Lọc theo trạng thái (nếu có chọn trạng thái và không phải 'Tất cả')
        const statusMatch = selectedStatus === null || selectedStatus === 1 ||
            (selectedStatus === 2 && table.status === 'Trống') ||
            (selectedStatus === 3 && table.status === 'Đang phục vụ');

        // Lọc theo từ khóa tìm kiếm
        const searchMatch =
            table.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            table.type.toLowerCase().includes(searchTerm.toLowerCase());

        return statusMatch && searchMatch;
    });

    if (loading) return <div className="loading">Đang tải dữ liệu bàn...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="staff-page">
            <div className="staff-page__header">
                <h2>Danh sách bàn</h2>
            </div>

            <div className="staff-page__top-bar">
                <div className="staff-page__staff-info">
                    Nhân viên: Nguyễn Văn A
                </div>
                <div className="search-bar-container">
                    <SearchBar
                        placeholder="Tìm kiếm bàn..."
                        onChange={handleSearch}
                        className="m-0 flex-grow-1"
                    />
                </div>
            </div>

            <div className="staff-page__container">
                <div className="staff-page__sidebar">
                    <h3>Trạng thái bàn</h3>
                    <ul className="category-list">
                        {tableStatuses.map(status => (
                            <li
                                key={status.id}
                                className={selectedStatus === status.id ? "active" : ""}
                                onClick={() => setSelectedStatus(status.id)}
                            >
                                {status.name}
                                {status.id !== 1 && (
                                    <span className="table-count">
                                        {status.id === 2
                                            ? tables.filter(t => t.status === 'Trống').length
                                            : tables.filter(t => t.status === 'Đang phục vụ').length}
                                    </span>
                                )}
                            </li>
                        ))}
                    </ul>

                    <div className="status-legend">
                        <div className="status-item">
                            <span className="status-dot status-available"></span>
                            <span>Trống</span>
                        </div>
                        <div className="status-item">
                            <span className="status-dot status-busy"></span>
                            <span>Đang phục vụ</span>
                        </div>
                    </div>

                    <div className="quick-actions">
                        <button className="action-button">
                            Yêu cầu hỗ trợ
                        </button>
                        <button className="action-button">
                            Báo cáo sự cố
                        </button>
                    </div>
                </div>

                <div className="staff-page__content">
                    <div className="category-section">
                        <div className="category-header">
                            <h3>
                                {selectedStatus === 2 ? 'Bàn Trống' :
                                    selectedStatus === 3 ? 'Bàn Đang phục vụ' :
                                        'Tất cả các bàn'}
                            </h3>
                            <span className="table-info">Hiển thị {filteredTables.length} bàn</span>
                        </div>
                        <div className="tables-grid">
                            {filteredTables.length === 0 ? (
                                <p className="no-tables">Không tìm thấy bàn nào</p>
                            ) : (
                                filteredTables.map(table => (
                                    <TableCard
                                        key={table.id}
                                        tableId={table.id}
                                        name={table.name}
                                        status={table.status}
                                        type={table.type}
                                        capacity={table.capacity}
                                        onTableClick={handleTableClick}
                                    />
                                ))
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* QR Code Modal */}
            {showQRModal && selectedTable && (
                <QRCodeModal
                    tableId={selectedTable.id}
                    tableName={selectedTable.name}
                    onClose={() => setShowQRModal(false)}
                    onConfirm={handleConfirmService}
                />
            )}
        </div>
    );
};

export default StaffPage;
