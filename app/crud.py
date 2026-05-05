from sqlalchemy.orm import Session
from . import models
from .ml.predict import predict_customer

# Create Customer + Prediction
def create_customer(db: Session, data: dict):
    
    # 1. Save customer
    customer = models.Customer(**data)
    db.add(customer)
    db.commit()
    db.refresh(customer)

    # 2. Run prediction
    result = predict_customer(data)

    # 3. Save prediction
    prediction = models.Prediction(
        customer_id=customer.id,
        prediction=result["prediction"],
        probability=result["probability"]
    )

    db.add(prediction)
    db.commit()

    return customer, prediction


# Update Customer + Re-Predict
def update_customer(db: Session, customer_id: int, data: dict):

    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()

    if not customer:
        return None

    # Update fields
    for key, value in data.items():
        setattr(customer, key, value)

    db.commit()

    # Re-run prediction
    result = predict_customer(data)

    prediction = db.query(models.Prediction).filter(
        models.Prediction.customer_id == customer_id
    ).first()

    if prediction:
        prediction.prediction = result["prediction"]
        prediction.probability = result["probability"]

    db.commit()

    return customer, prediction


# Get All Customers + Predictions
def get_customers(db: Session):
    customers = db.query(models.Customer).all()
    predictions = db.query(models.Prediction).all()

    pred_map = {p.customer_id: p for p in predictions}

    result = []
    for c in customers:
        p = pred_map.get(c.id)

        result.append({
            "id": c.id,
            "gender": c.gender,
            "SeniorCitizen": c.SeniorCitizen,
            "tenure": c.tenure,
            "MonthlyCharges": c.MonthlyCharges,
            "Contract": c.Contract,
            "prediction": p.prediction if p else None,
            "probability": p.probability if p else None
        })

    return result


# -------------------------
# Get single customer
# -------------------------
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


# -------------------------
# Get prediction for a customer
# -------------------------
def get_prediction(db: Session, customer_id: int):
    return db.query(models.Prediction).filter(models.Prediction.customer_id == customer_id).first()


# -------------------------
# Delete customer + prediction
# -------------------------
def delete_customer(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        return False

    # Delete prediction first
    db.query(models.Prediction).filter(models.Prediction.customer_id == customer_id).delete()

    # Delete customer
    db.delete(customer)
    db.commit()
    return True
