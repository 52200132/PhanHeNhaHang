# Hệ Thống Quản Lý Nhà Hàng

Hệ thống microservices quản lý nhà hàng với FastAPI backend và React frontend.

## Cấu trúc dự án

- `/backend-fastapi`: Backend API dùng FastAPI và SQLAlchemy
  - `/order-payment-service`: Dịch vụ quản lý đơn hàng và thanh toán
  - `/menu-service`: Dịch vụ quản lý thực đơn và món ăn
  - `/kitchen-service`: Dịch vụ quản lý nhà bếp
- `/frontend`: Frontend sử dụng React

## Cài đặt và chạy dự án

### Yêu cầu

- Python 3.8+
- Node.js 18+
- MySQL hoặc SQL Server
- Java Runtime Environment (JRE) cho Kafka

### Phương thức 1: Sử dụng Docker

#### Bước 1: Chuẩn bị môi trường

1. Clone repository:
   ```
   git clone <repository-url>
   cd PhanHeNhaHang
   ```

2. Tạo và cấu hình file .env từ mẫu:
   ```
   cp .env.example .env
   ```

3. Chỉnh sửa file `.env` với các thông số phù hợp

#### Bước 2: Khởi động services với Docker Compose

```
docker-compose up -d
```

Điều này sẽ khởi động:
- MySQL/SQL Server database
- Zookeeper
- Kafka
- Kafka UI (có thể truy cập tại http://localhost:8080)

#### Bước 3: Cài đặt và chạy backend

1. Cài đặt dependencies cho backend:
   ```
   cd backend-fastapi
   pip install -r requirements.txt
   ```

2. Chạy các dịch vụ backend:
   ```
   cd order-payment-service
   uvicorn main:app --reload --port 8001
   
   # Mở terminal mới
   cd backend-fastapi/menu-service
   uvicorn main:app --reload --port 8002
   
   # Mở terminal mới
   cd backend-fastapi/kitchen-service
   uvicorn main:app --reload --port 8003
   ```

#### Bước 4: Cài đặt và chạy frontend

1. Cài đặt dependencies cho frontend:
   ```
   cd frontend
   npm install
   ```

2. Chạy frontend:
   ```
   npm start
   ```

Frontend sẽ chạy tại http://localhost:3000

### Phương thức 2: Không sử dụng Docker

#### Bước 1: Cài đặt MySQL

1. Tải và cài đặt MySQL từ [trang chủ](https://dev.mysql.com/downloads/mysql/)
2. Tạo cơ sở dữ liệu `restaurant_db`
3. Tạo người dùng và cấp quyền cho cơ sở dữ liệu

#### Bước 2: Cài đặt Kafka và Zookeeper

Xem chi tiết trong [kafka-setup-guide.md](./kafka-setup-guide.md)

#### Bước 3: Cấu hình môi trường

1. Tạo file .env từ mẫu:
   ```
   cp .env.no-docker .env
   ```
2. Chỉnh sửa file `.env` với thông tin kết nối MySQL của bạn

#### Bước 4: Chạy hệ thống

##### Windows:
```
start-system.bat
```

##### Linux/Mac:
```
chmod +x start-system.sh
./start-system.sh
```

Hoặc chạy từng thành phần theo thứ tự:
1. Zookeeper
2. Kafka
3. Backend services (order-payment, menu, kitchen)
4. Frontend

## Sử dụng Kafka

Hệ thống sử dụng Kafka để giao tiếp giữa các microservices:

- `order.created`: Khi đơn hàng được tạo
- `order.updated`: Khi đơn hàng được cập nhật
- `order.status_changed`: Khi trạng thái đơn hàng thay đổi
- `payment.processed`: Khi thanh toán được xử lý
- `dish.availability`: Thay đổi tình trạng sẵn có của món ăn
- `table.status`: Thay đổi trạng thái bàn

## Truy cập các dịch vụ

- Order-Payment Service: http://localhost:8001
- Menu Service: http://localhost:8002
- Kitchen Service: http://localhost:8003
- Frontend: http://localhost:3000
