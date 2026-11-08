# Backtest summary (condensed, 2026-11-08)

The full reports are `backtest_report.md` (v2→v3) and `sizing_report.md` (v4 ranking and sizing), kept in the operator workspace. Every study was read-only.

**Notation used in the tables:**
- **Taker** copies are priced at the wallet's average entry + 1¢, minus the US fee 0.095·C·p·(1−p).
- **Maker / gross** means filled at the wallet's entry with no fee. This is an upper bound for resting orders.
- **±** is 1 standard error.

## 1. Post-mortem of the first 8 settled picks (2-6)
| Pick | Result | Wallet copied (size vs. its median) | Wallet main league | Own ROI / leaderboard Nov 7 → Nov 8 | Segment history | Entry → close (CLV) |
|---|---|---|---|---|---|---|
| LSU −6.5 (CFB spread) | L | EdZachary (4.71x) | NBA | +6.6% / +19.4% → −23.9% | 19 bets | 0.48 → 0.485 |
| Kentucky +6.5 (CFB spread) | L | 0x3DF ($18.2k, 1.0x) + 0x16bb ($371, 0.1x token) | MLB | −7.6% / +27.3% → −5.3% | 189 bets, flat +1.9% | 0.514 → 0.515 |
| Fresno St ML (CFB) | L | lightotunnel35 (5.85x) | CFB, but a 21-day-old wallet | +13.2% / +14.0% → −3.1% | 19 bets | 0.513 → 0.505 |
| Panthers +2.5 (NFL spread) | L | 0x3DF (0.63x) + gmpm2 (0.99x) | MLB / World Cup | −7.6% | 0x3DF NFL spread $ROI −17.4% | 0.48 → 0.445 |
| Falcons ML (NFL) | L | EdZachary (1.93x) + 0xBc43 ($289, 0.08x token) | NBA | +6.6% / +19.4% → −23.9% | 24 bets | 0.386 → 0.375 |
| Eagles +3.5 (NFL spread) | L | 0x16bb (9.07x) | MLB | −1.0% / +11.6% → −44.9% | NFL spread $ROI −25% | 0.557 → 0.565 |
| Baylor −10.5 (CFB spread) | W | EdZachary (3.68x) | NBA | +6.6% | 19 bets | 0.46 → 0.475 |
| Kennesaw St ML (CFB) | W | 0x16bb (6.35x) | MLB | −1.0% | 26 bets | 0.496 → 0.485 |

What went wrong:
- **Off-league copying.** Every pick was outside the wallet's main league, except Fresno, which came from a brand-new wallet.
- **Leaderboard ROI wasn't real.** It is a rolling window that flipped sign overnight.
- **Fake consensus.** Token positions were counted as a second wallet agreeing.
- **Losing segments.** Two picks were in segments where the wallet was already losing.

Going 2-6 on coin-flip prices happens about 14% of the time by luck alone.

*Update:* the Browns-Saints Over 42.5 settled later as a **win**, so all settled bets stand at 3-6. The 49ers −9.5 is still open (see TRADE_LOG.md).

## 2. Walk-forward test of copy rules (Aug 10 – Nov 8, 13 weeks, $5 flat, 215 wallets)
| Rule | Copies | Hit | Taker ROI | Gross (maker) |
|---|---|---|---|---|
| Every pre-game bet, all wallets | 32,866 | 51.2% | −7.2% ± 0.6 | −0.5% |
| v2 as run (leaderboard ROI ≥ 5%, one strong or two agreeing) | 1,144 | 56.2% | −4.0% ± 2.8 | +2.2% |
| Size ≥ 3x median (own ROI ≥ 5%) | 1,160 | 54.3% | −9.2% ± 2.8 | −3.1% |
| Size < 1x median (own ROI ≥ 5%) | 750 | 49.9% | −2.3% ± 4.4 | +5.1% |
| P4 = v3 core + same league + segment flat ROI > 0 + no totals + price 0.40-0.85 | 745 | 57.3% | −1.7% ± 3.3 | +4.4% |
| P7 = P4 + wallet CLV > 0 (**v3 rule**) | 439 | 57.6% | +1.0% ± 4.4 | +7.3% |
| P10 = P4 + 2 independent wallets | 40 | 60.0% | +9.2% ± 14.9 | +15.9% |

