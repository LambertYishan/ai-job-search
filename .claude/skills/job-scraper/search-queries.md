# Search Queries for Job Scraper

<!-- SETUP: Customized for Lambert Li / Yishan Li. -->

## Installed Portal CLIs

`/scrape` discovers every portal skill under `.agents/skills/*/SKILL.md` and runs its CLI first. For this setup:

- **linkedin-search**: primary US source.
- **freehire-search**: use where relevant for technical, data, ML, AI, and engineering-adjacent roles.
- **Danish portal demos**: leave disabled. The target market is the United States only.

The `site:` query templates below are WebSearch fallback queries for portals without a CLI, company career pages, or cases where a CLI fails.

## Search Strategy

Do not force the search into a single job-title category. Lambert's background crosses quantitative finance, risk modeling, data science, machine learning, and financial analytics. Search across functional buckets and rank jobs by actual responsibilities and requirements.

A role titled "Risk Analyst," "Quantitative Analyst," "Data Scientist," "Model Development Analyst," or "Financial Analyst" may be relevant if the underlying work involves Python, modeling, statistics, machine learning, financial risk, optimization, or quantitative research.

Avoid software-engineering roles that are primarily application or web development unless the work is meaningfully related to data, ML, AI, quantitative systems, or research infrastructure.

## Search Sites

Primary:
- **linkedin.com/jobs** - United States; onsite, hybrid, and remote.
- **FreeHire** - tech/data/ML/AI roles where relevant.
- **Company career pages** - banks, asset managers, hedge funds, fintech, insurance, financial-data/analytics companies, technology companies, and quantitative consulting teams.

Fallback Google queries:
- `site:boards.greenhouse.io`
- `site:jobs.lever.co`
- `site:myworkdayjobs.com`
- `site:careers.*`
- `site:linkedin.com/jobs`

## Query Categories

Use English queries only. Search nationally in the United States and include major quantitative/financial/technical markets: New York City, Boston, Chicago, Charlotte, Raleigh-Durham, Washington DC / Northern Virginia, Atlanta, Dallas, Austin, San Francisco Bay Area, and Seattle. Include remote roles.

### Priority 1: Quantitative Finance and Risk Modeling

Strongest fit: quantitative modeling, risk modeling, financial mathematics, CECL/ACL, prepayment modeling, credit risk, model development, and model validation.

```
site:linkedin.com/jobs "Quantitative Analyst" "United States" Python risk modeling
site:linkedin.com/jobs "Quantitative Finance Analyst" "United States" Python
site:linkedin.com/jobs "Quantitative Risk Analyst" "United States" Python SQL
site:linkedin.com/jobs "Risk Modeler" "United States" Python
site:linkedin.com/jobs "Model Development Analyst" "United States" credit risk Python
site:linkedin.com/jobs "Credit Risk Modeler" "United States" CECL Python
site:linkedin.com/jobs "Credit Risk Analyst" "United States" Python SQL modeling
site:linkedin.com/jobs "Model Risk Analyst" "United States" model validation Python
site:linkedin.com/jobs "Model Validation Analyst" "United States" risk modeling
```

### Priority 2: Financial Data Science and Analytics

Relevant when the work involves predictive modeling, machine learning, statistics, optimization, financial analytics, or investment/risk analytics.

```
site:linkedin.com/jobs "Data Scientist" finance Python machine learning "United States"
site:linkedin.com/jobs "Financial Data Scientist" Python "United States"
site:linkedin.com/jobs "Financial Analyst" Python modeling "United States"
site:linkedin.com/jobs "Portfolio Analytics Analyst" Python "United States"
site:linkedin.com/jobs "Investment Analytics Analyst" Python "United States"
site:linkedin.com/jobs "Treasury Analytics Analyst" Python "United States"
site:linkedin.com/jobs "ALM Analyst" Python "United States"
site:linkedin.com/jobs "Balance Sheet Analytics Analyst" Python "United States"
```

### Priority 3: Quantitative Research, ML, AI, and Applied Science

Include when responsibilities are data/model/research heavy, not primarily web application engineering.

```
site:linkedin.com/jobs "Quantitative Research Analyst" Python machine learning "United States"
site:linkedin.com/jobs "Machine Learning Engineer" finance Python "United States"
site:linkedin.com/jobs "AI Engineer" financial Python "United States"
site:linkedin.com/jobs "Applied Scientist" finance Python "United States"
site:linkedin.com/jobs "NLP" finance Python "United States"
site:linkedin.com/jobs "time-series" Python forecasting finance "United States"
site:linkedin.com/jobs "portfolio optimization" Python "United States"
```

### Priority 4: Data and Research Infrastructure

