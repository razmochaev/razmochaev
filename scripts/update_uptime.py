#!/usr/bin/env python3
"""Update daily Uptime inside README.md since 2004-04-21."""

import calendar
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BIRTH_DATE = date(2004, 4, 21)
UPTIME_RE = re.compile(r"(<!-- UPTIME:START -->).*?(<!-- UPTIME:END -->)")


def calc_uptime(today: date) -> str:
    """Compute exact calendar years, months, and days since BIRTH_DATE."""
    years = today.year - BIRTH_DATE.year
    months = today.month - BIRTH_DATE.month
    days = today.day - BIRTH_DATE.day
    if days < 0:
        months -= 1
        prev_month = 12 if today.month == 1 else today.month - 1
        prev_year = today.year - 1 if today.month == 1 else today.year
        days_in_prev = calendar.monthrange(prev_year, prev_month)[1]
        days += days_in_prev
    if months < 0:
        years -= 1
        months += 12
    y_str = f"{years} year" if years == 1 else f"{years} years"
    m_str = f"{months} month" if months == 1 else f"{months} months"
    d_str = f"{days} day" if days == 1 else f"{days} days"
    return f"{y_str}, {m_str}, {d_str}"


def main() -> None:
    today = datetime.now(ZoneInfo("Europe/Berlin")).date()
    uptime_str = calc_uptime(today)
    readme_path = Path(__file__).resolve().parent.parent / "README.md"
    content = readme_path.read_text(encoding="utf-8")
    updated, count = UPTIME_RE.subn(rf"\g<1>{uptime_str}\g<2>", content)
    if count != 1:
        raise RuntimeError(f"Expected 1 UPTIME marker block in README.md, found {count}")
    readme_path.write_text(updated, encoding="utf-8")
    print(f"Updated {readme_path} (today={today}, uptime={uptime_str})")


if __name__ == "__main__":
    main()
