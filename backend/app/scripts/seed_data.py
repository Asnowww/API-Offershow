from app.core.security import hash_password
from app.models.entities import Company, ContentColumn, Course, EliteProgram, JobPosting, Review, SalaryReport, User


INDUSTRIES = [
    {"code": "all", "name": "全部"},
    {"code": "internet", "name": "IT/互联网"},
    {"code": "game", "name": "游戏"},
    {"code": "hardware", "name": "硬件/半导体"},
    {"code": "auto", "name": "汽车/自动驾驶"},
    {"code": "machine", "name": "机械/制造业"},
    {"code": "finance", "name": "金融行业"},
    {"code": "consume", "name": "消费生活"},
    {"code": "health", "name": "医疗健康"},
    {"code": "gov", "name": "政府/事业单位"},
    {"code": "soe", "name": "国企央企"},
    {"code": "media", "name": "广告传媒"},
    {"code": "realestate", "name": "建筑/房地产"},
    {"code": "energy", "name": "材料/能源/化工"},
    {"code": "logistics", "name": "物流/交通运输"},
    {"code": "other", "name": "其他行业"},
]

CITIES = [
    "北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "苏州", "南京", "天津",
    "郑州", "合肥", "长沙", "济南", "太原", "青岛", "石家庄", "西安", "重庆", "厦门",
    "宁波", "福州", "昆明", "南昌", "佛山", "东莞",
]

RECRUITMENT_TYPES = [
    {"value": "campus", "label": "校招"},
    {"value": "intern", "label": "实习"},
    {"value": "social", "label": "社招"},
]

BATCHES = [
    "不限", "校招", "实习", "日常实习", "暑期实习", "春招提前批", "春招正式批", "春招补录",
    "秋招提前批", "秋招正式批", "秋招补录", "校招提前批", "校招正式批", "校招补录",
]

COMPANIES = [
    (1, "极兔速递", "极兔", "#FF5C5C", "logistics", "J&T极兔速递是一家全球综合物流服务运营商。"),
    (2, "庭宇科技", "庭宇", "#FFB347", "internet", "国内领先的互联网解决方案提供商。"),
    (3, "阿里巴巴淘宝闪购", "淘宝", "#FF7A00", "internet", "打造下一代即时电商体验。"),
    (4, "鼎捷数智", "Digiwin", "#0099E5", "internet", "企业数字化转型领导品牌。"),
    (5, "本源量子", "本源", "#3858E9", "hardware", "国内量子计算公司。"),
    (6, "字节跳动", "字节", "#000000", "internet", "全球化科技公司。"),
    (7, "腾讯", "T", "#0099FF", "internet", "连接一切，用户为本，科技向善。"),
    (8, "百度", "百度", "#3385FF", "internet", "领先的搜索与人工智能公司。"),
    (9, "京东", "京东", "#E1251B", "internet", "国内领先自营电商集团。"),
    (10, "美团", "美团", "#FFD100", "consume", "帮大家吃得更好，生活更好。"),
    (11, "中国三星", "Samsung", "#1428A0", "hardware", "全球科技企业。"),
    (12, "微软中国", "MS", "#00A4EF", "internet", "Empower every person and every organization."),
    (13, "宁德时代", "CATL", "#0E5C36", "energy", "全球动力电池系统提供商。"),
    (14, "小米", "MI", "#FF6700", "hardware", "让每个人都享受科技的乐趣。"),
    (15, "华为", "华为", "#C7000B", "hardware", "构建万物互联的智能世界。"),
    (16, "米哈游", "米游", "#23B7E5", "game", "技术宅拯救世界。"),
    (17, "网易游戏", "网易", "#C7000B", "game", "国内顶级游戏研发与发行平台。"),
    (18, "腾讯游戏", "腾游", "#0099FF", "game", "全球大型游戏发行商。"),
    (19, "莉莉丝", "莉莉丝", "#FF4D6D", "game", "专注海外发行。"),
    (20, "完美世界", "完美", "#7C3AED", "game", "老牌 MMORPG 与影视集团。"),
    (21, "叠纸游戏", "叠纸", "#F472B6", "game", "暖暖系列开发商。"),
    (22, "鹰角网络", "鹰角", "#1F2937", "game", "明日方舟开发商。"),
    (23, "朝夕光年", "朝夕", "#000000", "game", "字节跳动旗下游戏品牌。"),
    (24, "招商银行", "招行", "#C8102E", "finance", "零售银行代表。"),
    (25, "中信证券", "中信", "#B21E2A", "finance", "综合券商。"),
    (26, "比亚迪", "BYD", "#0E7C45", "auto", "新能源汽车与电池领导者。"),
    (27, "理想汽车", "理想", "#0F1A2A", "auto", "家庭智能电动旗舰。"),
    (28, "海底捞", "海底", "#E11D48", "consume", "餐饮服务品牌。"),
    (29, "中国电网", "电网", "#16A34A", "soe", "国家能源基础设施。"),
    (30, "迈瑞医疗", "迈瑞", "#0EA5E9", "health", "医疗器械龙头。"),
]

