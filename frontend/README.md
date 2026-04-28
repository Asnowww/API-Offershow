# OfferShow Frontend (H5)

Vue 3 + Vant 4 + Vite 移动端 H5。本目录是《Offer Show 微信公众号后台系统》的前端，对应文档二需求与文档三系统设计。

## 启动

```bash
cd frontend
npm install     # 已执行
npm run dev     # 启动开发服务，访问 http://localhost:5173
```

打开浏览器后建议切到手机模拟视图（375 宽）。

## 演示账号

| 账号 | 密码 | 角色 |
| --- | --- | --- |
| demo | demo | 普通用户 |
| hr | hr | HR（可访问 /hr 后台） |
| admin | admin | 管理员 |

## 模块对照

| 路由 | 文档二章节 |
| --- | --- |
| `/jobs` 找名企首页 | §3.1 招聘信息首页 + §3.2/3.3/3.4 筛选 |
| `/jobs/:id` 招聘详情 | §3.5 招聘详情（4 Tab） |
| `/daily-brief` | §3.6 求职早报 |
| `/courses` | §3.7 求职好课 |
| `/columns`、`/columns/:id` | §3.8 求职专栏 |
| `/refer` | §3.9 内推集合 |
| `/review-rank` | §3.10 实习点评榜 |
| `/elite` | §3.11 顶尖人才计划 |
| `/social` | §3.12 社招集合 |
| `/salary` 查薪资首页 | §4.1+4.2 薪资爆料/最新动态 |
| `/salary/rank` | §4.3 薪资人气榜单 |
| `/salary/campus` | §4.4 校招薪资查询 |
| `/salary/social` | §4.5 社招薪资查询 |
| `/salary/report` | §4.1 薪资爆料表单 |
| `/salary/:id` | §4.6 薪资详情 |
| `/me`、`/login`、`/hr` | 用户与 HR 后台 |

## 接入真实后端

`.env.development` 中：
- `VITE_USE_MOCK=true` → 走内存 mock（默认，无需后端）
- `VITE_USE_MOCK=false` → 走 `VITE_API_BASE`（默认 `/api/v1`），由 vite 代理至 `http://localhost:8000`
