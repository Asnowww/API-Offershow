import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.core.risk import risk_limiter


client = TestClient(app)
MOCK = json.loads((Path(__file__).resolve().parents[1] / "data" / "frontend_mock.json").read_text(encoding="utf-8"))


def unwrap(resp):
    assert resp.status_code < 500, resp.text
    body = resp.json()
    assert "code" in body
    return body


def login(username, password):
    body = unwrap(client.post("/api/v1/auth/login", json={"username": username, "password": password}))
    assert body["code"] == 0
    return body["data"]["token"]


def test_health():
    body = unwrap(client.get("/api/v1/health"))
    assert body["code"] == 0
    assert body["data"]["status"] == "ok"


def test_frontend_mock_counts_are_imported():
    jobs = unwrap(client.get("/api/v1/job-postings", params={"page_size": 1}))
    salaries = unwrap(client.get("/api/v1/salary-reports", params={"page_size": 1}))
    courses = unwrap(client.get("/api/v1/courses", params={"page_size": 1}))
    columns = unwrap(client.get("/api/v1/columns", params={"scope": "job", "page_size": 50}))
    salary_columns = unwrap(client.get("/api/v1/columns", params={"scope": "salary", "page_size": 50}))
    daily = unwrap(client.get("/api/v1/daily-briefs", params={"page_size": 50}))
    assert jobs["data"]["total"] == len(MOCK["jobPostings"])
    assert salaries["data"]["total"] == len(MOCK["salaryReports"])
    assert courses["data"]["total"] == len(MOCK["courses"])
    assert columns["data"]["total"] == len(MOCK["columns"])
    assert salary_columns["data"]["total"] == len(MOCK["salaryColumns"])
    assert daily["data"]["total"] == len(MOCK["dailyBriefs"])
    assert daily["data"]["items"][0]["id"] == MOCK["dailyBriefs"][0]["id"]
    assert daily["data"]["items"][0]["title"] == MOCK["dailyBriefs"][0]["title"]


def test_frontend_mock_sample_records_match():
    job_mock = MOCK["jobPostings"][0]
    job = unwrap(client.get(f"/api/v1/job-postings/{job_mock['id']}"))["data"]
    assert job["title"] == job_mock["title"]
    assert job["company"] == job_mock["company"]
    assert job["positions"] == job_mock["positions"]
    assert job["intro_html"] == job_mock["intro_html"]

    salary_mock = MOCK["salaryReports"][0]
    salary = unwrap(client.get(f"/api/v1/salary-reports/{salary_mock['id']}"))["data"]
    assert salary["company"] == salary_mock["company"]
    assert salary["position"] == salary_mock["position"]
    assert salary["salary_desc"] == salary_mock["salary_desc"]
    assert salary["edu_tags"] == salary_mock["edu_tags"]

    review = unwrap(client.get("/api/v1/companies:reviewRank", params={"tab": "new", "page_size": 1}))["data"]["items"][0]
    assert review["company"] == MOCK["reviewRank"][0]["company"]
    assert review["score"] == MOCK["reviewRank"][0]["score"]
    assert review["reviews"] == MOCK["reviewRank"][0]["reviews"]
    assert review["latest"] == MOCK["reviewRank"][0]["latest"]


def test_job_search_and_pagination():
    body = unwrap(client.get("/api/v1/job-postings", params={"q": "字节跳动", "page": 1, "page_size": 2}))
    assert body["code"] == 0
    assert body["data"]["page"] == 1
    assert body["data"]["page_size"] == 2
    assert body["data"]["total"] >= 1
    assert all("字节跳动" in item["company"]["name"] or "字节跳动" in item["title"] for item in body["data"]["items"])


def test_salary_search_rank_and_unified_search():
    salary = unwrap(client.get("/api/v1/salary-reports", params={"q": "字节跳动 后端", "page_size": 5}))
    assert salary["code"] == 0
    assert "items" in salary["data"]
    rank = unwrap(client.get("/api/v1/salary-reports:rank", params={"page_size": 3}))
    assert rank["code"] == 0
    assert len(rank["data"]["items"]) <= 3
    search = unwrap(client.get("/api/v1/search", params={"scope": "company", "q": "字节跳动"}))
    assert search["code"] == 0
    assert search["data"]["total"] >= 1


def test_auth_and_hr_batch_create():
    token = login("hr", "hr")
    body = unwrap(client.post(
        "/api/v1/job-postings:batchCreate",
        headers={"Authorization": f"Bearer {token}"},
        json={"items": [{
            "company_id": 1,
            "title": "极兔速递测试批量招聘",
            "batch": "测试批次",
            "recruitment_type": "campus",
            "cities": ["北京"],
        }]},
    ))
    assert body["code"] == 0
    assert body["data"]["success"] == 1
    created_id = body["data"]["ids"][0]
    admin = login("admin", "admin")
    deleted = unwrap(client.delete(f"/api/v1/job-postings/{created_id}", headers={"Authorization": f"Bearer {admin}"}))
    assert deleted["code"] == 0


def test_cheater_write_blocked_and_crawler_read_blocked():
    cheater = login("cheater", "cheater")
    blocked_write = client.post(
        "/api/v1/salary-reports",
        headers={"Authorization": f"Bearer {cheater}"},
        json={"company_id": 6, "position": "后端研发", "city": "北京", "salary_desc": "30k*15"},
    )
    assert blocked_write.status_code == 403
    assert blocked_write.json()["code"] == 40302

    crawler = login("crawler", "crawler")
    blocked_read = client.get("/api/v1/job-postings", headers={"Authorization": f"Bearer {crawler}"})
    assert blocked_read.status_code == 403
    assert blocked_read.json()["code"] == 40302


def test_risk_limiter_blocks_high_frequency_requests(monkeypatch):
    monkeypatch.setattr(risk_limiter, "redis", None)
    risk_limiter.local_hits.clear()
    try:
        for _ in range(240):
            resp = client.get("/api/v1/health")
            assert resp.status_code == 200

        blocked = client.get("/api/v1/health")
        assert blocked.status_code == 429
        body = blocked.json()
        assert body["code"] == 42901
        assert "message" in body
    finally:
        risk_limiter.local_hits.clear()
