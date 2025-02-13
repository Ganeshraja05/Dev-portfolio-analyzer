def compute_dynamic_scores(text: str, evaluation: dict) -> dict:
    """
    Compute dynamic scores for the portfolio based on the text content and AI evaluation.
    
    Parameters:
        text (str): The extracted text from the portfolio.
        evaluation (dict): Dictionary with evaluation metrics (e.g., sentiment and readability).
        
    Returns:
        dict: Scores for design, technical depth, impact, and clarity on a scale of 0 to 100.
    """
    # Impact: Normalize the sentiment compound score (range -1 to 1) to a 0–100 scale.
    compound = evaluation.get("sentiment", {}).get("compound", 0)
    impact = int((compound + 1) * 50)  # e.g., compound=0 => 50, compound=1 => 100, compound=-1 => 0

    # Clarity: Use the readability score directly (Flesch Reading Ease typically between 0 and 100)
    clarity = int(evaluation.get("readability", 50))
    clarity = min(max(clarity, 0), 100)  # Ensure it is between 0 and 100

    # Design: Count occurrences of design-related keywords and calculate a score.
    design_keywords = ["design", "ui", "ux", "interface", "layout"]
    design_count = sum(text.lower().count(word) for word in design_keywords)
    design_score = min(100, design_count * 10)  # Each occurrence adds 10 points (capped at 100)

    # Technical Depth: Count occurrences of technical keywords and calculate a score.
    tech_keywords = [
        "python", "javascript", "react", "node", "api",
        "database", "fastapi", "mongodb", "framework", "development"
    ]
    tech_count = sum(text.lower().count(word) for word in tech_keywords)
    technical_depth = min(100, tech_count * 10)  # Each occurrence adds 10 points (capped at 100)

    return {
        "design": design_score,
        "technical_depth": technical_depth,
        "impact": impact,
        "clarity": clarity
    }
