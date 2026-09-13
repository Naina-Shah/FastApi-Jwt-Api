from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import model


from schemas import UserCreate, ProductCreate,UserLogin
from auth import pwd_context

from fastapi import HTTPException
from auth import pwd_context, create_access_token, get_current_user



Base.metadata.create_all(bind= engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API is working!"}

def get_db():
    db= SessionLocal()
    try:
        yield db

    finally:
        db.close()


#============== Registration Form ===============
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(model.User).filter(
        model.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = db.query(model.User).filter(
        model.User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_password = pwd_context.hash(user.password)

    new_user = model.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }

#=================== Login =======================
@app.post("/login")
def login(user_data: UserLogin , db: Session = Depends(get_db)):
    user = db.query(model.User).filter(
        model.User.username == user_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token({
        "sub": user.username
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


#==============Profile ========================
@app.get("/profile")
def profile(current_user: str = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "username": current_user
    }
#================ Product ys Price ===============
@app.post("/products")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    new_product = model.Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

current_user: str = Depends(get_current_user)


#===================DB Session =============
@app.get("/products")
def get_products(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db.query(model.Product).all()

#=================Retrive =============
@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    product = db.query(model.Product).filter(
        model.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

#=================Update ===============
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    existing_product = db.query(model.Product).filter(
        model.Product.id == product_id
    ).first()

    if not existing_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing_product.name = product.name
    existing_product.price = product.price

    db.commit()
    db.refresh(existing_product)

    return existing_product


#====================Delete ===============
@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    product = db.query(model.Product).filter(
        model.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }