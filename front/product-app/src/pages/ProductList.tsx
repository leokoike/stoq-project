import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { productService } from '../services/productService';
import { Product } from '../types/product';
import Pagination from '../components/Pagination';

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [size, setSize] = useState(20);
  const [viewProduct, setViewProduct] = useState<Product | null>(null);
  const [showViewModal, setShowViewModal] = useState(false);
  const [nameFilter, setNameFilter] = useState('');
  const [searchInput, setSearchInput] = useState('');

  useEffect(() => {
    loadProducts();
  }, [page, size, nameFilter]);

  const loadProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await productService.listProducts(page, size, nameFilter);
      setProducts(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const handleViewProduct = (product: Product) => {
    setViewProduct(product);
    setShowViewModal(true);
  };

  const handleCloseModal = () => {
    setShowViewModal(false);
    setViewProduct(null);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    setNameFilter(searchInput);
  };

  const handleClearFilter = () => {
    setSearchInput('');
    setNameFilter('');
    setPage(1);
  };

  const handleSizeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newSize = parseInt(e.target.value, 10);
    setSize(newSize);
    setPage(1);
  };

  if (loading) return <div className="loading">Loading products...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>Products</h2>
        <Link to="/products/new">
          <button className="primary">Create Product</button>
        </Link>
      </div>

      <div className="filter-section">
        <form onSubmit={handleSearch} className="filter-form">
          <div className="filter-group">
            <input
              type="text"
              placeholder="Search by product name..."
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              className="filter-input"
            />
            <button type="submit" className="primary">
              Search
            </button>
            {nameFilter && (
              <button type="button" className="secondary" onClick={handleClearFilter}>
                Clear Filter
              </button>
            )}
          </div>
          <div className="filter-group">
            <label htmlFor="pageSize" style={{ marginRight: '0.5rem', fontWeight: '500' }}>
              Items per page:
            </label>
            <select 
              id="pageSize"
              value={size} 
              onChange={handleSizeChange}
              className="page-size-select"
            >
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
        </form>
        {nameFilter && (
          <div className="active-filter">
            Filtering by: <strong>{nameFilter}</strong>
          </div>
        )}
      </div>

      {products.length === 0 ? (
        <div className="card">
          <p>No products found. Create your first product!</p>
        </div>
      ) : (
        <>
          <table>
            <thead>
              <tr>
                <th>Picture</th>
                <th>Name</th>
                <th>EAN</th>
                <th>Price</th>
                <th>Status</th>
                <th>Selling Place</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id}>
                  <td>
                    {product.picture ? (
                      <img 
                        src={`data:image/jpeg;base64,${product.picture}`} 
                        alt={product.name}
                        style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '4px' }}
                      />
                    ) : (
                      <div style={{ width: '50px', height: '50px', backgroundColor: '#e0e0e0', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', color: '#666' }}>
                        No image
                      </div>
                    )}
                  </td>
                  <td>{product.name}</td>
                  <td>{product.ean}</td>
                  <td>${product.price.toFixed(2)}</td>
                  <td>
                    <span className={`badge ${product.active ? 'active' : 'inactive'}`}>
                      {product.active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${product.selling_place}`}>
                      {product.selling_place}
                    </span>
                  </td>
                  <td>
                    <button 
                      onClick={() => handleViewProduct(product)}
                      className="secondary" 
                      style={{ fontSize: '0.875rem', padding: '0.5rem 1rem', marginRight: '0.5rem' }}
                    >
                      View
                    </button>
                    <Link to={`/products/${product.id}`}>
                      <button className="secondary" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}>
                        Edit
                      </button>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <Pagination
            currentPage={page}
            totalItems={total}
            itemsPerPage={size}
            onPageChange={setPage}
          />
        </>
      )}

      {showViewModal && viewProduct && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Product Details</h2>
              <button className="modal-close" onClick={handleCloseModal}>&times;</button>
            </div>
            <div className="modal-body">
              {viewProduct.picture && (
                <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
                  <img 
                    src={`data:image/jpeg;base64,${viewProduct.picture}`} 
                    alt={viewProduct.name}
                    style={{ maxWidth: '100%', maxHeight: '300px', objectFit: 'contain', borderRadius: '8px', border: '1px solid #ddd' }}
                  />
                </div>
              )}
              <div className="detail-row">
                <strong>Name:</strong>
                <span>{viewProduct.name}</span>
              </div>
              <div className="detail-row">
                <strong>EAN:</strong>
                <span>{viewProduct.ean}</span>
              </div>
              <div className="detail-row">
                <strong>Price:</strong>
                <span>${viewProduct.price.toFixed(2)}</span>
              </div>
              <div className="detail-row">
                <strong>Description:</strong>
                <span>{viewProduct.description}</span>
              </div>
              <div className="detail-row">
                <strong>Status:</strong>
                <span className={`badge ${viewProduct.active ? 'active' : 'inactive'}`}>
                  {viewProduct.active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className="detail-row">
                <strong>Selling Place:</strong>
                <span className={`badge ${viewProduct.selling_place}`}>
                  {viewProduct.selling_place}
                </span>
              </div>
              <div className="detail-row">
                <strong>Created:</strong>
                <span>{new Date(viewProduct.inserted_at).toLocaleString()}</span>
              </div>
            </div>
            <div className="modal-footer">
              <button className="secondary" onClick={handleCloseModal}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductList;
