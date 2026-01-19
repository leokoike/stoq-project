import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { productService } from '../services/productService';
import { SellingPlace } from '../types/product';

const ProductForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditMode = !!id;

  const [formData, setFormData] = useState({
    name: '',
    ean: '',
    price: '',
    description: '',
    active: true,
    selling_place: SellingPlace.STORE,
    picture: null as string | null,
  });

  const [picturePreview, setPicturePreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [initialLoading, setInitialLoading] = useState(isEditMode);

  useEffect(() => {
    if (isEditMode && id) {
      loadProduct(id);
    }
  }, [id, isEditMode]);

  const loadProduct = async (productId: string) => {
    try {
      setInitialLoading(true);
      setError(null);
      const product = await productService.getProductById(productId);
      setFormData({
        name: product.name,
        ean: product.ean,
        price: product.price.toString(),
        description: product.description,
        active: product.active,
        selling_place: product.selling_place,
        picture: product.picture || null,
      });
      if (product.picture) {
        setPicturePreview(`data:image/jpeg;base64,${product.picture}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load product');
    } finally {
      setInitialLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file');
      return;
    }

    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
      setError('Image size must be less than 5MB');
      return;
    }

    try {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result as string;
        const base64Data = base64String.split(',')[1];
        setFormData(prev => ({ ...prev, picture: base64Data }));
        setPicturePreview(base64String);
      };
      reader.readAsDataURL(file);
    } catch (err) {
      setError('Failed to read image file');
    }
  };

  const handleRemovePicture = () => {
    setFormData(prev => ({ ...prev, picture: null }));
    setPicturePreview(null);
  };

  const validateEAN = (ean: string): boolean => {
    return /^\d{13}$/.test(ean);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!validateEAN(formData.ean)) {
      setError('EAN must be exactly 13 digits');
      return;
    }

    const price = parseFloat(formData.price);
    if (isNaN(price) || price < 0) {
      setError('Price must be a valid positive number');
      return;
    }

    try {
      setLoading(true);
      const productData = {
        name: formData.name,
        ean: formData.ean,
        price: price,
        description: formData.description,
        active: formData.active,
        selling_place: formData.selling_place,
        picture: formData.picture,
      };

      if (isEditMode && id) {
        await productService.updateProduct(id, productData);
        setSuccess('Product updated successfully!');
      } else {
        await productService.createProduct(productData);
        setSuccess('Product created successfully!');
        setTimeout(() => navigate('/'), 1500);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save product');
    } finally {
      setLoading(false);
    }
  };

  if (initialLoading) return <div className="loading">Loading product...</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>{isEditMode ? 'Edit Product' : 'Create New Product'}</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Product Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              maxLength={150}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="ean">EAN (13 digits) *</label>
            <input
              type="text"
              id="ean"
              name="ean"
              value={formData.ean}
              onChange={handleChange}
              pattern="\d{13}"
              maxLength={13}
              placeholder="1234567890123"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="price">Price *</label>
            <input
              type="number"
              id="price"
              name="price"
              value={formData.price}
              onChange={handleChange}
              step="0.01"
              min="0"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              maxLength={250}
              required
            />
          </div>

          <div className="form-group">
            <label>Selling Place *</label>
            <div className="radio-group">
              <label className="radio-label">
                <input
                  type="radio"
                  name="selling_place"
                  value={SellingPlace.STORE}
                  checked={formData.selling_place === SellingPlace.STORE}
                  onChange={handleChange}
                />
                <span>Store</span>
              </label>
              <label className="radio-label">
                <input
                  type="radio"
                  name="selling_place"
                  value={SellingPlace.EVENT}
                  checked={formData.selling_place === SellingPlace.EVENT}
                  onChange={handleChange}
                />
                <span>Event</span>
              </label>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="active">Active</label>
            <label className="toggle">
              <input
                type="checkbox"
                id="active"
                name="active"
                checked={formData.active}
                onChange={handleChange}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="picture">Product Picture</label>
            <input
              type="file"
              id="picture"
              name="picture"
              accept="image/*"
              onChange={handleFileChange}
              style={{ display: 'block' }}
            />
            <small style={{ color: '#666', fontSize: '0.875rem' }}>
              Max file size: 5MB. Accepted formats: JPG, PNG, GIF, WebP
            </small>
            
            {(picturePreview || formData.picture) && (
              <div style={{ marginTop: '1rem' }}>
                <img 
                  src={picturePreview || `data:image/jpeg;base64,${formData.picture}`} 
                  alt="Product preview" 
                  style={{ maxWidth: '200px', maxHeight: '200px', objectFit: 'contain', borderRadius: '8px', border: '1px solid #ddd' }}
                />
                <button
                  type="button"
                  onClick={handleRemovePicture}
                  className="secondary"
                  style={{ display: 'block', marginTop: '0.5rem', fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                >
                  Remove Picture
                </button>
              </div>
            )}
          </div>

          {error && <div className="error">{error}</div>}
          {success && <div className="success">{success}</div>}

          <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
            <button type="submit" className="primary" disabled={loading}>
              {loading ? 'Saving...' : isEditMode ? 'Update Product' : 'Create Product'}
            </button>
            <button type="button" className="secondary" onClick={() => navigate('/')}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProductForm;
