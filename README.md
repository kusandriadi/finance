# finance

An [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) that acts as
a personal-finance helper: budgeting & cashflow, investing basics, model
portfolios, insurance, estate planning, KPR/property, reading financials, risk
management, macro/market context (with an Indonesia focus), plus a scriptable
morning **market briefing**.

## Contents

- `SKILL.md` — how the skill behaves (the entry point)
- `references/` — topic guides (budgeting, investing, insurance, KPR, macro, …)
- `scripts/` — `market_briefing.py`, `calc.py`, cron setup for a daily briefing
- `scripts/briefing.env.example` — copy to `briefing.env` and fill in your own
  notify channel/target (the real `briefing.env` is gitignored)

## Install

Drop this folder into your agent's skills directory (Claude Code:
`~/.claude/skills/finance/`). The agent discovers it via the `SKILL.md`
frontmatter.

## Notes

- **Educational, not financial advice.** Reference rates/numbers were captured
  around 2026 — verify current figures before acting.
- **Placeholders & paths.** Contact targets are placeholders (`+62XXXXXXXXXX`,
  chat id `123456789`); some scripts reference the author's paths
  (`/home/kusa/...`) and helper tools not included here. Adjust to your setup.

## License

[MIT](LICENSE).
