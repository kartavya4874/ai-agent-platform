from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User, Subscription
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
import os
import stripe
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class SubscriptionCreate(BaseModel):
    plan_type: str
    user_id: int

class SubscriptionResponse(BaseModel):
    id: int
    plan_type: str
    is_active: bool
    start_date: datetime
    end_date: Optional[datetime] = None
    
@router.post("/create", response_model=SubscriptionResponse)
async def create_subscription(sub: SubscriptionCreate, db: Session = Depends(get_db)):
    """Create a free trial subscription"""
    # Check if user exists
    user = db.query(User).filter(User.id == sub.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user already has an active subscription
    existing_sub = db.query(Subscription).filter(
        Subscription.user_id == sub.user_id,
        Subscription.is_active == True
    ).first()
    
    if existing_sub:
        raise HTTPException(status_code=400, detail="User already has an active subscription")
    
    # Create trial subscription (valid for 7 days)
    end_date = datetime.utcnow() + timedelta(days=7)
    new_sub = Subscription(
        user_id=sub.user_id,
        plan_type=sub.plan_type,
        is_active=True,
        start_date=datetime.utcnow(),
        end_date=end_date
    )
    
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    
    return new_sub

@router.get("/status/{user_id}", response_model=SubscriptionResponse)
async def get_subscription_status(user_id: int, db: Session = Depends(get_db)):
    """Get user's subscription status"""
    # Get user's active subscription
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.is_active == True
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription found")
    
    return subscription

@router.post("/create-checkout-session/{user_id}")
async def create_checkout_session(user_id: int, plan_type: str, db: Session = Depends(get_db)):
    """Create Stripe checkout session for subscription"""
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create Stripe checkout session
    try:
        # Define price IDs based on plan type
        price_ids = {
            "basic": "price_1234",  # Replace with actual Stripe price IDs
            "premium": "price_5678"
        }
        
        if plan_type not in price_ids:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_ids[plan_type],
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url="http://localhost:8501/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8501/cancel",
            client_reference_id=str(user_id),
        )
        
        return {"checkout_url": checkout_session.url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include this route in the main.py file as well
