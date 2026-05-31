from fastapi import FastAPI, HTTPException, Query, Path, status
from pydantic import BaseModel, Field

app = FastAPI()

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    category: str


class Product(ProductCreate):
    id: int


products: list[Product] = [
    Product(id=1, name="Телефон", price=50000, category="electronics"),
    Product(id=2, name="Ноутбук", price=75000, category="electronics"),
    Product(id=3, name="Мышка", price=1500, category="accessories"),
    Product(id=4, name="Клвиатура", price=3000, category="accessories")
]



@app.get("/")
def read_root():
    return {"message": "hello"}



@app.get("/products", response_model=list[Product])
def get_products():
    return products


@app.get("/products/{id}", response_model=Product)
def get_product(
        id: int = Path(gt=0)
):
    for product in products:
        if product.id == id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product nt found"
    )


@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductCreate):

    new_product = Product(
        id=len(products) + 1,
        name=product.name,
        price=product.price,
        category=product.category
    )

    products.append(new_product)

    return new_product
@app.get("/products/search", response_model=list[Product])
def search_products(
        name: str = Query(default=None),
        min_price: float = Query(default=None, ge=0),
        category: str = Query(default=None)
):
    result = products

    if name:
        result = [
            p for p in result
            if name.lower() in p.name.lower()
        ]

    if min_price is not None:
        result = [
            p for p in result
            if p.price >= min_price
        ]

    if category:
        result = [
            p for p in result
            if p.category.lower() == category.lower()
        ]

    return result


@app.delete("/products/{id}")
def delete_product(id: int):

    for product in products:
        if product.id == id:
            products.remove(product)
            return {"message": "Product deleted"}

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )



@app.put("/products/{id}", response_model=Product)
def update_product(id: int, updated_product: ProductCreate):

    for product in products:
        if product.id == id:
            product.name = updated_product.name
            product.price = updated_product.price
            product.category = updated_product.category

            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )
