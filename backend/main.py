# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user, portfolio, gamification, integrations, resume

app = FastAPI(title="Portfolio Analyzer API", version="1.0")

# Configure CORS (adjust allowed origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],  # Use "*" for dev, but restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
app.include_router(gamification.router, prefix="/gamification", tags=["Gamification"])
app.include_router(integrations.router, prefix="/integrations", tags=["Integrations"])
app.include_router(resume.router, prefix="/resume", tags=["Resume"])

@app.get("/")
def read_root():
    return {"message": "Portfolio Analyzer API is running 🚀"}
