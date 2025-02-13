def compute_portfolio_level(scores: dict) -> dict:
    """
    Compute the portfolio level based on dynamic scores.
    An aggregate score (average of design, technical_depth, impact, and clarity) is computed.
    Levels:
      - Beginner: aggregate < 40
      - Intermediate: 40 <= aggregate < 70
      - Expert: aggregate >= 70
    """
    aggregate = (
        scores.get("design", 0) +
        scores.get("technical_depth", 0) +
        scores.get("impact", 0) +
        scores.get("clarity", 0)
    ) / 4

    if aggregate < 40:
        level = "Beginner"
    elif aggregate < 70:
        level = "Intermediate"
    else:
        level = "Expert"

    return {"level": level, "aggregate_score": aggregate}


def get_career_recommendations(scores: dict) -> dict:
    """
    Provide career insights and job recommendations based on dynamic scores.
    For example:
      - High technical depth → Backend/Full Stack Developer roles.
      - High design score → UI/UX Designer or Frontend Developer roles.
      - High impact → Leadership roles.
      - High clarity → Technical Writing or Developer Evangelist roles.
    If none of these are high, a default recommendation is provided.
    """
    recommendations = []

    if scores.get("technical_depth", 0) >= 70:
        recommendations.extend(["Backend Developer", "Full Stack Developer"])
    if scores.get("design", 0) >= 70:
        recommendations.extend(["UI/UX Designer", "Frontend Developer"])
    if scores.get("impact", 0) >= 70:
        recommendations.append("Project Manager")
    if scores.get("clarity", 0) >= 70:
        recommendations.append("Technical Writer")

    if not recommendations:
        recommendations.append("Software Engineer")

    # Remove duplicates if any
    recommendations = list(set(recommendations))
    return {"recommendations": recommendations}
