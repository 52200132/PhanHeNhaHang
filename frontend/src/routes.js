import { createBrowserRouter } from 'react-router-dom';
import App from './App';
// import MenuPage from './pages/MenuManagement/MenuPage';
import OrderPage from './pages/OrderSystem/OrderPage';
import KitchenPage from './pages/KitchenDisplay/KitchenPage';
import GuestMenu from './pages/Menu/GuestMenu';
import HomePage from './pages/Home/HomePage';
import StaffPage from './pages/Staff/StaffPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <HomePage />
      },
      // {
      //   path: '/menu',
      //   element: <MenuPage />
      // },
      {
        path: '/orders',
        element: <OrderPage />
      },
      {
        path: '/kitchen',
        element: <KitchenPage />
      },
      {
        path: '/guest-menu',
        element: <GuestMenu />
      },
      {
        path: '/staff',
        element: <StaffPage />
      }
    ]
  }
]);

export default router;
