// 静态种子数据，覆盖文档二需求中的所有展示型字段。
export const industries = [
  { code: 'all', name: '全部' },
  { code: 'internet', name: 'IT/互联网' },
  { code: 'game', name: '游戏' },
  { code: 'hardware', name: '硬件/半导体' },
  { code: 'auto', name: '汽车/自动驾驶' },
  { code: 'machine', name: '机械/制造业' },
  { code: 'finance', name: '金融行业' },
  { code: 'consume', name: '消费生活' },
  { code: 'health', name: '医疗健康' },
  { code: 'gov', name: '政府/事业单位' },
  { code: 'soe', name: '国企央企' },
  { code: 'media', name: '广告传媒' },
  { code: 'realestate', name: '建筑/房地产' },
  { code: 'energy', name: '材料/能源/化工' },
  { code: 'logistics', name: '物流/交通运输' },
  { code: 'other', name: '其他行业' },
]

export const cities = [
  '北京','上海','广州','深圳','杭州','成都','武汉','苏州','南京','天津',
  '郑州','合肥','长沙','济南','太原','青岛','石家庄','西安','重庆','厦门',
  '宁波','福州','昆明','南昌','佛山','东莞',
]

export const recruitmentTypes = [
  { value: 'campus', label: '校招' },
  { value: 'intern', label: '实习' },
  { value: 'social', label: '社招' },
]

export const batches = [
  '不限','校招','实习','日常实习','暑期实习',
  '春招提前批','春招正式批','春招补录',
  '秋招提前批','秋招正式批','秋招补录',
  '校招提前批','校招正式批','校招补录',
]

const benefitPool = ['年度奖金','带薪年假','五险一金','节日福利','年度免费体检','补充医疗','弹性工作','免费三餐']