Use as a wider net only when the posting supports quantitative research, ML, analytics engineering, data/model pipelines, or financial data systems.

```
site:linkedin.com/jobs "Data Engineer" finance Python SQL Snowflake "United States"
site:linkedin.com/jobs "Analytics Engineer" finance SQL Python "United States"
site:linkedin.com/jobs "Research Engineer" Python machine learning finance "United States"
site:linkedin.com/jobs "ML Platform" finance Python "United States"
site:linkedin.com/jobs "model pipeline" Python finance "United States"
```

## Company and Sector Targets

No strict company-only list. Prioritize relevant roles at:
- Banks and financial institutions.
- Asset managers, hedge funds, and investment firms.
- Fintech companies.
- Insurance companies.
- Financial-data and analytics companies.
- Technology companies hiring quantitative, data science, ML, or AI talent.
- Consulting firms with strong quantitative/modeling teams.

Do not exclude strong opportunities because the company is outside a predefined list.

## Keyword Bank

Core:
- Python
- Quantitative modeling
- Statistical modeling
- Machine learning
- Risk modeling
- SQL

Additional:
- CECL / ACL
- Credit risk
- Prepayment modeling
- Survival analysis
- Time-series analysis
- Portfolio optimization
- Gurobi
- CVXOPT
- Snowflake
- AWS
- R
- Financial modeling
- ALM
- Treasury analytics
- Model validation
- Backtesting
- NLP
- PyTorch
- LightGBM
- Factor models

## Location Filter

United States only.

Include:
- Remote, hybrid, and onsite roles in the United States.
- National searches, not only one metro area.
- Strong quantitative/financial/technical markets, including New York City, Boston, Chicago, Charlotte, Raleigh-Durham, Washington DC / Northern Virginia, Atlanta, Dallas, Austin, San Francisco Bay Area, and Seattle.
- Relocation roles when the opportunity is sufficiently strong.

Exclude:
- Non-US roles.
- Roles requiring relocation outside the United States.

## Experience and Seniority Filter

Must-haves:
- Full-time position.
- Appropriate for early-career candidates or candidates with a relatively low experience requirement.
- Substantive quantitative, analytical, financial, data, ML, or AI work.

Experience policy:
- 0-2 years required: strong target.
- 3 years required: target.
- 4 years required: stretch, still include.
- 5 years required: selective stretch; include if skills strongly match.
- 6+ years required: normally exclude unless the posting clearly indicates flexibility.

Prefer:
- Analyst
- Associate
- Junior
- Early Career
- New Grad
- Level I
- Level II

Review carefully:
- Senior
- Lead
- Level III

Normally exclude:
- Staff
- Principal
- Director
- Senior Manager
- VP roles that clearly require substantial management or senior experience

Do not reject jobs based only on title. Read the minimum-experience requirements because corporate leveling varies substantially.

Do not automatically convert a master's degree into two years of professional experience. Do not treat two master's degrees as four years of experience. Count education as an experience substitute only when the posting explicitly provides that substitution.

## Immigration / Work Authorization Filter

Do not use immigration status as an automatic discovery or ranking exclusion unless the posting has a hard legal eligibility requirement the candidate cannot satisfy, such as U.S. citizenship, permanent residency, export-control eligibility, or security clearance.

Do not reject an otherwise strong role merely because sponsorship information is missing.

If an employer explicitly states "no current or future sponsorship," "we do not sponsor," or similar, keep the role when it is otherwise relevant and mark it with a **SPONSORSHIP RISK** flag. Do not silently remove it.

If a posting requires citizenship, permanent residency, export-control eligibility, or security clearance, quote the exact wording and flag it as **ELIGIBILITY REVIEW** or **FAIL** according to `04-job-evaluation.md`.

## Language Filter

Working languages:
- English - fluent / professional working proficiency.
- Mandarin Chinese - native.

Apply `04-job-evaluation.md`'s Language Gate: a posting requiring a language not declared here is excluded; a posting requiring a higher level than declared in a listed language is flagged, not silently passed.

## Date Filter

Only include actual currently open full-time job postings. Exclude generic career pages, talent communities, internships, expired listings, and recruiting articles. Prefer jobs posted within the last 14 days or with an application deadline that has not passed. If a posting date cannot be determined, include it but flag as "date unknown".

## Salary Filter

No hard minimum for initial discovery. Use market-competitive compensation for the role and location during ranking. Do not exclude an otherwise strong early-career opportunity solely because salary information is missing.

## Adapting Queries

If the user specifies a focus area, select queries from the matching functional bucket and generate 2-3 custom queries for that focus. Always rank by responsibilities and requirements, not title alone.
