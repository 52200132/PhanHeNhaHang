import { Outlet } from 'react-router-dom';
import Header from './components/layout/Header';
import './styles/global.css';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}

export default App;
