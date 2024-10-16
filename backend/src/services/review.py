from fastapi import HTTPException
from sqlalchemy.orm import Session
from repository.review import ReviewRepository
from models.review import Review
from schemas.review import Review as ReviewSchema, ReviewCreate

class ReviewService:
    def __init__(self, db: Session):
        self.repository = ReviewRepository(db)

    def get(self, review_id):
        review = self.repository.get(review_id)
        if review is None:
            raise HTTPException(status_code=404, detail="review não encontrado")
        return review

    def get_all(self):
        return self.repository.get_all()

    def add(self, review: ReviewCreate):
        review = Review(**review.dict())
        return self.repository.add(review)

    def update(self, review_id, review: ReviewSchema):
        review = Review(**review.dict())
        return self.repository.update(review_id, review)

    def delete(self, review_id):
        return self.repository.delete(review_id)
