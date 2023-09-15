from fastapi import FastAPI, HTTPException, Depends, Response
from typing import List
from sqlalchemy.orm import Session
from models import Shop, Shop_Pydantic, Shop_Pydantic_Update, get_db


app = FastAPI()

# Create a GET endpoint to retrieve all shops
@app.get("/shops/")
async def read_shops(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    shops = db.query(Shop).offset(skip).limit(limit).all()
    return shops


# Create a POST endpoint to create a new shop
@app.post("/shops/")
async def create_shop(shop: Shop_Pydantic, db: Session = Depends(get_db)):
    db_shop = Shop(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop


# Create an UPDATE endpoint to update an existing shop by its ID
@app.put("/shops/{shop_id}/")
async def update_shop(shop_id: int, updated_shop: Shop_Pydantic_Update, db: Session = Depends(get_db)):
    db_shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    print(updated_shop.__dict__, updated_shop)

    for key, value in updated_shop.dict().items():
        if value is None:
            continue
        setattr(db_shop, key, value)

    db.commit()
    db.refresh(db_shop)
    return db_shop


# Delete operation
@app.delete("/shops/{shop_id}", response_model=Shop_Pydantic)
async def delete_shop(shop_id: int, db: Session = Depends(get_db)):
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if shop is None:
        raise HTTPException(status_code=404, detail="shop not found")
    db.delete(shop)
    db.commit()
    return Response(status_code=204)

