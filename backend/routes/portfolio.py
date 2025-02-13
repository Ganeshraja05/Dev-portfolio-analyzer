from fastapi import APIRouter, HTTPException, Depends
from models import Portfolio, PortfolioAnalysisRequest
from database import database
from services.portfolio_analyzer import extract_clean_text, analyze_portfolio
from services.ai_evaluator import evaluate_text
from services.dynamic_scoring import compute_dynamic_scores
from services.auto_enhancements import generate_enhancement_suggestions
from services.gamification import compute_portfolio_level, get_career_recommendations
from auth.auth_bearer import JWTBearer

router = APIRouter()

@router.post("/add", dependencies=[Depends(JWTBearer())])
async def add_portfolio(portfolio: Portfolio):
    """
    Add a new portfolio to the database.
    """
    result = await database.portfolios.insert_one(portfolio.dict())
    return {"message": "Portfolio added successfully", "id": str(result.inserted_id)}

@router.get("/{portfolio_id}", dependencies=[Depends(JWTBearer())])
async def get_portfolio(portfolio_id: str):
    """
    Retrieve a portfolio by its ID from the database.
    """
    portfolio = await database.portfolios.find_one({"_id": portfolio_id})
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.post("/analyze", dependencies=[Depends(JWTBearer())])
async def portfolio_analysis(request: PortfolioAnalysisRequest):
    """
    Analyze a portfolio website using web scraping and basic AI insights.
    Returns metadata and a snippet of the content.
    """
    url = request.url
    try:
        extracted_text = extract_clean_text(url)
        metadata = analyze_portfolio(url)
        return {
            "metadata": metadata,
            "content_analysis": extracted_text[:1000] + "..."  # Limit output length for brevity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate", dependencies=[Depends(JWTBearer())])
async def evaluate_portfolio(request: PortfolioAnalysisRequest):
    """
    Evaluate the portfolio content using AI-based NLP techniques.
    Provides sentiment scores and a readability score.
    """
    url = request.url
    try:
        text = extract_clean_text(url)
        evaluation = evaluate_text(text)
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/score", dependencies=[Depends(JWTBearer())])
async def score_portfolio(request: PortfolioAnalysisRequest):
    """
    Compute dynamic scores for the portfolio based on extracted text.
    Returns scores for:
      - Design
      - Technical Depth
      - Impact
      - Clarity
    """
    try:
        text = extract_clean_text(request.url)
        evaluation = evaluate_text(text)
        scores = compute_dynamic_scores(text, evaluation)
        return scores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enhance", dependencies=[Depends(JWTBearer())])
async def enhance_portfolio(request: PortfolioAnalysisRequest):
    """
    Provide automated enhancement suggestions for the portfolio.
    Suggestions cover SEO optimization, AI-generated descriptions, and resume integration.
    """
    try:
        text = extract_clean_text(request.url)
        suggestions = generate_enhancement_suggestions(text)
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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