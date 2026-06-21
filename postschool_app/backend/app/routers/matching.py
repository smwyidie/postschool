from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..security import get_current_user
from ..matching import compute_matches

router = APIRouter(prefix="/api/match", tags=["matching"])


@router.post("", response_model=list[schemas.MatchItem])
def match_preview(data: schemas.MatchIn, db: Session = Depends(get_db)):
    """Compute statuses for arbitrary scores (used for guests and live recalculation)."""
    return compute_matches(db, data.scores, data.bonuses.model_dump())


@router.get("", response_model=list[schemas.MatchItem])
def match_current_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Compute statuses from the saved profile of the authenticated user."""
    profile = current_user.profile
    scores = {r.subject.key: r.score for r in profile.results} if profile else {}
    bonuses = {
        "gto": profile.gto_gold if profile else False,
        "oly": profile.olympiad_winner if profile else False,
        "vol": profile.volunteer if profile else False,
    }
    return compute_matches(db, scores, bonuses)
