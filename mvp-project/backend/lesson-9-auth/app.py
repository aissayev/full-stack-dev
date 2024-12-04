# JWT

from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

SECRET_KEY = "QDOgm0tI0zJ5plPi95Cpf4gd5BRvVDgpk6gg5eQiigY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    # Добавляем дату истечения токена
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Поле "exp" указывает, когда токен истечет
    
    # Генерируем токен
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Возвращаем данные токена, если он валиден
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# Create a MongoDB client
client = AsyncIOMotorClient("mongodb://localhost:27017")

# Access a database and collection
db = client.fullstack
collection = db.students

app = FastAPI()

class User(BaseModel):
    id: Optional[int] = None
    name: str
    # age: int
    email: str
    password: str
    # role: str

class LoginUser(BaseModel):
    email: str
    password: str


async def create_user_in_db(user: User):
    document = {"name": user.name, "age": user.age, "email": user.email}
    result = await collection.insert_one(document)
    print(f"Inserted document ID: {result.inserted_id}")


@app.get("/")
async def hello():
    return "Hello"


# CRUD - Create Read Update Delete



@app.post("/users")
async def create_user(user: User):
    await create_user_in_db(user)
    return {"message": f"User {user.name} created successfully!"}

@app.post("/auth/register")
async def register_user(user: User):
    

    query = {"email": user.email}
    saved_user = await collection.find_one(query)

    print(saved_user)

    if saved_user is not None:
        return {"error": "Email already exists"}
    else: 
        # Хеширование пароля
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        document = {"name": user.name, "email": user.email, "password": hashed_password}
        result = await collection.insert_one(document)
        print(f"Register user ID: {result.inserted_id}")
        return {"message": "User registered successfully"}
    

@app.post("/auth/login")
async def login_user(user: LoginUser):
    
    query = {"email": user.email}
    saved_user = await collection.find_one(query)

    if saved_user is None:
      return {"error": "Wrong Credentials"}
    
    print("password")
    print(saved_user["password"])
    
    # Проверка пароля
    if not bcrypt.checkpw(user.password.encode('utf-8'), saved_user["password"].encode('utf-8')):
        return {"error": "Invalid email or password"}
    
    token = create_access_token({"email": user.email, "name": saved_user["name"]})
    
    return {"message": f"Welcome, {saved_user['name'], token }"}



   
@app.get("/me")
def get_my_info(token: str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    return {"message": f"Welcome, your email is {user_data['email']}"}