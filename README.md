# STOQ PROJECT

## Requirements
- Docker and Docker Compose
- Node.js (for frontend)
- Python 3.12+
- UV (for Python dependency management)
- NPM (for frontend dependency management)
- Make (for command execution)

## Setup Instructions

1. **Clone the Repository** \
    ```bash
    git clone https://github.com/leokoike/stoq-project.git
    cd stoq-project
    ```

2. **Backend Setup** \
    Ensure you have Python 3.12+ installed. Then, check if you have UV installed. If not, install it using pip:
    ```bash
    pip install uv
    ```
    From the root directory, navigate to the `api` directory and install dependencies:
    ```bash
    cd api
    uv sync
    ```

3. **Frontend Setup** \
    From the root directory, navigate to the `product-app` directory and install dependencies:
    ```bash
    cd front/product-app
    npm install
    ```

4. **Running the Application** \
    Create .env file for backend configuration:
    ```bash
    cd api
    cp .env.example .env
    ```
    From the root directory, you can use make commands to build the application:
    ```bash
    make build-api
    make build-frontend
    ```
    To run the API application and the database:
    ```bash
    make run-api
    ```
    To run the database migrations:
    ```bash
    make upgrade
    ```
    To seed the database with initial data, run the following command from the root directory:
    ```bash
    make seed-products
    ```
    To run the frontend application:
    ```bash
    make run-frontend
    ```
    And access it at `http://localhost:3000`.

5. **Stopping the Application** \
    To stop the backend application, you can use:
    ```bash
    make stop-api
    ```
    To stop the frontend application, use Ctrl + C in the terminal where it's running.

6. **Running Testing** \
    To run backend tests, in the root directory and execute:
    ```bash
    make test-api
    ```