from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime,
    ForeignKey, Table, UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base

# association table: required exam subjects for a program (many-to-many)
program_subjects = Table(
    "program_subjects", Base.metadata,
    Column("program_id", ForeignKey("programs.id", ondelete="CASCADE"), primary_key=True),
    Column("subject_id", ForeignKey("exam_subjects.id", ondelete="CASCADE"), primary_key=True),
)


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, default="")
    population = Column(String(40), default="")
    climate = Column(String(40), default="")
    student_life = Column(String(40), default="")
    universities = relationship("University", back_populates="city", cascade="all, delete-orphan")


class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True)
    slug = Column(String(40), unique=True, nullable=False)
    short_name = Column(String(80), nullable=False)
    full_name = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    tuition_month = Column(Integer, default=0)
    military_dept = Column(Boolean, default=False)
    internal_exams = Column(Boolean, default=False)
    city = relationship("City", back_populates="universities")
    programs = relationship("Program", back_populates="university", cascade="all, delete-orphan")


class ExamSubject(Base):
    __tablename__ = "exam_subjects"
    id = Column(Integer, primary_key=True)
    key = Column(String(10), unique=True, nullable=False)
    name = Column(String(60), nullable=False)


class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(160), nullable=False)
    code = Column(String(20), nullable=False)
    threshold = Column(Integer, nullable=False)
    university = relationship("University", back_populates="programs")
    subjects = relationship("ExamSubject", secondary=program_subjects)


class Olympiad(Base):
    __tablename__ = "olympiads"
    id = Column(Integer, primary_key=True)
    title = Column(String(160), nullable=False)
    meta = Column(String(200), default="")
    bonus = Column(String(60), default="")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="applicant")
    created_at = Column(DateTime, default=datetime.utcnow)
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    gto_gold = Column(Boolean, default=False)
    olympiad_winner = Column(Boolean, default=False)
    volunteer = Column(Boolean, default=False)
    user = relationship("User", back_populates="profile")
    results = relationship("ExamResult", back_populates="profile", cascade="all, delete-orphan")


class ExamResult(Base):
    __tablename__ = "exam_results"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("exam_subjects.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, default=0)
    profile = relationship("Profile", back_populates="results")
    subject = relationship("ExamSubject")


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("user_id", "program_id", name="uq_user_program"),)
    user = relationship("User", back_populates="favorites")
    program = relationship("Program")
