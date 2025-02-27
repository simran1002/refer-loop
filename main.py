from fastapi import FastAPI
from .routes import auth, password, referral
from app.database import engine
from app import models
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from starlette.requests import Request
from starlette.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware


app = FastAPI(title="User Authentication & Referral System")

limiter = Limiter(key_func=lambda request: request.client.host)

app = FastAPI()

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Create database tables
models.Base.metadata.create_all(bind=engine)
app.add_middleware(SlowAPIMiddleware)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."}
    )

# Include routers
app.include_router(auth.router)
app.include_router(password.router)
app.include_router(referral.router)

@app.get("/")
def home():
    return {"message": "Welcome to the User Authentication & Referral System API!"}
