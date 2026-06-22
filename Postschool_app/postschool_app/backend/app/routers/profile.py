from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..security import get_current_user

router = APIRouter(prefix="/api/profile", tags=["profile"])


def _ensure_profile(db: Session, user: models.User) -> models.Profile:
    if user.profile is None:
        user.profile = models.Profile()
        db.add(user)
        db.commit()
        db.refresh(user)
    return user.profile


@router.get("", response_model=schemas.ProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    profile = _ensure_profile(db, current_user)
    scores = {r.subject.key: r.score for r in profile.results}
    return schemas.ProfileOut(
        scores=scores,
        bonuses=schemas.Bonuses(
            gto=profile.gto_gold, oly=profile.olympiad_winner, vol=profile.volunteer
        ),
    )


@router.put("", response_model=schemas.ProfileOut)
def update_profile(
    data: schemas.ProfileIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    profile = _ensure_profile(db, current_user)
    profile.gto_gold = data.bonuses.gto
    profile.olympiad_winner = data.bonuses.oly
    profile.volunteer = data.bonuses.vol

    # rebuild exam results from the submitted scores
    db.query(models.ExamResult).filter(models.ExamResult.profile_id == profile.id).delete()
    subjects = {s.key: s.id for s in db.query(models.ExamSubject).all()}
    for key, score in data.scores.items():
        if key in subjects and score:
            db.add(models.ExamResult(profile_id=profile.id, subject_id=subjects[key], score=int(score)))
    db.commit()
    db.refresh(profile)

    scores = {r.subject.key: r.score for r in profile.results}
    return schemas.ProfileOut(
        scores=scores,
        bonuses=schemas.Bonuses(
            gto=profile.gto_gold, oly=profile.olympiad_winner, vol=profile.volunteer
        ),
    )
