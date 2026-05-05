from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI()


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 1️⃣ Add Customer
# =========================
@app.post("/customers")
def add_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    c, p = crud.create_customer(db, customer.dict())

    return {
        "message": "Customer added",
        "customer_id": c.id,
        "prediction": p.prediction,
        "probability": p.probability
    }


# =========================
# 2️⃣ Update Customer
# =========================
@app.put("/customers/{id}")
def update_customer(id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    result = crud.update_customer(db, id, customer.dict())

    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")

    c, p = result

    return {
        "message": "Customer updated",
        "prediction": p.prediction,
        "probability": p.probability
    }


# =========================
# 3️⃣ Get Customers
# =========================
@app.get("/customers")
def get_all_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)

# =========================
# 4️⃣ Get Customer by ID
# =========================
@app.get("/customers/{id}")
def get_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Include prediction if exists
    prediction = crud.get_prediction(db, id)
    
    return {
        "customer": customer,
        "prediction": prediction.prediction if prediction else "N/A",
        "probability": prediction.probability if prediction else 0
    }


# =========================
# 5️⃣ Delete Customer by ID
# =========================
@app.delete("/customers/{id}")
def delete_customer(id: int, db: Session = Depends(get_db)):
    success = crud.delete_customer(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"message": f"Customer {id} deleted successfully"}