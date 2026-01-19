# Product Management App

A TypeScript React application for managing products with create, update, and list functionality.

## Features

- **Product List Page**: View all products with pagination
- **Create Product**: Form to add new products
- **Edit Product**: Update existing product information
- **API Integration**: Connects to FastAPI backend at `/api`

## Product Fields

- **Name**: Product name (max 150 characters)
- **EAN**: 13-digit barcode number
- **Price**: Product price (numeric)
- **Description**: Product description (max 250 characters)
- **Active**: Boolean status
- **Selling Place**: Either "store" or "event"

## Setup

1. Install dependencies:
```bash
cd front/product-app
npm install
```

2. Start development server:
```bash
npm run dev
```

The app will run on http://localhost:3000

## API Endpoints Used

- `GET /api/products?page=1&size=20` - List products
- `POST /api/products` - Create product
- `PUT /api/products/{id}` - Update product

## Build for Production

```bash
npm run build
```

## Tech Stack

- React 18
- TypeScript
- React Router v6
- Vite
- CSS3