const companyTpl = [
  { id: 1, name: '极兔速递', logo_text: '极兔', logo_color: '#FF5C5C', industry: 'logistics',
    intro: 'J&T极兔速递是一家全球综合物流服务运营商，业务在全球规模最大及增长最快的中国和东南亚市场处于领先地位。公司创立于2015年，快递网络覆盖印尼、马来西亚、泰国、越南、菲律宾、柬埔寨、新加坡等13个国家。' },
  { id: 2, name: '庭宇科技', logo_text: '庭宇', logo_color: '#FFB347', industry: 'internet',
    intro: '庭宇科技是国内领先的互联网解决方案提供商，提供云原生、AI 驱动的企业级产品。' },
  { id: 3, name: '阿里巴巴淘宝闪购', logo_text: '淘宝', logo_color: '#FF7A00', industry: 'internet',
    intro: '阿里巴巴淘宝闪购，致力于打造下一代即时电商体验。' },
  { id: 4, name: '鼎捷数智', logo_text: 'Digiwin', logo_color: '#0099E5', industry: 'internet',
    intro: '鼎捷数智，企业数字化转型领导品牌。' },
  { id: 5, name: '本源量子', logo_text: '本源', logo_color: '#3858E9', industry: 'hardware',
    intro: '本源量子是国内首家量子计算公司，拥有完整自研技术栈。' },
  { id: 6, name: '字节跳动', logo_text: '字节', logo_color: '#000000', industry: 'internet',
    intro: '字节跳动是一家全球化的科技公司，旗下产品覆盖信息流、视频、教育等多个领域。' },
  { id: 7, name: '腾讯', logo_text: 'T', logo_color: '#0099FF', industry: 'internet',
    intro: '腾讯，连接一切，用户为本，科技向善。' },
  { id: 8, name: '百度', logo_text: '百度', logo_color: '#3385FF', industry: 'internet',
    intro: '百度，中国领先的搜索与人工智能公司。' },
  { id: 9, name: '京东', logo_text: '京东', logo_color: '#E1251B', industry: 'internet',
    intro: '京东，国内领先自营电商集团。' },
  { id: 10, name: '美团', logo_text: '美团', logo_color: '#FFD100', industry: 'consume',
    intro: '美团，帮大家吃得更好，生活更好。' },
  { id: 11, name: '中国三星', logo_text: 'Samsung', logo_color: '#1428A0', industry: 'hardware',
    intro: '中国三星，全球科技领军企业。' },
  { id: 12, name: '微软中国', logo_text: 'MS', logo_color: '#00A4EF', industry: 'internet',
    intro: 'Microsoft, empower every person and every organization.' },
  { id: 13, name: '宁德时代', logo_text: 'CATL', logo_color: '#0E5C36', industry: 'energy',
    intro: '宁德时代，全球领先的动力电池系统提供商。' },
  { id: 14, name: '小米', logo_text: 'MI', logo_color: '#FF6700', industry: 'hardware',
    intro: '小米，让每个人都享受科技的乐趣。' },
  { id: 15, name: '华为', logo_text: '华为', logo_color: '#C7000B', industry: 'hardware',
    intro: '华为，构建万物互联的智能世界。' },
  // 游戏行业
  { id: 16, name: '米哈游', logo_text: '米游', logo_color: '#23B7E5', industry: 'game',
    intro: '米哈游 miHoYo，技术宅拯救世界，《原神》《崩坏：星穹铁道》开发商。' },
  { id: 17, name: '网易游戏', logo_text: '网易', logo_color: '#C7000B', industry: 'game',
    intro: '网易游戏，国内顶级 MMO / 二次元 / 竞技手游研发与发行平台。' },
  { id: 18, name: '腾讯游戏', logo_text: '腾游', logo_color: '#0099FF', industry: 'game',
    intro: '腾讯互娱（IEG），全球最大游戏发行商之一，旗下《王者荣耀》《和平精英》等。' },
  { id: 19, name: '莉莉丝', logo_text: '莉莉丝', logo_color: '#FF4D6D', industry: 'game',
    intro: '莉莉丝游戏，《剑与远征》《万国觉醒》开发商，专注海外发行。' },
  { id: 20, name: '完美世界', logo_text: '完美', logo_color: '#7C3AED', industry: 'game',
    intro: '完美世界，老牌 MMORPG 与影视集团。' },
  { id: 21, name: '叠纸游戏', logo_text: '叠纸', logo_color: '#F472B6', industry: 'game',
    intro: '叠纸游戏，《恋与制作人》《暖暖系列》开发商。' },
  { id: 22, name: '鹰角网络', logo_text: '鹰角', logo_color: '#1F2937', industry: 'game',
    intro: '鹰角网络，《明日方舟》《来自星尘》开发商。' },
  { id: 23, name: '朝夕光年', logo_text: '朝夕', logo_color: '#000000', industry: 'game',
    intro: '朝夕光年，字节跳动旗下游戏发行品牌。' },
  // 金融
  { id: 24, name: '招商银行', logo_text: '招行', logo_color: '#C8102E', industry: 'finance',
    intro: '招商银行，零售之王。' },
  { id: 25, name: '中信证券', logo_text: '中信', logo_color: '#B21E2A', industry: 'finance',
    intro: '中信证券，国内顶级综合券商。' },
  // 汽车
  { id: 26, name: '比亚迪', logo_text: 'BYD', logo_color: '#0E7C45', industry: 'auto',
    intro: '比亚迪，新能源汽车与电池领导者。' },
  { id: 27, name: '理想汽车', logo_text: '理想', logo_color: '#0F1A2A', industry: 'auto',
    intro: '理想汽车，家庭智能电动旗舰。' },
  // 消费
  { id: 28, name: '海底捞', logo_text: '海底', logo_color: '#E11D48', industry: 'consume',
    intro: '海底捞，全球知名餐饮品牌。' },
  // 国企
  { id: 29, name: '中国电网', logo_text: '电网', logo_color: '#16A34A', industry: 'soe',
    intro: '国家电网，国家能源命脉。' },
  // 医疗
  { id: 30, name: '迈瑞医疗', logo_text: '迈瑞', logo_color: '#0EA5E9', industry: 'health',
    intro: '迈瑞医疗，医疗器械龙头。' },
]

