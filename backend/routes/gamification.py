from fastapi import APIRouter, HTTPException, Depends
from models import PortfolioAnalysisRequest
from services.portfolio_analyzer import extract_clean_text
from services.ai_evaluator import evaluate_text
from services.dynamic_scoring import compute_dynamic_scores
from services.gamification import compute_portfolio_level, get_career_recommendations
from auth.auth_bearer import JWTBearer

router = APIRouter()

@router.post("/gamify", dependencies=[Depends(JWTBearer())])
async def gamify_portfolio(request: PortfolioAnalysisRequest):
    """
    Compute the portfolio level based on dynamic scores.
    Returns the level (Beginner, Intermediate, Expert) and the aggregate score.
    """
    try:
        text = extract_clean_text(request.url)
        evaluation = evaluate_text(text)
        scores = compute_dynamic_scores(text, evaluation)
        level_info = compute_portfolio_level(scores)
        return level_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/career", dependencies=[Depends(JWTBearer())])
async def career_insights(request: PortfolioAnalysisRequest):
    """
    Provide career insights and job matching recommendations based on portfolio dynamic scores.
    Returns a list of recommended job roles.
    """
    try:
        text = extract_clean_text(request.url)
        evaluation = evaluate_text(text)
        scores = compute_dynamic_scores(text, evaluation)
        career_info = get_career_recommendations(scores)
        return career_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
