from fastapi import FastAPI,Path
from typing import Optional
# import BaseModel when working with post and put
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    processor: str
    quantity: Optional[int]

class UpdateItem(BaseModel):
    name: Optional[str] = None
    processor: Optional[str] = None
    quantity: Optional[int] = None

inventory = {
    1: {
        "name": "laptop",
        "processor": "intel",
        "quantity": 5
    },
    2: {
        "name": "phone",
        "processor": "infinix",
        "quantity": 6
    }
}


@app.get("/")
def home():
    return {"Data": "working"}

# path parameter
@app.get("/get-items/{item_id}")
def get_items(item_id: int = Path(None, description="The ID of the item you want to view",gt=0,lt=5)):
    return inventory[item_id]


# query parameter
@app.get("/get-items-name")
def get_items(*, name: Optional[str] = None, test: int):
    for items_id in inventory:
        if inventory[items_id]["name"] == name:
            return inventory[items_id]
    return {"Data":"Not found"}

# path and query parameter
@app.get("/get-items-name/{item_id}")
def get_items(*, item_id: int, name: Optional[str] = None, test: int):
    for items_id in inventory:
        if inventory[items_id]["name"] == name:
            return inventory[items_id]
    return {"Data":"Not found"}


@app.post("/create-item/{item_id}")
def create_item(item: Item, item_id: int):
    if item_id in inventory:
        return {"Data": "item already present"}
    inventory[item_id] = {"name":item.name,"processor":item.processor,"quantity":item.quantity}
    # or
    # inventory[item_id] = item
    return inventory[item_id]



@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"data": "data does not exist"}
    if item.name != None:
        inventory[item_id].name = item.name
    if item.processor != None:
        inventory[item_id].processor = item.processor
    if item.quantity != None:
        inventory[item_id].quantity = item.quantity
    return inventory[item_id]


@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int):
    if item_id not in inventory:
        return {"Data": "data does not exist"}
    del inventory[item_id]
    return {"data": "item deleted successfully"}