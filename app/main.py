# # from fastapi import FastAPI
# # from app.routers import chat
# # from fastapi.middleware.cors import CORSMiddleware
# # app = FastAPI()
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )
# # app.include_router(chat.router, prefix="/chats")
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.routers import chat

# app = FastAPI()

# SECRET_KEY = "yoursecretkey"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# # User database with properly hashed password
# fake_users_db = {
#     "pappe": {
#         "username": "pappe", 
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p02.0BEjAj.Yy/nZGCpgxp.u"  # This is "secret"
#     }
# }

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_user(username: str):
#     return fake_users_db.get(username)

# def authenticate_user(username: str, password: str):
#     user = get_user(username)
#     if not user:
#         return False
#     if not verify_password(password, user["hashed_password"]):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(username=username)
#     if user is None:
#         raise credentials_exception
#     return user

# @app.post("/login")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user["username"]}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(chat.router, prefix="/chats")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from app.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# CORS and router add...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat.router, prefix="/chats")

from app.user_store import create_user
from fastapi import status

@app.post("/signup")
async def signup(form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required."
        )
    if create_user(form_data.username, form_data.password):
        return {"message": "User registered successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists."
        )

