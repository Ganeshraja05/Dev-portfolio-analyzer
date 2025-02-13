from pydantic import BaseModel, EmailStr
from typing import Optional, List

class Portfolio(BaseModel):
    title: str
    description: Optional[str]
    url: Optional[str]
    technologies: List[str]
    rating: Optional[float] = 0.0

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"  # default role is "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Model for portfolio analysis and evaluation requests
class PortfolioAnalysisRequest(BaseModel):
    url: str
