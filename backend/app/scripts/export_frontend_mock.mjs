import { writeFileSync, mkdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const mockUrl = pathToFileURL(resolve(__dirname, '../../../frontend/src/api/mockData.js')).href
const mock = await import(mockUrl)

const data = {
  industries: mock.industries,
  cities: mock.cities,
  recruitmentTypes: mock.recruitmentTypes,
  batches: mock.batches,
  jobPostings: mock.jobPostings,
  dailyBriefs: mock.dailyBriefs,
  courses: mock.courses,
  columns: mock.columns,
  reviewRank: mock.reviewRank,
  elitePrograms: mock.elitePrograms,
  salaryReports: mock.salaryReports,
  salaryColumns: mock.salaryColumns,
  salaryComments: mock.salaryComments,
  adminAccounts: mock.adminAccounts,
}

const outDir = resolve(__dirname, '../../data')
mkdirSync(outDir, { recursive: true })
writeFileSync(resolve(outDir, 'frontend_mock.json'), JSON.stringify(data, null, 2), 'utf8')
console.log(`exported frontend mock data to ${resolve(outDir, 'frontend_mock.json')}`)
