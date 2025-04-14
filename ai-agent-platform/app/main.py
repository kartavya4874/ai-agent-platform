import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db.database import engine, get_db
from app.models import models
from dotenv import load_dotenv
from app.api.routes import auth, ai_tools, subscription

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Agent Platform")

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(ai_tools.router, prefix="/api/tools", tags=["AI Tools"])
app.include_router(subscription.router, prefix="/api/subscription", tags=["Subscription"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Agent Platform"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
