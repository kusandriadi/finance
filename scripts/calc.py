#!/usr/bin/env python3
"""calc.py — financial calculators for the finance skill.

Self-contained (stdlib only). Turns the principles in references/ into concrete
numbers so advice is quantified, not hand-waved. All money in IDR (Rupiah).

Subcommands:
    fv         Future value of a lump sum and/or recurring monthly saving
    pv         Present value (what a future amount is worth today)
    loan       Loan / KPR amortization (monthly payment + schedule summary)
    retire     Retirement number (FIRE) from annual expenses
    education  Child-education fund: future cost + required monthly saving
    dca        Required monthly saving to hit a goal by a deadline
    real       Convert nominal return to real (inflation-adjusted) return
    zakat      Zakat maal (2.5% above nisab)

Examples:
    python3 calc.py fv --monthly 1000000 --years 20 --rate 10
    python3 calc.py loan --principal 500000000 --years 15 --rate 9
    python3 calc.py retire --annual-expense 120000000 --swr 3.5
    python3 calc.py education --cost-today 200000000 --years 15 --edu-inflation 10 --rate 8
    python3 calc.py dca --goal 200000000 --years 4 --rate 6
    python3 calc.py real --nominal 8 --inflation 4

Notes:
    Returns are nominal annual %. "real" return = adjusted for inflation.
    Output is educational, not financial advice. Assumptions are explicit so
    you can sanity-check them. Use conservative return assumptions.
"""
import argparse
import sys


# ---------- formatting ----------

def rp(x):
    """Format a number as Indonesian Rupiah: Rp1.234.567."""
    return "Rp" + f"{round(x):,.0f}".replace(",", ".")


def pct(x):
    return f"{x:.2f}%"


def line(label, value):
    print(f"  {label:<34} {value}")


def header(title):
    print(f"\n=== {title} ===")


# ---------- core math ----------

def fv_lump(pv, annual_rate, years):
    """Future value of a single lump sum, compounded annually."""
    return pv * (1 + annual_rate) ** years


def fv_annuity(monthly, annual_rate, years):
    """FV of recurring monthly contributions, compounded monthly (ordinary annuity)."""
    i = annual_rate / 12
    n = years * 12
    if i == 0:
        return monthly * n
    return monthly * (((1 + i) ** n - 1) / i)


def required_monthly(goal_fv, annual_rate, years):
    """Monthly contribution needed to reach goal_fv, compounded monthly."""
    i = annual_rate / 12
    n = years * 12
    if i == 0:
        return goal_fv / n
    return goal_fv * i / ((1 + i) ** n - 1)


def loan_payment(principal, annual_rate, years):
    """Fixed monthly payment (annuitas) for an amortizing loan."""
    i = annual_rate / 12
    n = years * 12
    if i == 0:
        return principal / n
    return principal * i * (1 + i) ** n / ((1 + i) ** n - 1)


# ---------- subcommands ----------

def cmd_fv(a):
    r = a.rate / 100
    fv_l = fv_lump(a.lump, r, a.years) if a.lump else 0.0
    fv_a = fv_annuity(a.monthly, r, a.years) if a.monthly else 0.0
    total = fv_l + fv_a
    contributed = a.lump + a.monthly * a.years * 12
    header("Future Value")
    if a.lump:
        line("Lump sum awal", rp(a.lump))
    if a.monthly:
        line("Setoran per bulan", rp(a.monthly))
    line("Horizon", f"{a.years} tahun")
    line("Asumsi return (nominal)", pct(a.rate))
    print("  " + "-" * 46)
    line("Total disetor", rp(contributed))
    line("Nilai akhir (FV)", rp(total))
    line("Hasil compounding", rp(total - contributed))
    if a.inflation:
        real = total / (1 + a.inflation / 100) ** a.years
        line(f"Nilai riil (daya beli, infl {pct(a.inflation)})", rp(real))


def cmd_pv(a):
    r = a.rate / 100
    pv = a.future / (1 + r) ** a.years
    header("Present Value")
    line("Nilai masa depan", rp(a.future))
    line("Horizon", f"{a.years} tahun")
    line("Asumsi diskonto", pct(a.rate))
    print("  " + "-" * 46)
    line("Nilai sekarang (PV)", rp(pv))
    print(f"\n  Artinya: {rp(a.future)} dalam {a.years} th setara {rp(pv)} hari ini.")


