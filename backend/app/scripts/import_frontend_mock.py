import json
import subprocess
from datetime import datetime
from pathlib import Path

from sqlalchemy import text

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.entities import Company, ContentColumn, Course, EliteProgram, JobPosting, Review, SalaryReport, User
from app.scripts.init_db import ensure_schema_exists


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "frontend_mock.json"


def export_json() -> None:
    script = Path(__file__).with_name("export_frontend_mock.mjs")
    subprocess.run(["node", str(script)], check=True)


def parse_created_at(value: str):
    if not value:
        return datetime.utcnow()
    return datetime.fromisoformat(value)


def reset_schema() -> None:
    ensure_schema_exists()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def company_from_snapshot(snapshot: dict, fallback_industry: str = "") -> Company:
    return Company(
        id=snapshot["id"],
        name=snapshot["name"],
        logo_text=snapshot.get("logo_text", ""),
        logo_color=snapshot.get("logo_color", "#1E6EFF"),
        industry=fallback_industry or "other",
        intro="",
    )


def import_data() -> None:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    reset_schema()
    with SessionLocal() as db:
        companies: dict[int, Company] = {}
        for job in data["jobPostings"]:
            snapshot = job["company"]
            company = companies.get(snapshot["id"]) or company_from_snapshot(snapshot, job.get("industry", ""))
            company.industry = job.get("industry", company.industry)
            companies[company.id] = company
        for report in data["salaryReports"]:
            snapshot = report["company"]
            company = companies.get(snapshot["id"]) or company_from_snapshot(snapshot, report.get("industry", ""))
            company.industry = company.industry or report.get("industry", "other")
            companies[company.id] = company
        db.add_all(companies.values())
        db.flush()

        for account in data["adminAccounts"]:
            db.add(User(
                id=account["id"],
                username=account["username"],
                password_hash=hash_password(account["password"]),
                nickname=account["nickname"],
                role=account["role"],
                company_id=account.get("company_id"),
            ))
        db.add(User(id=1003, username="cheater", password_hash=hash_password("cheater"), nickname="作弊用户", role="user", is_blacklisted=True))
        db.add(User(id=1004, username="crawler", password_hash=hash_password("crawler"), nickname="爬虫用户", role="user", is_crawler=True))
        db.flush()

        for job in data["jobPostings"]:
            db.add(JobPosting(
                id=job["id"],
                company_id=job["company"]["id"],
                title=job["title"],
                batch=job.get("batch", ""),
                recruitment_type=job.get("recruitment_type", "campus"),
                industry=job.get("industry", ""),
                cities=job.get("cities", []),
                deliver_start=job.get("deliver_start", ""),
                deliver_end=job.get("deliver_end", ""),
                graduation_range=job.get("graduation_range", ""),
                apply_url=job.get("apply_url", ""),
                internal_code=job.get("internal_code", ""),
                benefits=job.get("benefits", []),
                positions=job.get("positions", []),
                tags=job.get("tags", []),
                intro_html=job.get("intro_html", ""),
                views=job.get("views", 0),
                interest_count=job.get("interest_count", 0),
                is_official=job.get("is_official", False),
                owner_user_id=1002 if job["company"]["id"] == 1 else 1,
                created_at=parse_created_at(job.get("created_at")),
                updated_at=parse_created_at(job.get("created_at")),
            ))

        for course in data["courses"]:
            db.add(Course(
                id=course["id"],
                title=course["title"],
                cover_color=course.get("cover_color", "#1E6EFF"),
                category=course.get("category", ""),
                price=course.get("price", 0),
                intro=course.get("intro", ""),
            ))

        for column in data["columns"]:
            db.add(ContentColumn(
                id=column["id"],
                source_id=column["id"],
                name=column["name"],
                cover_color=column.get("cover_color", "#1E6EFF"),
                scope="job",
                total=column.get("total", 0),
                views=column.get("views", 0),
                desc=column.get("desc", ""),
                filter_rule=column.get("filter_rule", {}),
            ))
        for column in data["salaryColumns"]:
            db.add(ContentColumn(
                id=1000 + column["id"],
                source_id=column["id"],
                name=column["name"],
                cover_color=column.get("cover_color", "#1E6EFF"),
                scope="salary",
                total=column.get("total", 0),
                views=column.get("views", 0),
                desc=column.get("desc", ""),
                filter_rule=column.get("filter_rule", {}),
            ))

        for item in data["reviewRank"]:
            db.add(Review(
                id=item["rank"],
                company_id=item["company"]["id"],
                score=item["score"],
                review_count=item.get("reviews", 1),
                content=item.get("latest", ""),
            ))

        for program in data["elitePrograms"]:
            company = next((c for c in companies.values() if c.name == program["company"]["name"]), None)
            db.add(EliteProgram(
                id=program["id"],
                company_id=company.id if company else None,
                company_snapshot_data=program["company"],
                name=program["name"],
                salary_range=program.get("salary_range", ""),
                description=program.get("description", ""),
                apply_url=program.get("apply_url", ""),
            ))

        for report in data["salaryReports"]:
            db.add(SalaryReport(
                id=report["id"],
                company_id=report["company"]["id"],
                position=report.get("position", ""),
                city=report.get("city", ""),
                salary_desc=report.get("salary_desc", ""),
                annual_min=report.get("annual_min", 0),
                annual_max=report.get("annual_max", 0),
                recruitment_type=report.get("recruitment_type", "campus"),
                education=report.get("education", ""),
                edu_tags=report.get("edu_tags", []),
                industry=report.get("industry", ""),
                tags=report.get("tags", []),
                remark=report.get("remark", ""),
                credibility=report.get("credibility", 60),
                views=report.get("views", 0),
                likes=report.get("likes", 0),
                author_user_id=1001,
                created_at=parse_created_at(report.get("created_at")),
                updated_at=parse_created_at(report.get("created_at")),
            ))

        db.commit()
        for table in [
            "companies", "users", "job_postings", "courses", "content_columns",
            "reviews", "elite_programs", "salary_reports", "salary_comments",
        ]:
            db.execute(text(f"select setval(pg_get_serial_sequence('offershow.{table}', 'id'), coalesce(max(id), 1)) from offershow.{table}"))
        db.commit()


def main() -> None:
    export_json()
    import_data()
    print("frontend mock data imported")


if __name__ == "__main__":
    main()

