import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import ProductList from './pages/ProductList';
import ProductForm from './pages/ProductForm';

const App: React.FC = () => {
  return (
    <>
      <nav>
        <div className="container" style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
          <h1>Product Management</h1>
          <div>
            <Link to="/">Products</Link>
            <Link to="/products/new">New Product</Link>
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/products/new" element={<ProductForm />} />
        <Route path="/products/:id" element={<ProductForm />} />
      </Routes>
    </>
  );
};

export default App;
