from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from .. import models, schemas
    from ..database import get_db
except ImportError:
    import models
    import schemas
    from database import get_db

router = APIRouter()

@router.post("/categories", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db) 
):
    existing_category = (
        db.query(models.Category)
        .filter(models.Category.name == category.name)
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = models.Category(name=category.name)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.get("/categories/", response_model = list[schemas.Category])
def get_categories(db: Session =
Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

@router.get("/categories/{category_id}", response_model=schemas.Category)
def get_categories(category_id: int, db:
Session = Depends(get_db)):
    categories = db.query(models.Category).filter(models.Category.id == category_id).first()
    
    if not categories:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    return categories
    
@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db:
Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    
    return{"mensaje": "Category deleted"}

@router.patch("/categories/{category_id}", response_model=schemas.Category)
def patch_category(category_id: int,
category: schemas.CategoryUpdate, db:
Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    if category.name is not None:
        existing_category = (
            db.query(models.Category)
            .filter(
                models.Category.name == category.name,
                models.Category.id != category_id,
            )
            .first()
        )

        if existing_category:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

    update_data = category.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)

    return db_category

#Productos dentro de una categoria

@router.get("/categories/{category_id}/products", response_model=schemas.CategoryWithProducts)
def get_category_products(
    category_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):   
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    products = db.query(models.Product).filter(models.Product.category_id == category_id).offset(skip).limit(limit).all()

    category.products = products

    return category
