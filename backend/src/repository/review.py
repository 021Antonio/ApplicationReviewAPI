from models.review import Review
from sqlalchemy.orm import Session

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, produto_id):
        return self.db.query(Review).get(review_id)

    def get_all(self):
        return self.db.query(Review).all()

    def add(self, review: Review):
        review.id = None
        self.db.add(review)
        self.db.flush()
        self.db.commit()
        return {"message": "Review cadastrado com sucesso"}

    def update(self, review_id, review):
        reviewdb = self.db.query(Review).filter(Review.id == review).first()
        if reviewdb is None:
            return {"message": "Review não encontrado"}
        review = review.__dict__
        review.pop("_sa_instance_state")
        review.pop("estrelas")
        review.pop("id")
        self.db.query(Review).filter(Review.id == review_id).update(review)
        self.db.flush()
        self.db.commit()
        return {"message": "Review atualizado com sucesso"}

    def delete(self, review_id):
        reviewdb = self.db.query(Review).filter(Review.id == review_id).first()
        if review_db is None:
            return {"message": "Review não encontrado"}
        self.db.query(Review).filter(Review.id == review_id).delete()
        self.db.flush()
        self.db.commit()
        return {"message": "Review deletado com sucesso"}
        