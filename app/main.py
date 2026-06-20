from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.database import Base, engine, get_db
from app.model_client import request_forecast
from app.models import User
from app.schemas import ForecastRequest, ForecastResponse, LoginRequest, SignupRequest, TokenResponse


Base.metadata.create_all(bind=engine)

app = FastAPI(title="India Weather Forecast App")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/signup", response_model=TokenResponse)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        home_state=payload.home_state,
    )
    db.add(user)
    db.commit()
    return TokenResponse(access_token=create_access_token(payload.email))


@app.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return TokenResponse(access_token=create_access_token(payload.email))


@app.post("/forecast", response_model=ForecastResponse)
def forecast(payload: ForecastRequest):
    try:
        return request_forecast(payload)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Model service unavailable: {exc}") from exc