def cmd_loan(a):
    r = a.rate / 100
    n = a.years * 12
    pay = loan_payment(a.principal, r, a.years)
    total_paid = pay * n
    total_interest = total_paid - a.principal
    header("Amortisasi Pinjaman / KPR")
    line("Pokok pinjaman", rp(a.principal))
    line("Tenor", f"{a.years} tahun ({n} bulan)")
    line("Bunga (anuitas, p.a.)", pct(a.rate))
    print("  " + "-" * 46)
    line("Cicilan per bulan", rp(pay))
    line("Total dibayar", rp(total_paid))
    line("Total bunga", rp(total_interest))
    line("Bunga / pokok", pct(total_interest / a.principal * 100))
    if a.income:
        ratio = pay / a.income * 100
        verdict = "sehat" if ratio <= 35 else "berat — di atas 35%"
        line("Rasio cicilan / penghasilan", f"{pct(ratio)} ({verdict})")
    # First-year split to show how early payments are mostly interest.
    bal = a.principal
    yr_interest = yr_principal = 0.0
    for _ in range(min(12, n)):
        intr = bal * (r / 12)
        prin = pay - intr
        bal -= prin
        yr_interest += intr
        yr_principal += prin
    print("\n  Tahun pertama (kenapa cicilan awal terasa 'jalan di tempat'):")
    line("  → ke bunga", rp(yr_interest))
    line("  → ke pokok", rp(yr_principal))


def cmd_retire(a):
    multiple = 100 / a.swr
    target = a.annual_expense * multiple
    header("Angka Pensiun / FIRE")
    line("Pengeluaran per tahun (hari ini)", rp(a.annual_expense))
    line("Safe withdrawal rate", pct(a.swr))
    line("Pengali (1 / SWR)", f"{multiple:.1f}×")
    print("  " + "-" * 46)
    line("Target portofolio (nilai hari ini)", rp(target))
    if a.years:
        infl = (a.inflation or 4) / 100
        future_expense = a.annual_expense * (1 + infl) ** a.years
        future_target = future_expense * multiple
        print(f"\n  Disesuaikan inflasi {pct((a.inflation or 4))} selama {a.years} th:")
        line("  Pengeluaran/th saat pensiun", rp(future_expense))
        line("  Target portofolio (nominal)", rp(future_target))
        if a.rate:
            need = required_monthly(future_target, a.rate / 100, a.years)
            line(f"  Setoran/bln (return {pct(a.rate)})", rp(need))
    print("\n  Catatan: SWR 4% = konteks AS. Di ID banyak pakai 3-3,5% (lebih aman).")


def cmd_education(a):
    edu_infl = a.edu_inflation / 100
    future_cost = a.cost_today * (1 + edu_infl) ** a.years
    header("Dana Pendidikan Anak")
    line("Biaya hari ini", rp(a.cost_today))
    line("Mulai dipakai dalam", f"{a.years} tahun")
    line("Inflasi pendidikan", pct(a.edu_inflation))
    print("  " + "-" * 46)
    line("Estimasi biaya nanti", rp(future_cost))
    if a.rate:
        need = required_monthly(future_cost, a.rate / 100, a.years)
        line(f"Setoran/bln (return {pct(a.rate)})", rp(need))
    print("\n  Inflasi pendidikan biasanya lebih tinggi dari inflasi umum (~10%/th).")


def cmd_dca(a):
    need = required_monthly(a.goal, a.rate / 100, a.years)
    contributed = need * a.years * 12
    header("Target Menabung (DCA)")
    line("Target dana", rp(a.goal))
    line("Tenggat", f"{a.years} tahun")
    line("Asumsi return", pct(a.rate))
    print("  " + "-" * 46)
    line("Setoran per bulan", rp(need))
    line("Total disetor", rp(contributed))
    line("Bantuan compounding", rp(a.goal - contributed))


