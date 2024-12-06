# SPA-app API

The **SPA-app API** is a DjangoRestFramework- and vue.js-based project for managing comments

## Installing

### Prerequisites

- Python 3.8+
- Install PostgreSQL and create db
- Docker

### Steps to Install Locally

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/vladislav-tsybuliak1/spa-app.git
    cd spa-app
    ```

2. **Create a Virtual Environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:

    ```bash
    cd backend
    pip install -r requirements.txt
    ```
4. **Create .env files and set up environment variables**:

    See ```env.sample``` in frontend & backend folders

5. **Run Migrations**:

    ```bash
    python manage.py migrate
    ```

6. **Start Backend Server**:

    ```bash
    python manage.py runserver
    ```

7. **Start Frontend APP**:
    
   ```bash
    cd ../frontend
    npm install
    npm run dev
    ```

## Run with Docker

### Steps to Run Using Docker

1. **Build the Docker Image**:

    ```bash
    docker-compose build
    ```

2. **Start the Backend Service & PostgreSQL db**:

    ```bash
    docker-compose up
    ```

## **Access the app**

   - The API will be available at `http://localhost:8000/`.
   - The vue.js frontend will be available at `http://localhost:8080/`.

## Contact
For any inquiries, please contact [vladislav.tsybuliak@gmail.com](mailto:vladislav.tsybuliak@gmail.com).