BENEFITS = ["年度奖金", "带薪年假", "五险一金", "节日福利", "年度免费体检", "补充医疗", "弹性工作", "免费三餐"]
POSITIONS = [
    {"id": 1, "name": "物流营运类", "description": "负责区域物流网络规划与优化。"},
    {"id": 2, "name": "产品研发类", "description": "负责系统架构设计与核心功能开发。"},
    {"id": 3, "name": "财务审计类", "description": "财务报表、预算与内部审计。"},
    {"id": 4, "name": "算法工程师", "description": "机器学习、推荐、搜索与工程优化。"},
    {"id": 5, "name": "综合职能类", "description": "HR、行政、市场等综合岗位。"},
    {"id": 6, "name": "实习生", "description": "暑期 / 日常实习生。"},
]


def seed(db):
    if db.query(Company).count() == 0:
        for item in COMPANIES:
            db.add(Company(id=item[0], name=item[1], logo_text=item[2], logo_color=item[3], industry=item[4], intro=item[5]))
        db.flush()

    if db.query(User).count() == 0:
        users = [
            User(id=1, username="admin", password_hash=hash_password("admin"), nickname="管理员", role="admin"),
            User(id=1001, username="demo", password_hash=hash_password("demo"), nickname="演示用户", role="user"),
            User(id=1002, username="hr", password_hash=hash_password("hr"), nickname="HR 演示账号", role="hr", company_id=1),
            User(id=1003, username="cheater", password_hash=hash_password("cheater"), nickname="作弊用户", role="user", is_blacklisted=True),
            User(id=1004, username="crawler", password_hash=hash_password("crawler"), nickname="爬虫用户", role="user", is_crawler=True),
        ]
        db.add_all(users)
        db.flush()

    if db.query(JobPosting).count() == 0:
        batches = ["春招正式批", "秋招正式批", "暑期实习", "春招提前批", "社会招聘", "社招正式批"]
        job_id = 1000
        for c in db.query(Company).order_by(Company.id).all():
            for k in range(4):
                batch = batches[(job_id + k) % len(batches)]
                rt = "intern" if "实习" in batch else ("social" if "社" in batch else "campus")
                db.add(JobPosting(
                    id=job_id,
                    company_id=c.id,
                    title=f"{c.name}2026{batch}招聘启动",
                    batch=batch,
                    recruitment_type=rt,
                    industry=c.industry,
                    cities=["北京", "上海", "广州", "深圳", "杭州"][: ((job_id + k) % 4) + 1],
                    deliver_start="2026-04-02",
                    deliver_end="2026-07-31",
                    graduation_range="2025-09-01 至 2026-07-31 应届毕业生",
                    apply_url=f"https://example.jobs/apply/{job_id}",
                    internal_code=f"9FB{1000 + job_id}",
                    benefits=BENEFITS[: ((job_id + k) % 5) + 3],
                    positions=POSITIONS,
                    tags=["官方直聘", batch],
                    intro_html="<p><b>【招聘对象】</b></p><p>面向2026届应届毕业生。</p>",
                    views=500 + ((job_id * 13 + k * 97) % 4000),
                    interest_count=50 + ((job_id * 7 + k * 11) % 600),
                    is_official=(job_id + k) % 2 == 0,
                    owner_user_id=1002 if c.id == 1 else 1,
                ))
                job_id += 1

    if db.query(Course).count() == 0:
        courses = [
            ("27/28届校招求职陪跑", "#FF6F61", "求职陪跑", 12980, "简历+面试+内推全套陪跑"),
            ("1v1私教 简历精修-校招版", "#1E6EFF", "求职必备", 599, "行业 HR 1v1 简历指导"),
            ("1v1私教 简历精修-社招版", "#FFB347", "求职必备", 799, "社招方向简历优化"),
            ("1v1私教 大厂面试官模拟面试", "#16A34A", "行业好课", 14980, "前大厂面试官真题模拟"),
            ("AI 面试通关训练营", "#A78BFA", "行业好课", 1299, "聚焦 AI 行业的面试题库"),
            ("量化金融求职训练营", "#0F766E", "行业好课", 1899, "量化方向针对性训练"),
        ]
        for idx, item in enumerate(courses, 1):
            db.add(Course(id=idx, title=item[0], cover_color=item[1], category=item[2], price=item[3], intro=item[4]))

    if db.query(ContentColumn).count() == 0:
        job_columns = [
            ("春招早鸟专场", "#FF8B3D", 138, 16320, {}),
            ("国企央企优选", "#C7000B", 92, 19850, {"industry": "soe"}),
            ("互联网优选", "#1E6EFF", 215, 33001, {"industry": "internet"}),
            ("寒暑假实习专场", "#16A34A", 76, 8923, {"recruitment_type": "intern"}),
            ("半导体专场", "#0F766E", 41, 6204, {"industry": "hardware"}),
            ("优质外企", "#0099E5", 58, 9120, {}),
            ("金融科技专场", "#3858E9", 472, 66325, {"industry": "finance"}),
            ("AI 专场", "#A78BFA", 132, 21899, {}),
        ]
        for idx, item in enumerate(job_columns, 1):
            db.add(ContentColumn(id=idx, name=item[0], cover_color=item[1], scope="job", total=item[2], views=item[3], filter_rule=item[4]))
        salary_columns = [
            ("985/211 党专场", "#1E6EFF", "名校学子的高薪 Offer 集合", {"edu_tags_any": ["985", "211"]}),
            ("量化专场", "#3858E9", "量化研究员 / 量化开发岗位真实薪资", {"position_any": ["量化研究", "算法工程师"]}),
            ("半导体专场", "#0F766E", "硬件 / 半导体行业薪资透明化", {"industry": "hardware"}),
            ("40W 研发", "#FF8B3D", "年薪 40W+ 研发岗位汇总", {"annual_min_gte": 40}),
            ("HR 专场", "#A78BFA", "HR / HRBP / 招聘岗薪资", {"position_any": ["HRBP", "技术支持"]}),
            ("目标年薪 20W", "#16A34A", "应届毕业生年薪 20W 起步", {"annual_min_lte": 25}),
            ("目标年薪 100W+", "#C7000B", "顶级人才与 SSP Offer", {"annual_min_gte": 80}),
            ("外企/大厂入门", "#0099E5", "微软、字节、腾讯等外企大厂入门 Offer", {"company_id_any": [6, 7, 8, 12]}),
            ("游戏行业专场", "#7C3AED", "游戏行业真实薪资", {"industry": "game"}),
            ("金融科技专场", "#0F1A2A", "银行 / 券商 / 量化机构", {"industry": "finance"}),
        ]
        for offset, item in enumerate(salary_columns, 101):
            db.add(ContentColumn(id=offset, name=item[0], cover_color=item[1], scope="salary", desc=item[2], filter_rule=item[3]))

    if db.query(Review).count() == 0:
        comments = ["团队氛围不错，导师指导用心。", "加班较多但学到很多。", "薪资略低但成长快。", "发展前景不错，强烈推荐。"]
        for idx, c in enumerate(db.query(Company).order_by(Company.id).all(), 1):
            db.add(Review(company_id=c.id, score=round(7.5 + ((idx % 5) * 0.3), 1), content=comments[idx % len(comments)]))

    if db.query(EliteProgram).count() == 0:
        programs = [
            (3, "A Star 顶尖人才计划", "100~200万/年", "阿里星 A Star 面向全球顶尖博士。", "https://campus.alibaba.com/"),
            (9, "TGT 顶尖青年技术天才", "100~200万/年", "京东 TGT 计划。", "https://campus.jd.com/"),
            (7, "青云计划", "80~160万/年", "腾讯青云计划。", "https://join.qq.com/"),
            (6, "Top Seed", "80~150万/年", "字节 Top Seed 计划。", "https://job.bytedance.com/"),
        ]
        for idx, item in enumerate(programs, 1):
            db.add(EliteProgram(id=idx, company_id=item[0], name=item[1], salary_range=item[2], description=item[3], apply_url=item[4]))

    if db.query(SalaryReport).count() == 0:
        positions = ["后端研发", "前端研发", "产品经理", "算法工程师", "数据分析", "测试工程师", "运维工程师", "客户端开发", "机器学习", "量化研究", "游戏策划", "游戏美术", "HRBP", "技术支持"]
        educations = ["本科", "硕士", "博士"]
        tags_pool = ["#年终奖", "#签字费", "#工作作息", "#团队氛围", "#发展前景", "#加班情况", "#股票"]
        types = ["campus", "intern", "social"]
        companies = db.query(Company).order_by(Company.id).all()
        for i in range(120):
            c = companies[i % len(companies)]
            monthly = 8 + ((i * 7) % 35)
            months = 14 + (i % 4)
            annual_max = round(monthly * months / 10, 2)
            db.add(SalaryReport(
                id=80000 + i,
                company_id=c.id,
                position=positions[i % len(positions)],
                city=CITIES[i % len(CITIES)],
                salary_desc=f"{monthly}k*{months}",
                annual_min=round(annual_max * 0.85, 2),
                annual_max=annual_max,
                recruitment_type=types[i % len(types)],
                education=educations[i % len(educations)],
                edu_tags=["985", "211", "海归", "双一流"][: (i % 3) + 1],
                industry=c.industry,
                tags=tags_pool[: (i % 4) + 1],
                remark=["整体打包不错，签字费 5w。", "作息较强，但年终给力。", "base 给到行业前列。", "发展空间大，团队靠谱。"][i % 4],
                credibility=60 + (i * 7 % 40),
                views=200 + (i * 53 % 3000),
                likes=i % 80,
                author_user_id=1001,
            ))

    db.commit()
