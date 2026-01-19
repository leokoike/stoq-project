import { Product, CreateProductDTO, UpdateProductDTO, ProductListResponse } from '../types/product';

const API_BASE_URL = '/api/v1';

class ProductService {

  async listProducts(page: number = 1, size: number = 20, name?: string): Promise<ProductListResponse> {
    const params = new URLSearchParams({
      page: page.toString(),
      size: size.toString(),
    });
    
    if (name && name.trim()) {
      params.append('name', name.trim());
    }
    
    const response = await fetch(`${API_BASE_URL}/products?${params.toString()}`);
    if (!response.ok) throw new Error('Failed to fetch products');
    return response.json();
  }

  async getProductById(productId: string): Promise<Product> {
    const response = await fetch(`${API_BASE_URL}/products/${productId}`);
    if (!response.ok) throw new Error(`Failed to fetch product: ${await response.text()}`);
    return response.json();
  }

  async createProduct(productData: CreateProductDTO): Promise<Product> {
    const response = await fetch(`${API_BASE_URL}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(productData),
    });
    if (!response.ok) throw new Error(`Failed to create product: ${await response.text()}`);
    return response.json();
  }

  async updateProduct(productId: string, productData: UpdateProductDTO): Promise<Product> {
    const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(productData),
    });
    if (!response.ok) throw new Error(`Failed to update product: ${await response.text()}`);
    return response.json();
  }
}

export const productService = new ProductService();