def cmd_real(a):
    nominal = a.nominal / 100
    infl = a.inflation / 100
    real = (1 + nominal) / (1 + infl) - 1
    header("Return Riil (setelah inflasi)")
    line("Return nominal", pct(a.nominal))
    line("Inflasi", pct(a.inflation))
    print("  " + "-" * 46)
    line("Return riil", pct(real * 100))
    approx = a.nominal - a.inflation
    print(f"\n  Perkiraan kasar (nominal − inflasi) = {pct(approx)}; rumus tepat di atas.")


def cmd_zakat(a):
    # Nisab = 85 gram emas × harga emas/gram.
    nisab = 85 * a.gold_price
    header("Zakat Maal")
    line("Harga emas / gram", rp(a.gold_price))
    line("Nisab (85 gram emas)", rp(nisab))
    line("Total harta (haul 1 th)", rp(a.wealth))
    print("  " + "-" * 46)
    if a.wealth >= nisab:
        zakat = a.wealth * 0.025
        line("Wajib zakat?", "Ya (≥ nisab)")
        line("Zakat (2,5%)", rp(zakat))
    else:
        line("Wajib zakat?", "Tidak (< nisab)")
    print("\n  Cek nisab & haul ke lembaga resmi (BAZNAS/LAZ) untuk kepastian.")


# ---------- CLI ----------

def build_parser():
    p = argparse.ArgumentParser(
        description="Financial calculators (IDR). Educational, not advice.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fv", help="Future value of lump sum + monthly saving")
    f.add_argument("--lump", type=float, default=0, help="Lump sum awal (IDR)")
    f.add_argument("--monthly", type=float, default=0, help="Setoran/bulan (IDR)")
    f.add_argument("--years", type=float, required=True)
    f.add_argument("--rate", type=float, required=True, help="Return nominal %/th")
    f.add_argument("--inflation", type=float, default=0, help="Untuk nilai riil")
    f.set_defaults(func=cmd_fv)

    v = sub.add_parser("pv", help="Present value of a future amount")
    v.add_argument("--future", type=float, required=True)
    v.add_argument("--years", type=float, required=True)
    v.add_argument("--rate", type=float, required=True, help="Diskonto %/th")
    v.set_defaults(func=cmd_pv)

    l = sub.add_parser("loan", help="Loan/KPR amortization")
    l.add_argument("--principal", type=float, required=True)
    l.add_argument("--years", type=float, required=True)
    l.add_argument("--rate", type=float, required=True, help="Bunga %/th (anuitas)")
    l.add_argument("--income", type=float, default=0, help="Penghasilan/bln untuk rasio")
    l.set_defaults(func=cmd_loan)

    r = sub.add_parser("retire", help="Retirement / FIRE number")
    r.add_argument("--annual-expense", type=float, required=True)
    r.add_argument("--swr", type=float, default=3.5, help="Safe withdrawal rate % (default 3.5)")
    r.add_argument("--years", type=float, default=0, help="Tahun ke pensiun (opsional)")
    r.add_argument("--inflation", type=float, default=0, help="Default 4 jika --years dipakai")
    r.add_argument("--rate", type=float, default=0, help="Return untuk hitung setoran/bln")
    r.set_defaults(func=cmd_retire)

    e = sub.add_parser("education", help="Child education fund")
    e.add_argument("--cost-today", type=float, required=True)
    e.add_argument("--years", type=float, required=True)
    e.add_argument("--edu-inflation", type=float, default=10, help="Default 10%/th")
    e.add_argument("--rate", type=float, default=0, help="Return untuk setoran/bln")
    e.set_defaults(func=cmd_education)

    d = sub.add_parser("dca", help="Required monthly saving for a goal")
    d.add_argument("--goal", type=float, required=True)
    d.add_argument("--years", type=float, required=True)
    d.add_argument("--rate", type=float, required=True)
    d.set_defaults(func=cmd_dca)

    rr = sub.add_parser("real", help="Nominal -> real return")
    rr.add_argument("--nominal", type=float, required=True)
    rr.add_argument("--inflation", type=float, required=True)
    rr.set_defaults(func=cmd_real)

    z = sub.add_parser("zakat", help="Zakat maal (2.5% above nisab)")
    z.add_argument("--wealth", type=float, required=True, help="Total harta (IDR)")
    z.add_argument("--gold-price", type=float, required=True, help="Harga emas/gram (IDR)")
    z.set_defaults(func=cmd_zakat)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
