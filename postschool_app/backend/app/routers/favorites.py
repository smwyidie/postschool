from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..security import get_current_user

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.get("", response_model=list[schemas.FavoriteOut])
def list_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return [schemas.FavoriteOut(program_id=f.program_id) for f in current_user.favorites]


@router.post("/{program_id}", response_model=schemas.FavoriteOut)
def add_favorite(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not db.query(models.Program).filter(models.Program.id == program_id).first():
        raise HTTPException(status_code=404, detail="Program not found")
    existing = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.program_id == program_id,
    ).first()
    if not existing:
        db.add(models.Favorite(user_id=current_user.id, program_id=program_id))
        db.commit()
    return schemas.FavoriteOut(program_id=program_id)


@router.delete("/{program_id}")
def remove_favorite(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.program_id == program_id,
    ).delete()
    db.commit()
    return {"detail": "removed"}