function makeJobs() {
  const tplBatches = ['春招正式批','秋招正式批','暑期实习','春招提前批','社会招聘','社招正式批']
  const list = []
  let id = 1000
  for (const c of companyTpl) {
    for (let k = 0; k < 4; k++) {
      const batch = tplBatches[(id + k) % tplBatches.length]
      const rt = batch.includes('实习') ? 'intern' : (batch.includes('社') ? 'social' : 'campus')
      list.push({
        id: id++,
        company: { id: c.id, name: c.name, logo_text: c.logo_text, logo_color: c.logo_color },
        title: `${c.name}2026${batch}招聘启动`,
        batch,
        recruitment_type: rt,
        industry: c.industry,
        cities: ['北京','上海','广州','深圳','杭州'].slice(0, ((id+k)%4)+1),
        deliver_start: '2026-04-02',
        deliver_end: '2026-07-31',
        graduation_range: '2025-09-01 至 2026-07-31 应届毕业生',
        apply_url: 'https://example.jobs/apply/' + (id+k),
        internal_code: '9FB' + (1000 + (id+k)).toString(),
        benefits: benefitPool.slice(0, ((id+k)%5)+3),
        views: 500 + ((id*13+k*97) % 4000),
        interest_count: 50 + ((id*7+k*11) % 600),
        is_official: ((id+k)%2===0),
        positions: [
          { id: 1, name: '物流营运类', description: '负责区域物流网络的规划、运营与优化。' },
          { id: 2, name: '产品研发类', description: '负责系统架构设计与核心功能开发。' },
          { id: 3, name: '财务审计类', description: '财务报表、预算与内部审计。' },
          { id: 4, name: '小语种类(西/葡/阿/法/德)', description: '负责对接海外业务的语言支持。' },
          { id: 5, name: '综合职能类', description: 'HR、行政、市场等综合岗位。' },
          { id: 6, name: '海外地区岗', description: '驻外岗位，长期外派。' },
          { id: 7, name: '实习生', description: '暑期 / 日常实习生。' },
        ],
        intro_html: `<p><b>【招聘对象】</b></p><p>面向2026届应届毕业生，毕业于2025年9月1日-2026年8月31日。</p><p><b>【专属福利】</b></p><ul><li>年度奖金</li><li>带薪年假</li><li>五险一金</li><li>节日福利</li><li>年度免费体检</li></ul>`,
        created_at: '2026-04-' + String(2 + ((id+k)%25)).padStart(2,'0'),
      })
    }
  }
  return list
}

export const jobPostings = makeJobs()

export const dailyBriefs = jobPostings.slice(0, 30)

export const courses = [
  { id: 1, title: '27/28届校招求职陪跑', cover_color: '#FF6F61', category: '求职陪跑', price: 12980, intro: '简历+面试+内推全套陪跑' },
  { id: 2, title: '1v1私教 简历精修-校招版', cover_color: '#1E6EFF', category: '求职必备', price: 599, intro: '行业 HR 1v1 简历指导' },
  { id: 3, title: '1v1私教 简历精修-社招版', cover_color: '#FFB347', category: '求职必备', price: 799, intro: '社招方向简历优化' },
  { id: 4, title: '1v1私教 大厂面试官模拟面试', cover_color: '#16A34A', category: '行业好课', price: 14980, intro: '前大厂面试官真题模拟' },
  { id: 5, title: 'AI 面试通关训练营', cover_color: '#A78BFA', category: '行业好课', price: 1299, intro: '聚焦 AI 行业的面试题库' },
  { id: 6, title: '量化金融求职训练营', cover_color: '#0F766E', category: '行业好课', price: 1899, intro: '量化方向针对性训练' },
]

export const columns = [
  { id: 1, name: '春招早鸟专场', cover_color: '#FF8B3D', scope: 'job', total: 138, views: 16320 },
  { id: 2, name: '国企央企优选', cover_color: '#C7000B', scope: 'job', total: 92, views: 19850 },
  { id: 3, name: '互联网优选', cover_color: '#1E6EFF', scope: 'job', total: 215, views: 33001 },
  { id: 4, name: '寒暑假实习专场', cover_color: '#16A34A', scope: 'job', total: 76, views: 8923 },
  { id: 5, name: '半导体专场', cover_color: '#0F766E', scope: 'job', total: 41, views: 6204 },
  { id: 6, name: '优质外企', cover_color: '#0099E5', scope: 'job', total: 58, views: 9120 },
  { id: 7, name: '金融科技专场', cover_color: '#3858E9', scope: 'job', total: 472, views: 66325 },
  { id: 8, name: 'AI 专场', cover_color: '#A78BFA', scope: 'job', total: 132, views: 21899 },
]

