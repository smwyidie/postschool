from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api", tags=["catalog"])


@router.get("/cities", response_model=list[schemas.CityOut])
def list_cities(db: Session = Depends(get_db)):
    return [
        schemas.CityOut(
            name=c.name, description=c.description, population=c.population,
            climate=c.climate, student_life=c.student_life,
        )
        for c in db.query(models.City).order_by(models.City.name).all()
    ]


@router.get("/universities", response_model=list[schemas.UniversityOut])
def list_universities(
    city: str | None = None,
    max_price: int | None = None,
    search: str | None = None,
    sort: str = "name",
    db: Session = Depends(get_db),
):
    query = db.query(models.University).join(models.City)
    if city:
        query = query.filter(models.City.name == city)
    if max_price is not None:
        query = query.filter(models.University.tuition_month <= max_price)
    if search:
        like = f"%{search.lower()}%"
        query = query.filter(
            (models.University.full_name.ilike(like)) | (models.University.short_name.ilike(like))
        )
    if sort == "price":
        query = query.order_by(models.University.tuition_month)
    else:
        query = query.order_by(models.University.short_name)

    out = []
    for u in query.all():
        thresholds = [p.threshold for p in u.programs]
        out.append(schemas.UniversityOut(
            slug=u.slug, short_name=u.short_name, full_name=u.full_name,
            city=u.city.name, tuition_month=u.tuition_month,
            military_dept=u.military_dept, internal_exams=u.internal_exams,
            program_count=len(u.programs),
            min_threshold=min(thresholds) if thresholds else 0,
        ))
    return out


@router.get("/programs", response_model=list[schemas.ProgramOut])
def list_programs(db: Session = Depends(get_db)):
    return [
        schemas.ProgramOut(
            id=p.id, university_slug=p.university.slug, name=p.name,
            code=p.code, threshold=p.threshold,
            subjects=[s.key for s in p.subjects],
        )
        for p in db.query(models.Program).all()
    ]


@router.get("/olympiads", response_model=list[schemas.OlympiadOut])
def list_olympiads(db: Session = Depends(get_db)):
    return [
        schemas.OlympiadOut(title=o.title, meta=o.meta, bonus=o.bonus)
        for o in db.query(models.Olympiad).all()
    ]
