---
framework_version: 1.2.3
---

# Job Evaluation Framework

<!-- SETUP: Skill match areas and career goals are personalized by running /setup -->

## Eligibility Gate — run before scoring

If the candidate is not a citizen or permanent resident of the country they are applying in, run this first. It is a hard filter, not a scoring dimension, and it is separate from work-permit *timing*: timing asks "can they work the required hours yet?", eligibility asks "are they permitted to hold this job at all?". A candidate can pass timing and still be categorically excluded.

Read the posting's eligibility / work rights / "who can apply" section **verbatim** and classify:

| Posting wording | Verdict |
|-----------------|---------|
| Names a **citizenship or permanent-residency requirement** ("must be a citizen of X", "permanent resident", "PR required", "full working rights" where the employer means citizen/PR) | **FAIL — hard stop.** Do not score, do not draft. Quote the exact wording back to the user. |
| Requires a **security clearance** at any level | **FAIL** in most countries, since clearance is normally gated on citizenship. Verify the specific scheme rather than assuming. |
| **Explicitly names** the candidate's permit class, or says "international applicants welcome", "visa holders considered", "we sponsor" | **PASS** — verified acceptance. Worth noting as a positive in the application. |
| **Silent** on citizenship or residency | **PROCEED, but mark unverified.** Check the employer's own careers or international-applicant page before drafting. |

**Two rules that are easy to get wrong:**

1. **Silence is not permission.** Large graduate programs frequently gate eligibility on their own website rather than in the job ad. Highest-risk categories: professional-services firms, government and defence, banking, telecommunications, and anything touching critical infrastructure.
2. **A company-wide "we accept international applicants" statement is not role-level permission.** The common pattern is a general welcome followed by a *named list* of the specific programs or service lines it covers. Confirm the **specific posting or stream** appears on that list before drafting.

**Report an eligibility failure to the user with the quoted source** rather than silently dropping the role. They may know something about their own status that the profile does not record.

If the candidate's permit also constrains *hours* or *start date* (a student visa with a term-time cap, a permit that begins on graduation), record that as a second gate under this section during `/setup`, with the specific dates. Do not merge it with the eligibility question above — they fail for different reasons and need different answers.

A role that fails this gate is not scored and not drafted. Everything below applies only to roles that pass it.

### Immigration / Work Authorization Policy Override

For Lambert's US search, immigration status and sponsorship are not automatic job-discovery or ranking exclusions. Do not reject an otherwise strong role merely because sponsorship information is missing.

Use hard eligibility exclusions only when the posting names a legal requirement the candidate cannot satisfy, such as U.S. citizenship, permanent residency, export-control eligibility, or security clearance. Quote the exact wording and flag it clearly.

If an employer explicitly states "no current or future sponsorship," "we do not sponsor," or similar, mark the role with **SPONSORSHIP RISK** and continue scoring unless the user says to exclude it. Do not silently remove it.

Do not proactively disclose immigration details in CVs, cover letters, or free-text fields unless the application specifically asks. Never invent immigration status, citizenship, permanent residence, visa category, work authorization, or sponsorship eligibility.

#### Work-Authorization Form Answer Policy

Answer only according to the exact wording of the form question. Never automatically submit an application containing an immigration or work-authorization answer that has not been mapped unambiguously to these rules.

| Form question | Handling |
|---------------|----------|
| "Are you currently authorized to work in the United States?" | Answer **YES** only if the candidate currently has valid employment authorization for the position. If current authorization is not confirmed in the profile, flag for manual review. |
| "Do you currently require employer sponsorship to work in the United States?" | Answer **NO** only if the candidate can begin and continue working under current independent work authorization without employer sponsorship at the time of hire. Otherwise flag for manual review. |
| "Will you now or in the future require sponsorship for employment visa status?" | Do not guess and do not answer falsely. If future sponsorship need is not clearly and truthfully answerable from confirmed profile data, flag for manual review before submission. |
| "Will you require sponsorship in the future?" | Do not guess and do not answer falsely. If future sponsorship need is not clearly and truthfully answerable from confirmed profile data, flag for manual review before submission. |
| "Are you authorized to work permanently / indefinitely in the United States without sponsorship?" | Do not infer YES from temporary employment authorization. Answer according to the candidate's actual confirmed status; otherwise flag for manual review. |
| Combined current-authorization and future-sponsorship question | Answer each component truthfully according to its wording. If any component is ambiguous or unsupported by confirmed profile data, flag for manual review. |
| Ambiguous, unusual, or nonstandard wording | **MANUAL REVIEW.** Do not guess. |