export const reviewRank = companyTpl.map((c, i) => ({
  rank: i + 1,
  company: { id: c.id, name: c.name, logo_text: c.logo_text, logo_color: c.logo_color },
  score: +(7.5 + (Math.sin(i)*1.5)).toFixed(1),
  reviews: 30 + (i*17 % 200),
  latest: ['团队氛围不错，导师指导用心。','加班较多但学到很多。','薪资略低但成长快。','发展前景不错，强烈推荐。'][i%4],
}))

export const elitePrograms = [
  { id: 1, company: { name: '阿里巴巴', logo_text: '阿里', logo_color: '#FF7A00' }, name: 'A Star 顶尖人才计划', salary_range: '100~200万/年', description: '阿里星 A Star 是阿里集团面向全球顶尖博士的招聘计划，提供超高薪资与导师支持。', apply_url: 'https://campus.alibaba.com/' },
  { id: 2, company: { name: '京东', logo_text: '京东', logo_color: '#E1251B' }, name: 'TGT 顶尖青年技术天才', salary_range: '100~200万/年', description: '京东 TGT 计划，给顶尖技术人才一个无上限的舞台。', apply_url: 'https://campus.jd.com/' },
  { id: 3, company: { name: '腾讯', logo_text: 'T', logo_color: '#0099FF' }, name: '青云计划', salary_range: '80~160万/年', description: '腾讯青云计划，瞄准未来 5 年的核心技术骨干。', apply_url: 'https://join.qq.com/' },
  { id: 4, company: { name: '字节跳动', logo_text: '字节', logo_color: '#000' }, name: 'Top Seed', salary_range: '80~150万/年', description: '字节 Top Seed 计划，AI 与基础架构方向顶尖博士。', apply_url: 'https://job.bytedance.com/' },
]

function makeSalaryReports() {
  const list = []
  let id = 80000
  const positions = ['后端研发','前端研发','产品经理','算法工程师','数据分析','测试工程师','运维工程师','客户端开发','机器学习','量化研究','游戏策划','游戏美术','HRBP','技术支持']
  const eduOpts = ['本科','硕士','博士']
  const eduTagPool = ['985','211','海归','双一流']
  const tagsPool = ['#年终奖','#签字费','#工作作息','#团队氛围','#发展前景','#加班情况','#股票']
  const types = ['campus','intern','social']
  for (let i = 0; i < 120; i++) {
    const c = companyTpl[i % companyTpl.length]
    const p = positions[i % positions.length]
    const rt = types[i % types.length]
    const monthly = 8 + ((i*7) % 35)
    const months = 14 + (i % 4)
    const annualMax = +(monthly * months / 10).toFixed(2)
    const eduTags = eduTagPool.slice(0, (i % 3) + (i % 7 === 0 ? 2 : 1))
    list.push({
      id: id++,
      company: { id: c.id, name: c.name, logo_text: c.logo_text, logo_color: c.logo_color },
      position: p,
      city: cities[i % cities.length],
      salary_desc: `${monthly}k*${months}`,
      annual_min: +(annualMax * 0.85).toFixed(2),
      annual_max: annualMax,
      recruitment_type: rt,
      education: eduOpts[i % eduOpts.length],
      edu_tags: eduTags,
      industry: c.industry,
      tags: tagsPool.slice(0, (i % 4) + 1),
      remark: ['整体打包不错，签字费 5w。','作息 996，但年终给力。','base 给到行业 top 10%。','发展空间大，团队靠谱。','面试 4 轮，hr 面友好。','签字费 8w，期权按四年发放。'][i % 6],
      credibility: 60 + (i*7 % 40),
      views: 200 + (i*53 % 3000),
      likes: i % 80,
      created_at: '2026-04-' + String(1 + (i % 26)).padStart(2,'0'),
    })
  }
  const bytedance = companyTpl.find(c => c.name === '字节跳动')
  const byteTypes = ['campus', 'intern', 'social']
  const bytePositions = ['后端研发','前端研发','算法工程师','产品经理','客户端开发','数据分析']
  byteTypes.forEach((rt, typeIndex) => {
    bytePositions.forEach((p, k) => {
      const monthly = 22 + typeIndex * 4 + k
      const months = 14 + (k % 4)
      const annualMax = +(monthly * months / 10).toFixed(2)
      list.push({
        id: id++,
        company: { id: bytedance.id, name: bytedance.name, logo_text: bytedance.logo_text, logo_color: bytedance.logo_color },
        position: p,
        city: cities[(typeIndex * 6 + k) % cities.length],
        salary_desc: `${monthly}k*${months}`,
        annual_min: +(annualMax * 0.85).toFixed(2),
        annual_max: annualMax,
        recruitment_type: rt,
        education: eduOpts[(typeIndex + k) % eduOpts.length],
        edu_tags: eduTagPool.slice(0, ((typeIndex + k) % 3) + 1),
        industry: bytedance.industry,
        tags: tagsPool.slice(0, (k % 4) + 1),
        remark: ['校招 SP 批次，面试节奏较快。','技术面较深入，base 竞争力强。','业务线选择较多，成长空间大。'][typeIndex],
        credibility: 82 + ((typeIndex * 6 + k) % 15),
        views: 1800 + typeIndex * 300 + k * 77,
        likes: 30 + typeIndex * 10 + k,
        created_at: '2026-04-' + String(20 + k).padStart(2,'0'),
      })
    })
  })
  return list
}

