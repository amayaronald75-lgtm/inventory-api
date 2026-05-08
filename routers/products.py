from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException
from typing import Optional

try:
    from .. import models, schemas
    from ..database import get_db
except ImportError:
    import models
    import schemas
    from database import get_db

router = APIRouter()

@router.post("/products", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    if product.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == product.category_id).first()

        if not category:
            raise HTTPException(
                status_code=400,
                detail="Invalid category_id"
            )
    
    if product.price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid price"
        )
    
    if product.stock < 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid stock"
        )

    existing_product = (
        db.query(models.Product)
        .filter(
            models.Product.name == product.name,
            models.Product.category_id == product.category_id,
        )
        .first()
    )

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Product already exists in this category"
        )
    
    if product.min_stock <0:
        raise HTTPException(
            status_code=400,
            detail="Invalid min_stock"
        )

    
    new_product = models.Product(
        name=product.name,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id,
        min_stock=product.min_stock
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/products", response_model = schemas.ProductListResponse)
def get_products(category_id: Optional[int] = None, search: Optional[str] = None, order: Optional[str] = None,
min_price: Optional[float] = None, max_price: Optional[float] = None, skip: int = 0, limit: int = 10, db: Session = 
Depends(get_db)):
    
    query = db.query(models.Product)
    
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="min_price no puede ser mayor que max_price"
        )
    if order is not None and order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="order debe ser 'asc' o 'desc'" 
        ) 

    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))
    
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)  
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
        
    if order:
        if order == "asc":
            query = query.order_by(models.Product.price)
        elif order == "desc":
            query = query.order_by(models.Product.price.desc())
    
    total = query.count()
    
    products = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "items": products
    }


@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db:
Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    return product


@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db:
Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id). first()

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    db.delete(db_product)
    db.commit()

    return


@router.patch("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int,
product: schemas.ProductUpdate, db:
Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    update_data = product.model_dump(exclude_unset=True)
    
    if "price" in update_data:
        if update_data["price"] is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid price"
            )
        if update_data["price"] <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid price"
            )
    
    if "stock" in update_data:
        if update_data["stock"] is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid stock"
            )
        if update_data["stock"] < 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid stock"
            )

    if "name" in update_data and update_data["name"] is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid name"
        )
    
    if "category_id" in update_data and update_data["category_id"] is not None:
        category_id = update_data["category_id"]
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=400,
                detail="Category not found"
            )

    new_name = update_data.get("name", db_product.name)
    new_category_id = update_data.get("category_id", db_product.category_id)
    duplicate_product = (
        db.query(models.Product)
        .filter(
            models.Product.name == new_name,
            models.Product.category_id == new_category_id,
            models.Product.id != product_id,
        )
        .first()
    )

    if duplicate_product:
        raise HTTPException(
            status_code=400,
            detail="Product already exists in this category"
        )

    for key, value in update_data.items():
        setattr(db_product, key, value)    

    db.commit()
    db.refresh(db_product)

    return db_product


    



    


