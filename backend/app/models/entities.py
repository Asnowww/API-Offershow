from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    nickname: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(32), default="user", index=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("companies.id"), nullable=True)
    is_blacklisted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_crawler: Mapped[bool] = mapped_column(Boolean, default=False)


class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    logo_text: Mapped[str] = mapped_column(String(64), default="")
    logo_color: Mapped[str] = mapped_column(String(32), default="#1E6EFF")
    industry: Mapped[str] = mapped_column(String(64), index=True)
    intro: Mapped[str] = mapped_column(Text, default="")


class JobPosting(Base, TimestampMixin):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    batch: Mapped[str] = mapped_column(String(64), default="")
    recruitment_type: Mapped[str] = mapped_column(String(32), index=True)
    industry: Mapped[str] = mapped_column(String(64), index=True)
    cities: Mapped[list] = mapped_column(JSONB, default=list)
    deliver_start: Mapped[str] = mapped_column(String(32), default="")
    deliver_end: Mapped[str] = mapped_column(String(32), default="")
    graduation_range: Mapped[str] = mapped_column(String(128), default="")
    apply_url: Mapped[str] = mapped_column(String(512), default="")
    internal_code: Mapped[str] = mapped_column(String(64), default="")
    benefits: Mapped[list] = mapped_column(JSONB, default=list)
    positions: Mapped[list] = mapped_column(JSONB, default=list)
    tags: Mapped[list] = mapped_column(JSONB, default=list)
    intro_html: Mapped[str] = mapped_column(Text, default="")
    views: Mapped[int] = mapped_column(Integer, default=0)
    interest_count: Mapped[int] = mapped_column(Integer, default=0)
    is_official: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    company: Mapped[Company] = relationship("Company")


class SalaryReport(Base, TimestampMixin):
    __tablename__ = "salary_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), index=True)
    position: Mapped[str] = mapped_column(String(128), index=True)
    city: Mapped[str] = mapped_column(String(64), index=True)
    salary_desc: Mapped[str] = mapped_column(String(64))
    annual_min: Mapped[float] = mapped_column(Float, default=0)
    annual_max: Mapped[float] = mapped_column(Float, default=0)
    recruitment_type: Mapped[str] = mapped_column(String(32), index=True)
    education: Mapped[str] = mapped_column(String(64), default="")
    edu_tags: Mapped[list] = mapped_column(JSONB, default=list)
    industry: Mapped[str] = mapped_column(String(64), index=True)
    tags: Mapped[list] = mapped_column(JSONB, default=list)
    remark: Mapped[str] = mapped_column(Text, default="")
    credibility: Mapped[int] = mapped_column(Integer, default=60)
    views: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    author_user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    company: Mapped[Company] = relationship("Company")


class SalaryComment(Base, TimestampMixin):
    __tablename__ = "salary_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    salary_report_id: Mapped[int] = mapped_column(Integer, ForeignKey("salary_reports.id"), index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    content: Mapped[str] = mapped_column(Text)


class ContentColumn(Base, TimestampMixin):
    __tablename__ = "content_columns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_id: Mapped[int] = mapped_column(Integer, default=0, index=True)
    name: Mapped[str] = mapped_column(String(128), index=True)
    scope: Mapped[str] = mapped_column(String(32), index=True)
    cover_color: Mapped[str] = mapped_column(String(32), default="#1E6EFF")
    total: Mapped[int] = mapped_column(Integer, default=0)
    views: Mapped[int] = mapped_column(Integer, default=0)
    desc: Mapped[str] = mapped_column(Text, default="")
    filter_rule: Mapped[dict] = mapped_column(JSONB, default=dict)


class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    cover_color: Mapped[str] = mapped_column(String(32), default="#1E6EFF")
    category: Mapped[str] = mapped_column(String(64), index=True)
    price: Mapped[int] = mapped_column(Integer, default=0)
    intro: Mapped[str] = mapped_column(Text, default="")


class Review(Base, TimestampMixin):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    score: Mapped[float] = mapped_column(Float, default=8.0)
    review_count: Mapped[int] = mapped_column(Integer, default=1)
    content: Mapped[str] = mapped_column(Text, default="")

    company: Mapped[Company] = relationship("Company")


class EliteProgram(Base, TimestampMixin):
    __tablename__ = "elite_programs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("companies.id"), nullable=True)
    company_snapshot_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    name: Mapped[str] = mapped_column(String(128), index=True)
    salary_range: Mapped[str] = mapped_column(String(64), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    apply_url: Mapped[str] = mapped_column(String(512), default="")

    company: Mapped[Optional[Company]] = relationship("Company")