export const salaryReports = makeSalaryReports()

// 每个专栏带 filter_rule，路由 /salary/columns/:id 详情页据此过滤 salaryReports
export const salaryColumns = [
  { id: 1, name: '985/211 党专场', cover_color: '#1E6EFF',
    desc: '名校学子的高薪 Offer 集合', filter_rule: { edu_tags_any: ['985','211'] } },
  { id: 2, name: '量化专场', cover_color: '#3858E9',
    desc: '量化研究员 / 量化开发岗位真实薪资', filter_rule: { position_any: ['量化研究','算法工程师'] } },
  { id: 3, name: '半导体专场', cover_color: '#0F766E',
    desc: '硬件 / 半导体行业薪资透明化', filter_rule: { industry: 'hardware' } },
  { id: 4, name: '40W 研发', cover_color: '#FF8B3D',
    desc: '年薪 40W+ 研发岗位汇总', filter_rule: { annual_min_gte: 40, position_any: ['后端研发','前端研发','算法工程师','机器学习','客户端开发','运维工程师'] } },
  { id: 5, name: 'HR 专场', cover_color: '#A78BFA',
    desc: 'HR / HRBP / 招聘岗薪资', filter_rule: { position_any: ['HRBP','技术支持'] } },
  { id: 6, name: '目标年薪 20W', cover_color: '#16A34A',
    desc: '应届毕业生年薪 20W 起步', filter_rule: { annual_min_lte: 25 } },
  { id: 7, name: '目标年薪 100W+', cover_color: '#C7000B',
    desc: '顶级人才与 SSP Offer', filter_rule: { annual_min_gte: 80 } },
  { id: 8, name: '外企/大厂入门', cover_color: '#0099E5',
    desc: '微软、字节、腾讯等外企大厂入门 Offer', filter_rule: { company_id_any: [6,7,8,12] } },
  { id: 9, name: '游戏行业专场', cover_color: '#7C3AED',
    desc: '米哈游/网易/腾讯游戏等真实薪资', filter_rule: { industry: 'game' } },
  { id: 10, name: '金融科技专场', cover_color: '#0F1A2A',
    desc: '银行 / 券商 / 量化机构', filter_rule: { industry: 'finance' } },
]

export const salaryComments = []

export const adminAccounts = [
  { username: 'demo', password: 'demo', role: 'user', id: 1001, nickname: '演示用户' },
  { username: 'hr', password: 'hr', role: 'hr', id: 1002, nickname: 'HR 演示账号', company_id: 1 },
  { username: 'admin', password: 'admin', role: 'admin', id: 1, nickname: '管理员' },
]
