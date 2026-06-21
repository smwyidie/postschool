from sqlalchemy.orm import Session

from . import models

CLOSE_MARGIN = 20
BONUS = {"gto": 2, "oly": 5, "vol": 2}


def bonus_total(bonuses: dict) -> int:
    return sum(pts for key, pts in BONUS.items() if bonuses.get(key))


def compute_matches(db: Session, scores: dict, bonuses: dict) -> list[dict]:
    extra = bonus_total(bonuses)
    result = []
    programs = db.query(models.Program).all()
    for p in programs:
        required = [s.key for s in p.subjects]
        your_score = sum(int(scores.get(k, 0) or 0) for k in required) + extra
        if your_score >= p.threshold:
            status = "pass"
        elif your_score >= p.threshold - CLOSE_MARGIN:
            status = "close"
        else:
            status = "far"
        result.append({
            "program_id": p.id,
            "name": p.name,
            "university_slug": p.university.slug,
            "code": p.code,
            "your_score": your_score,
            "threshold": p.threshold,
            "status": status,
        })
    return result
