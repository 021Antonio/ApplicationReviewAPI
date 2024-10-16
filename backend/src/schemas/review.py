from pydantic import BaseModel

class ReviewBase(BaseModel):
    nome: str
    review: str
    estrelas: int  
    serie_filme: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True