Two caveats on P7:
- It is 78% esports. On traditional sports alone it was −4.5% ± 9.6 over 97 copies.
- Totals and longshots under 35¢ were the worst slices in every set: −11% to −20% and −17% to −31% respectively.

## 3. Ranking by credibility score (Jun 1 – Nov 8, 23 weeks, 76,535 test bets)
The score is the empirical-Bayes shrunk flat ROI per wallet × league × bet type, computed from data before each week.

| Group | Copies | Maker | Taker |
|---|---|---|---|
| All: top decile | 4,660 | +0.8% ± 1.6 | −6.0% ± 1.6 |
| All: rest | 23,029 | −0.3% ± 0.7 | −7.1% ± 0.7 |
| Tradeable: top decile | 2,277 | +1.6% ± 1.9 | −4.4% ± 1.9 |
| Tradeable: rest | 13,610 | +0.5% ± 0.8 | −5.5% ± 0.8 |
| Tradeable: score > 0 | 8,844 | +2.0% ± 1.0 | −4.1% ± 1.0 |
| Tradeable: score ≤ 0 | 8,685 | −0.6% ± 1.0 | −6.6% ± 1.0 |
| Tradeable quintiles Q1→Q5 | ~4.1k each | −2.2 / +0.6 / +1.1 / +3.6 / +0.3% | |
| Watch tier, own ROI ≥ 0 | 1,843 | +6.0% ± 2.2 | −0.3% ± 2.2 |
| Watch tier, own ROI < 0 | 2,141 | −0.4% ± 2.1 | −6.6% ± 2.0 |

- The segment-level Spearman between score and next-week ROI is **0.006** (p = 0.41).
- The score mostly filters out bad segments; it does not reliably find the best ones. The wallet's own ROI ≥ 0 is the strongest separator. That split was chosen after a first look, so treat it with care.

## 4. Sizing skill
Bet size is measured as the size multiple x = stake / the wallet's median stake.

| Test (23 weeks) | Wallets | Copies | Out-of-sample Spearman(x, z) | Flat maker / taker | √x-sized maker / taker |
|---|---|---|---|---|---|
| Flagged sizers (p < 0.05) | 4 | 1,092 | −0.013 | −7.3% / −13.7% | −6.8% / −13.1% |
| Not flagged | 112 | 37,669 | −0.018 | −0.3% / −6.9% | −0.2% / −6.7% |
| Looser flag (p < 0.2, 13 weeks) | 17 | 1,957 | −0.009 | −2.8% / −9.2% | −2.8% / −9.1% |

- No wallet is a proven sizer today. Three pass p < 0.05, but none survives a Benjamini-Hochberg correction at FDR 10% across the 134 wallets tested.
- Bigger bets did not win more often out of sample.

## 5. Stake rule (base $5; √x scaling, clamped to $3-$12, for proven sizers only; daily cap 25% of $99)
| Pick set | Copies | Flat maker / taker | v4 rule | Capped (flat) maker / taker, PnL |
|---|---|---|---|---|
| P4 (v3) | 828 | +4.3% / −1.8% | identical | +4.1% / −1.8%, +$79 / −$34 on $1,915 |
| P7 (v3 + CLV) | 470 | +7.1% / +0.8% | identical | +10.0% / +3.7%, +$148 / +$54 |
| **v4 (keep + watch)** | 1,973 | **+5.5% ± 2.1 / −0.8% ± 2.1** | +5.5% / −0.7% | +2.1% / −3.9%, +$44 / −$84 on $2,145 |
| Top decile only | 2,277 | +1.6% / −4.4% | same | −1.9% / −7.9% |

**Conclusion:** sizing adds nothing measurable, and ranking within good segments adds little. v4 is about breakeven as a taker. It is positive only if resting orders fill at the trader's price, and that is an optimistic assumption.

## Caveats
- Only 13-23 weeks of data, with overlapping wallets, so standard errors understate the true uncertainty.
- Activity history was capped at 30k-90k records per wallet.
- The maker numbers ignore fill risk and adverse selection.
- Many esports and tennis markets in the data aren't listed on Polymarket US.
