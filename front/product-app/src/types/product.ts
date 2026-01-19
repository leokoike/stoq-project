export enum SellingPlace {
  EVENT = 'event',
  STORE = 'store',
}

export interface Product {
  id: string;
  name: string;
  ean: string;
  inserted_at: string;
  price: number;
  description: string;
  active: boolean;
  selling_place: SellingPlace;
  picture?: string | null;
}

export interface CreateProductDTO {
  name: string;
  ean: string;
  price: number;
  description: string;
  active: boolean;
  selling_place: SellingPlace;
  picture?: string | null;
}

export interface UpdateProductDTO {
  name?: string;
  ean?: string;
  price?: number;
  description?: string;
  active?: boolean;
  selling_place?: SellingPlace;
  picture?: string | null;
}

export interface ProductListResponse {
  items: Product[];
  total: number;
  page: number;
  size: number;
}
