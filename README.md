# 🚀 Customer Churn Prediction API

This is the backend API for the Customer Churn Prediction platform. It handles customer data storage and serves machine learning predictions for churn probability.

---

## 📡 Base URL
- **Local Development:** `http://127.0.0.1:8000`
- **Hugging Face Space:** `https://abdulqayyum360-custoemer-churn-prediction.hf.space`

---

## 🛠 API Endpoints

### 1. Customers Management

#### 📥 Get All Customers
- **Endpoint:** `GET /customers`
- **Description:** Retrieves a list of all customers in the database.
- **Response:** `Array of Customer Objects`

#### 🔍 Get Customer by ID
- **Endpoint:** `GET /customers/{id}`
- **Description:** Retrieves details for a specific customer, including their latest churn prediction and probability.
- **Response:**
  ```json
  {
    "customer": { ...data... },
    "prediction": "Churn" or "No Churn",
    "probability": 0.85
  }
  ```

#### ➕ Add New Customer
- **Endpoint:** `POST /customers`
- **Description:** Adds a new customer to the database and runs the ML model to generate an immediate churn prediction.
- **Request Body (JSON):**
  ```json
  {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 1,
    "PhoneService": "No",
    "MultipleLines": "No phone service",
    "InternetService": "DSL",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 29.85,
    "TotalCharges": 29.85
  }
  ```
- **Response:**
  ```json
  {
    "message": "Customer added",
    "customer_id": 1,
    "prediction": "Churn",
    "probability": 0.72
  }
  ```

#### 📝 Update Customer
- **Endpoint:** `PUT /customers/{id}`
- **Description:** Updates an existing customer's information and recalculates their churn prediction.
- **Request Body:** Same as **Add New Customer**.

#### ❌ Delete Customer
- **Endpoint:** `DELETE /customers/{id}`
- **Description:** Deletes a customer record from the database.

---

## 🧪 Interactive Documentation
Once the server is running, you can access the interactive Swagger UI at:
- **Local:** `http://127.0.0.1:8000/docs`
- **Deployed:** `https://abdulqayyum360-custoemer-churn-prediction.hf.space/docs`
