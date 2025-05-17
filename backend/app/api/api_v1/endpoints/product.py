from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status


from crud import crud_product
from schemas.product import ProductCreate, ProductUpdate, ProductInDB
from api.deps import get_db

router = APIRouter()


@router.get(
    "/",
    response_model=list[ProductInDB],
    status_code=status.HTTP_200_OK,
)
def get_products(
    db: Session = Depends(get_db),
):
    """
    Retrieve products
    """
    return crud_product.get_multi(db=db)


@router.post(
    "/",
    response_model=ProductInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    obj_in: ProductCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new product.
    """
    return crud_product.create(db=db, obj_in=obj_in)


@router.put(
    "/{product_id}/",
    response_model=ProductInDB,
    status_code=status.HTTP_201_CREATED,
)
def update_product(
    product_id: int,
    obj_in: ProductUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a product by its ID.
    """
    return crud_product.update(db=db, product_id=product_id, obj_in=obj_in)


@router.delete(
    "/{product_id}/",
    response_model=ProductInDB,
    status_code=status.HTTP_200_OK,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    Remove a product by its ID.
    """
    return crud_product.remove(db=db, id=product_id)
