import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import MenuPage from './pages/MenuManagement/MenuPage';
import OrderPage from './pages/OrderSystem/OrderPage';
import KitchenPage from './pages/KitchenDisplay/KitchenPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <OrderPage />
      },
      {
        path: '/menu',
        element: <MenuPage />
      },
      {
        path: '/orders',
        element: <OrderPage />
      },
      {
        path: '/kitchen',
        element: <KitchenPage />
      }
    ]
  }
]);

export default router;
