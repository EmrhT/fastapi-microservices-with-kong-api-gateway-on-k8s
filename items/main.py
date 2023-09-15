from fastapi import FastAPI, HTTPException, Depends, Response
from typing import List
from sqlalchemy.orm import Session
from models import Item, Item_Pydantic, Item_Pydantic_Update, get_db


app = FastAPI()

# Create a GET endpoint to retrieve all items
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items


# Create a POST endpoint to create a new item
@app.post("/items/")
async def create_item(item: Item_Pydantic, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Create an UPDATE endpoint to update an existing item by its ID
@app.put("/items/{item_id}/")
async def update_item(item_id: int, updated_item: Item_Pydantic_Update, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in updated_item.dict().items():
        if value is None:
            continue
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


# Delete operation
@app.delete("/items/{item_id}", response_model=Item_Pydantic)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return Response(status_code=204)

