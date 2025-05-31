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
- MySQL

### Cài đặt - Trên windows

#### Backend

##### Bước 1: Cài các thư viện python

- Mở terminal tại thư mục chứ backend và frontend

   ```
   cd backend-fastapi
   pip install -r requirements.txt
   ```

##### Bước 2: Thiết lập biến môi trường

- Tạo một file backend-fastapi/.env và cấu hình cho phù hợp trên thiết bị của bạn

   ```
   DB_USERNAME=root
   DB_PASSWORD=
   DB_SERVER=localhost:3333

   DB_NAME_1=menu_service_db
   DB_NAME_2=order_payment_service_db
   DB_NAME_3=kitchent_service_db
   ```

##### Bước 3: Cài đặt MySQL

- Tạo các cơ sở dữ liệu giống với `DB_NAME_1`, `DB_NAME_3`, `DB_NAME_2`

##### Bước 4: Chạy các dịch vụ backend

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

#### Frontend

##### Bước 1: Thiết lập biến môi trường

- Tạo file frontend/.env và cấu hình

   ```
   REACT_APP_MENU_SERVICE_URL=http://localhost:8001/api/v1

   REACT_APP_ORDER_SERVICE_URL=http://localhost:8002/api/v1

   REACT_APP_KITCHEN_SERVICE_URL=http://localhost:8003/api/v1
   ```

##### Bước 2: Cài đặt các package và chạy front end

- Mở terminal tại thư mục gốc

   ```
   # Cài đặt thư viện
   cd frontend
   npm install

   # Chạy front end
   npm start
   ```

#### Truy cập các dịch vụ

- Order-Payment Service: http://localhost:8001
- Menu Service: http://localhost:8002
- Kitchen Service: http://localhost:8003
- Frontend: http://localhost:3000
