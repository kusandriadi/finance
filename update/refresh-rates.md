# Update: refresh rates & thresholds

Trigger: user says "update finance rates", "refresh angka pajak", "cek rate terbaru",
or `references/rates.md` looks stale (header date is old / a critical number is needed).

Goal: re-verify the volatile numbers in `references/rates.md` against official sources
and update the file + its "Terakhir diverifikasi" date. **Don't guess — verify.**

## Steps

1. **Read** `references/rates.md` to see the current values and what's flagged ⚠️.
2. **Verify each volatile item** via WebSearch/WebFetch against the official source:
   - **Pajak (PTKP, tarif progresif, final, UMKM, PPN, batas PKP):** DJP — pajak.go.id.
   - **LPS penjaminan + tingkat bunga penjaminan:** lps.go.id.
   - **BI-Rate (suku bunga acuan):** bi.go.id. (Don't store it long-term — it moves; just
     report current when asked.)
   - **Inflasi terbaru:** BPS — bps.go.id.
   - **Properti (BPHTB, PPh penjual, insentif PPN DTP):** DJP / Kementerian Keuangan / PUPR.
   - **Zakat nisab:** BAZNAS — baznas.go.id (depends on current gold price).
3. **Update** only the numbers that changed. Keep the structure; don't bloat.
4. **Bump the date:** set "Terakhir diverifikasi: <today>" in `rates.md` header.
5. **If a number couldn't be confirmed**, leave it with a ⚠️ note rather than inventing one.
6. **Report** to Kus: what changed, what stayed, what couldn't be verified.

## Notes

- Prefer primary/official sources over blogs. Cross-check if a figure looks off.
- Tax rules change with new UU/PP/PMK — note the regulation if you find a change.
- Numbers in other `references/*.md` should point back to `rates.md`, not re-hardcode.
  If you find a stale hardcoded figure elsewhere, replace it with a pointer here.
