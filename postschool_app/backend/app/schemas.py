from pydantic import BaseModel, EmailStr


# ---- auth ----
class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# ---- catalog ----
class CityOut(BaseModel):
    name: str
    description: str
    population: str
    climate: str
    student_life: str


class UniversityOut(BaseModel):
    slug: str
    short_name: str
    full_name: str
    city: str
    tuition_month: int
    military_dept: bool
    internal_exams: bool
    program_count: int
    min_threshold: int


class ProgramOut(BaseModel):
    id: int
    university_slug: str
    name: str
    code: str
    threshold: int
    subjects: list[str]


class OlympiadOut(BaseModel):
    title: str
    meta: str
    bonus: str


# ---- profile ----
class Bonuses(BaseModel):
    gto: bool = False
    oly: bool = False
    vol: bool = False


class ProfileIn(BaseModel):
    scores: dict[str, int] = {}
    bonuses: Bonuses = Bonuses()


class ProfileOut(BaseModel):
    scores: dict[str, int]
    bonuses: Bonuses


# ---- matching ----
class MatchIn(BaseModel):
    scores: dict[str, int] = {}
    bonuses: Bonuses = Bonuses()


class MatchItem(BaseModel):
    program_id: int
    name: str
    university_slug: str
    code: str
    your_score: int
    threshold: int
    status: str


# ---- favorites ----
class FavoriteOut(BaseModel):
    program_id: int
