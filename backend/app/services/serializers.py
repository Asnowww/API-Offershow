from typing import Optional

from app.models.entities import (
    Company,
    ContentColumn,
    Course,
    EliteProgram,
    JobPosting,
    Review,
    SalaryComment,
    SalaryReport,
    User,
)


def iso(dt):
    if not dt:
        return None
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
        return dt.date().isoformat()
    return dt.isoformat()


def user_out(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "role": user.role,
        "company_id": user.company_id,
    }


def company_out(company: Company) -> dict:
    return {
        "id": company.id,
        "name": company.name,
        "logo_text": company.logo_text,
        "logo_color": company.logo_color,
        "industry": company.industry,
        "intro": company.intro,
    }


def company_snapshot(company: Optional[Company]) -> Optional[dict]:
    if not company:
        return None
    return {
        "id": company.id,
        "name": company.name,
        "logo_text": company.logo_text,
        "logo_color": company.logo_color,
    }


def job_out(job: JobPosting) -> dict:
    return {
        "id": job.id,
        "company": company_snapshot(job.company),
        "company_id": job.company_id,
        "title": job.title,
        "batch": job.batch,
        "recruitment_type": job.recruitment_type,
        "industry": job.industry,
        "cities": job.cities or [],
        "deliver_start": job.deliver_start,
        "deliver_end": job.deliver_end,
        "graduation_range": job.graduation_range,
        "apply_url": job.apply_url,
        "internal_code": job.internal_code,
        "benefits": job.benefits or [],
        "positions": job.positions or [],
        "tags": job.tags or [],
        "intro_html": job.intro_html,
        "views": job.views,
        "interest_count": job.interest_count,
        "is_official": job.is_official,
        "created_at": iso(job.created_at),
        "updated_at": iso(job.updated_at),
    }


def salary_out(report: SalaryReport) -> dict:
    return {
        "id": report.id,
        "company": company_snapshot(report.company),
        "company_id": report.company_id,
        "position": report.position,
        "city": report.city,
        "salary_desc": report.salary_desc,
        "annual_min": report.annual_min,
        "annual_max": report.annual_max,
        "recruitment_type": report.recruitment_type,
        "education": report.education,
        "edu_tags": report.edu_tags or [],
        "industry": report.industry,
        "tags": report.tags or [],
        "remark": report.remark,
        "credibility": report.credibility,
        "views": report.views,
        "likes": report.likes,
        "created_at": iso(report.created_at),
        "updated_at": iso(report.updated_at),
    }


def column_out(column: ContentColumn) -> dict:
    return {
        "id": column.source_id or column.id,
        "name": column.name,
        "scope": column.scope,
        "cover_color": column.cover_color,
        "total": column.total,
        "views": column.views,
        "desc": column.desc,
        "filter_rule": column.filter_rule or {},
    }


def course_out(course: Course) -> dict:
    return {
        "id": course.id,
        "title": course.title,
        "cover_color": course.cover_color,
        "category": course.category,
        "price": course.price,
        "intro": course.intro,
    }


def review_rank_out(review: Review, rank: int) -> dict:
    return {
        "rank": rank,
        "company": company_snapshot(review.company),
        "score": review.score,
        "reviews": review.review_count,
        "latest": review.content,
    }


def elite_out(program: EliteProgram) -> dict:
    return {
        "id": program.id,
        "company": program.company_snapshot_data or company_snapshot(program.company),
        "name": program.name,
        "salary_range": program.salary_range,
        "description": program.description,
        "apply_url": program.apply_url,
    }


def comment_out(comment: SalaryComment) -> dict:
    return {
        "id": comment.id,
        "salary_report_id": comment.salary_report_id,
        "user_id": comment.user_id,
        "content": comment.content,
        "created_at": iso(comment.created_at),
    }
