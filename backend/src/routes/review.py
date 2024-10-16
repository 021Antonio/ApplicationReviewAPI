from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.review import Review as ReviewSchema, ReviewCreate
from services.review import ReviewService
from db import get_db

router = APIRouter()

@router.get("/review/{review_id}")
async def get_review(review_id: int, db: Session = Depends(get_db)):
    reviewService = ReviewService(db)
    return reviewService.get(review_id)

@router.get("/review")
async def get_reviews(db: Session = Depends(get_db)):
    reviewService = ReviewService(db)
    return reviewService.get_all()

@router.post("/review")
async def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    reviewService = ReviewService(db)
    return reviewService.add(review=review)

@router.put("/review/{review_id}")
async def update_review(review_id: int, review: ReviewSchema, db: Session = Depends(get_db)):
    reviewService = ReviewService(db)
    return reviewService.update(review_id, review)

@router.delete("/review/{review_id}")
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    reviewService = ReviewService(db)
    return reviewService.delete(review_id)