Sponsorship should be tracked separately from job-fit scoring. A role with sponsorship uncertainty can still be a strong technical and career fit; surface the risk clearly and let the candidate decide whether to proceed.

## Language Gate — run before scoring

No dimension or gate anywhere in this framework currently checks a posting's language requirements against what the candidate actually speaks - it is not one of the five Scoring Dimensions below, not a field `/scrape` or `/rank` track, and not something `/apply`'s language detection (Step 1, which already extracts a posting's required language generically) has anywhere to report to. This gate adds that check, structured the same way as the Eligibility Gate above: read the posting, classify against profile data, and treat a hard mismatch as FAIL before scoring.

Read the posting's language requirements as stated for **the role itself** — not the language the ad happens to be written in. A posting written in a language you don't work in, for a role that only needs languages you do work in on the job, passes fine; only an explicit job-condition requirement ("fluent X required," "must communicate with the Y team in Z") triggers this check. For each language the posting requires as a job condition, compare it against your Languages table in CLAUDE.md / `01-candidate-profile.md`:

| Posting requirement vs. your Languages table | Verdict |
|---|---|
| Requires a language **not on your table at all** (e.g. "fluent Polish required," "must communicate with the Warsaw team in Russian," and you list no Polish/Russian row) | **FAIL — hard stop.** Do not score, do not draft. Quote the exact requirement line. |
| Requires a language you **do** list, but the posting's stated bar (as written — "fluent," "native," "C1+," "business-level") reads as plausibly **higher** than your declared level | **FLAG, then proceed.** Not a fail. Score and draft normally, but surface the gap explicitly in your report to the user (quote both the posting's requirement and your declared level) so they can judge it themselves — bars like "fluent" vary a lot by company and geography, and a recruiter may be flexible. Never silently drop the posting and never silently treat it as a clean pass. |
| Requires a language you list, at or below your declared level (or the posting doesn't specify a level at all — just names the language) | **PASS.** No note needed. |

Judge the level comparison the same way you judge everything else in this framework: read both sides as written and reason about it, don't force either into a rigid scale — CEFR letters, LinkedIn-style buckets ("professional working proficiency"), and plain-English words ("conversational," "fluent," "native") all appear in the wild and don't map onto each other precisely. When genuinely unsure whether a stated bar exceeds the candidate's level, prefer FLAG over a silent PASS — the human is meant to be the tiebreaker, not the gate.

**Worked example:** a candidate whose Languages table lists Spanish (Native) and English (B1/B2). A posting requiring "fluent Russian" → **FAIL**, Russian isn't declared at all. A posting requiring "fluent English" → **FLAG**, English is declared but "fluent" plausibly exceeds B1/B2 — score and draft the application, but tell the candidate this posting's bar may be a stretch and let them decide. A posting requiring "conversational English" or unspecified English → **PASS**, B1/B2 clears a "conversational" bar cleanly.

## Scoring Dimensions

Evaluate each job posting against these five dimensions:

### 1. Technical Skills Match (0-100)
How well do the required/preferred skills align with the candidate's capabilities?

| Score | Meaning |
|-------|---------|
| 80-100 | Core requirements are primary skills |
| 60-79 | Most requirements match, 1-2 gaps that are learnable |
| 40-59 | Partial match, significant upskilling needed |
| 0-39 | Fundamental mismatch |

**Strong match areas:** Quantitative modeling, risk modeling, Python-based research pipelines, financial mathematics, machine learning and statistical modeling, portfolio simulation, CECL forecasting, prepayment modeling, survival analysis, stochastic interest-rate modeling, Monte Carlo simulation.
**Moderate match areas:** AWS-based model workflow support, Snowflake analytics, commercial banking operations, AI agentic workflows, Microsoft Power Platform, Copilot Studio, ESG reporting, executive reporting.
**Weak match areas:** Primarily application/web-development software engineering, senior people-management roles, non-quantitative operations/reporting roles, and non-finance domain experience unless the work clearly involves data, ML, AI, quantitative systems, or research infrastructure.

### 2. Experience Match (0-100)
Does work history align with what they're looking for? Match on the function and nature of the work performed, not the literal job title - a "Data Consultant" and a "Data Scientist" role can be functionally identical.

| Score | Meaning |
|-------|---------|
| 80-100 | Direct experience in the same domain and role type |
| 60-79 | Related experience, transferable skills clear |
| 40-59 | Adjacent experience, would need to make the case |
| 0-39 | Unrelated experience |

**Strong:** Quantitative finance, financial mathematics, risk modeling, banking analytics, mortgage/prepayment modeling, systematic trading research, portfolio simulation.
**Moderate:** Cloud-supported ML workflows, AI workflow automation, commercial banking business exposure, ESG reporting, technical consulting around analytical models.
**Entry-level:** Generalist software engineering, non-finance data science domains, product analytics outside financial services, production ML platform engineering.

### 3. Behavioral/Culture Fit (0-100)
Does the role and company culture match the behavioral profile?

| Score | Meaning |
|-------|---------|
| 80-100 | Culture strongly matches behavioral preferences |
| 60-79 | Mixed signals but mostly compatible |
| 40-59 | Some friction areas |
| 0-39 | Significant culture mismatch |

**Red flags to research:** Department disorganization, work dominated by maintenance over development, poor chemistry with leadership, culture mismatches. Check reviews, media coverage, LinkedIn connections, and network contacts for insider perspective.

### 4. Location & Logistics (Pass/Fail + Notes)
- United States full-time roles: PASS.
- Remote or hybrid within the United States: PASS.
- Onsite roles in strong quantitative/financial/technical markets: PASS if the opportunity is strong enough to justify relocation.
- Non-US roles: FAIL.
- Frequent international travel: FLAG.

### 5. Career Alignment & Motivation (0-100)
Does this role advance career goals and contain tasks that energize?

| Score | Meaning |
|-------|---------|
| 80-100 | Strongly aligned with career direction, clear growth path |
| 60-79 | Good role but only partially aligned with long-term goals |
| 40-59 | Decent job but doesn't build toward career goals |
| 0-39 | Dead end or backwards step |

**Career goals:**
- Build a career across quantitative finance, risk modeling, data science, machine learning, and financial analytics.
- Work on roles where Python, statistics, modeling, machine learning, optimization, or quantitative finance are core responsibilities.
- Stay open to multiple job-title families when the underlying work is quantitative, analytical, financial, data, ML, AI, or research-infrastructure focused.

**Motivation filter:** Evaluate not just whether you *can* do the tasks, but whether the tasks will *energize* you. Consider:
- Tasks that energize: statistical and predictive modeling, financial/risk modeling, machine learning, model development and validation, quantitative research, portfolio/risk analytics, credit and prepayment modeling, forecasting, scenario analysis, data/model pipelines, optimization, and Python-based research or production workflows.
- Tasks that drain: primarily manual reporting, operations, administrative work, or application/web development where data, ML, AI, quantitative systems, or research infrastructure are not meaningful parts of the role.
- Non-task factors: leadership style, department culture, company values, degree of autonomy

**Life situation alignment:** Consider personal constraints:
- **Security**: No hard salary minimum for initial discovery; consider market-competitive compensation during ranking, but do not exclude strong early-career roles solely because salary is missing.
- **Flexibility**: United States only; onsite, hybrid, and remote are all acceptable; relocation is acceptable for sufficiently strong opportunities.
- **Professional development**: Prioritize early-career or lower-experience full-time roles with substantive quantitative, analytical, financial, data, ML, or AI work.

### Search and Ranking Strategy

Do not force the candidate into a single job-title category. Search and rank across functional buckets, then judge postings by actual responsibilities and requirements.

Relevant titles may include, but are not limited to: Risk Analyst, Quantitative Analyst, Quantitative Finance Analyst, Quantitative Risk Analyst, Risk Modeler, Model Development Analyst, Credit Risk Analyst, Credit Risk Modeler, Model Risk Analyst, Model Validation Analyst, Data Scientist, Financial Data Scientist, Treasury Analytics Analyst, ALM / Balance Sheet Analytics Analyst, Portfolio Analytics Analyst, Quantitative Research Analyst, Investment Analytics Analyst, Machine Learning Engineer, AI Engineer, Applied Scientist, Data Engineer, and Analytics Engineer.

Include a role when the underlying work involves Python, modeling, statistics, machine learning, financial risk, optimization, quantitative research, data pipelines, AI, or financial analytics, even if the title is broad or nonstandard.

Avoid software-engineering roles that are primarily application or web development unless the posting meaningfully involves data, ML, AI, quantitative systems, or research infrastructure.

Experience filter:
- 0-2 years required: strong target.
- 3 years required: target.
- 4 years required: stretch, still include.
- 5 years required: selective stretch, include only when skills strongly match.
- 6+ years required: normally exclude unless the posting clearly indicates flexibility.

Do not automatically convert a master's degree into professional experience, and do not treat two master's degrees as four years of experience. Count education as an experience substitute only when the posting explicitly allows it.

### 6. Salary Benchmark (Optional)

If the salary lookup tool is configured (`salary_data.json` exists), look up the company:
```
python salary_lookup.py "<Company Name>" --json
```

If a city is known from the posting, add `--city "<City>"` to narrow results.

Present findings as:
```
### Salary Benchmark
| Metric | Value |
|--------|-------|
| [Category] index | XX.X (+/-X.X% vs baseline) |
| Overall index | XX.X (+/-X.X% vs baseline) |
```

Interpret results relative to the baseline defined in the data file's metadata. For index-based data, higher typically means above-market compensation.

If the salary tool is not configured, skip this section.

## Output Format

Present the evaluation as:

```
## Job Fit Evaluation: [Role] at [Company]

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technical Skills | XX/100 | [brief note] |
| Experience Match | XX/100 | [brief note] |
| Behavioral Fit | XX/100 | [brief note] |
| Location | PASS/FAIL | [brief note] |
| Career Alignment | XX/100 | [brief note] |

**Overall Score: XX/100** (weighted average of scored dimensions)

### Verdict: [Strong Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit]

### Key Strengths for This Role
- [bullet points]

### Gaps to Address
- [bullet points]

### Recommendation
[1-2 sentences: apply/skip/apply with caveats]

### Company Research Checklist
- [ ] Checked company website (mission, values, recent news)
- [ ] Checked review sites (Glassdoor, Jobindex, etc.)
- [ ] Checked LinkedIn for team size, recent hires, connections
- [ ] Checked media for restructuring, growth, or workplace issues
- [ ] Identified network contacts who may know the team/manager
```

## Weighting
- Technical Skills: 30%
- Experience Match: 25%
- Behavioral Fit: 15%
- Career Alignment: 30%

(Location is pass/fail, not weighted)

## Thresholds
- **Strong Fit** (75+): Definitely apply, tailor everything
- **Good Fit** (60-74): Apply, address gaps in cover letter
- **Moderate Fit** (45-59): Consider carefully, discuss with user
- **Weak Fit** (30-44): Probably skip unless strategic reasons
- **Poor Fit** (<30): Skip

## Pre-Application: Call the Employer (Best Practice)

Before writing the application, consider whether the candidate should call the contact person listed in the posting. **Only call if there are substantive questions** - never call just to "be remembered."

### When to Suggest Calling
- The posting has unclear or ambiguous requirements
- It's unclear which competencies are essential vs. nice-to-have
- The role description is vague about day-to-day tasks
- There's a named contact person who invites questions

### Good Questions to Ask
- "What are the primary challenges in this role?"
- "How is time typically divided across the listed responsibilities?"
- "Which competencies are most critical for success in this position?"
- "What does success look like in the first 6-12 months?"

### Rules for the Call
- Prepare a 30-second "elevator pitch" about your background in case they ask
- The call's purpose is **gathering information**, not delivering a pitch
- Take notes - use what you learn to tailor the application
- Reference the conversation naturally in the cover letter ("After speaking with [name], I was especially drawn to...")
