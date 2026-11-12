# Trade log: Moneyball copy bets on Polymarket US

The source is the account's `portfolio.activities` and `portfolio.positions` (read-only SDK calls) as of 2026-11-11 10:35 PM PT, plus open resting orders at that time. Settlements were checked against the US activity feed (and, for the Penguins, the resolved market prices). No order IDs, account IDs, or keys are recorded here.

How to read the columns:
- **Price** is the price paid for the side we bought. For BUY_SHORT orders the exchange records 1 − price in LONG terms; the price here is the side we actually own.
- **Cost** = shares × price + fee.
- **Net** = payout − cost.
- All times are PT.
- Starting Nov 11, live stakes are about $10 per pick (they were $5 before that).

| Placed (PT) | Market (US slug) | Side | Price | Shares | Fee | Cost | Wallet copied | Result | Net |
|---|---|---|---|---|---|---|---|---|---|
| Nov 7 08:17 | LSU −6.5 vs Alabama (`asc-cfb-ala-lsu-2026-11-07-pos-6pt5`) | −6.50 (short) | 0.485 | 10 | $0.24 | $5.09 | EdZachary | **Loss** | −$5.09 |
| Nov 7 08:17 | Browns-Saints Over 42.5 (`tsc-nfl-cle-no-2026-11-08-total-42pt5`) | Over | 0.500 | 10 | $0.24 | $5.24 | 0x3DFb153c… | **Win** (settled Nov 8 2:11 PM) | +$4.76 |
| Nov 7 08:39 | Baylor −10.5 vs Iowa St (`asc-cfb-iowast-bayl-2026-11-07-pos-10pt5`) | −10.50 (short) | 0.460 | 10 | $0.24 | $4.84 | EdZachary | **Win** | +$5.16 |
| Nov 7 08:39 | Kennesaw St ML vs Delaware (`aec-cfb-del-kenest-2026-11-07`) | Owls (short) | 0.500 | 10 | $0.24 | $5.24 | 0x16bb9951… | **Win** | +$4.76 |
| Nov 7 13:29 + 13:38 | Fresno St ML at Utah St (`aec-cfb-frest-utahst-2026-11-07`) | Bulldogs | 0.500 | 30 (10 + 20) | $0.72 | $15.72 | lightotunnel35 | **Loss** | −$15.72 |
| Nov 7 13:29 | Kentucky +6.5 at Tennessee (`asc-cfb-uk-tenn-2026-11-07-pos-6pt5`) | +6.50 | 0.525 | 9 | $0.21 | $4.94 | 0x3DFb153c… (+0x16bb token) | **Loss** | −$4.94 |
| Nov 7 21:12 | Panthers +2.5 vs Broncos (`asc-nfl-den-car-2026-11-08-neg-2pt5`) | +2.50 (short) | 0.485 | 10 | $0.24 | $5.09 | 0x3DFb153c… + gmpm2 | **Loss** | −$5.09 |
| Nov 7 21:12 | Eagles +3.5 at Giants (`asc-nfl-nyg-phi-2026-11-08-neg-3pt5`) | +3.50 (short) | 0.550 | 9 | $0.21 | $5.16 | 0x16bb9951… | **Loss** | −$5.16 |
| Nov 7 21:12 | 49ers −9.5 vs Raiders (`asc-nfl-lv-sf-2026-11-08-pos-9pt5`) | −9.50 (short) | 0.505 | 9 | $0.21 | $4.76 | 0x16bb9951… | **Win** (settled Nov 8 4:14 PM) | +$4.24 |
| Nov 7 21:13 | Falcons ML vs Bengals (`aec-nfl-cin-atl-2026-11-08`) | Falcons (short) | 0.3875 | 12 | $0.27 | $4.92 | EdZachary (+0xBc43 token) | **Loss** | −$4.92 |
| Nov 8 14:46 | Hawks ML vs Lakers (`aec-nba-lal-atl-2026-11-09`) | Hawks (short) | 0.420 | 11 | $0.00 | $4.62 | ic4cream | **Loss** (settled Nov 9 6:24 PM) | −$4.62 |
| Nov 8 16:38 | Cal +19.5 vs Houston (`asc-cbb-hou-cah-2026-11-08-neg-19pt5`) | +19.50 (short) | 0.480 | 10 | $0.00 | $4.80 | hi774c | **Win** | +$5.20 |
| Nov 8 16:48 | Ducks ML vs Penguins (`aec-nhl-pit-ana-2026-11-08`) | Ducks (short) | 0.530 | 9 | $0.21 | $4.98 | cocococococo | **Win** | +$4.02 |
| Nov 9 08:42 | Hornets +8.5 vs Cavaliers (`asc-nba-cle-cha-2026-11-09-neg-8pt5`) | +8.50 (short) | 0.510 | 9 | $0.00 | $4.59 | HomeRunHazard | **Win** | +$4.41 |
| Nov 9 09:59 | Hornets +9.5 vs Cavaliers (`asc-nba-cle-cha-2026-11-09-neg-9pt5`) | +9.50 (short) | 0.550 | 9 | $0.00 | $4.95 | HomeRunHazard | **Win** | +$4.05 |
| Nov 9 10:00 | Lakers +2.5 vs Hawks (`asc-nba-lal-atl-2026-11-09-pos-2pt5`) | +2.50 | 0.530 | 9 | $0.00 | $4.77 | HomeRunHazard | **Win** | +$4.23 |
| Nov 9 17:03 | Bills −3.5 vs Vikings (`asc-nfl-buf-min-2026-11-09-neg-3pt5`) | −3.50 | 0.485 | 10 | $0.24 | $5.09 | BreakTheBank | **Win** | +$4.91 |
| Nov 10 10:43 | Canadiens ML vs Wild (`aec-nhl-min-mon-2026-11-10`) | Canadiens (short) | 0.460 | 10 | $0.00 | $4.60 | cocococococo | **Loss** | −$4.60 |
| Nov 10 16:51 | Texas Tech +2.5 vs Illinois (`asc-cbb-ill-txtech-2026-11-10-neg-2pt5`) | +2.50 (short) | 0.510 | 10 | $0.24 | $5.34 | hi774c | **Win** (taker) | +$4.66 |
| Nov 11 01:10 | Predators ML vs Ducks (`aec-nhl-nas-ana-2026-11-11`) | Predators | 0.420 | 24 | $0.00 | $10.08 | royalestake | **Win** | +$13.92 |
| Nov 11 03:44 + 04:07 | Penguins ML vs Sharks (`aec-nhl-pit-sj-2026-11-11`) | Penguins | 0.560 | 18 (8 + 10) | $0.00 | $10.08 | cocococococo | **Win** (settled Nov 11 10:11 PM) | +$7.92 |
| Nov 11 05:26 | Bucks +12.5 vs Lakers (`asc-nba-lal-mil-2026-11-11-neg-12pt5`) | +12.50 (short) | 0.500 | 20 | $0.00 | $10.00 | HomeRunHazard | **Win** | +$10.00 |
| Nov 11 05:29 | Bucks +11.5 vs Lakers (`asc-nba-lal-mil-2026-11-11-neg-11pt5`) | +11.50 (short) | 0.470 | 21 | $0.00 | $9.87 | HomeRunHazard | **Win** | +$11.13 |
| Nov 11 16:47 | Spurs −12.5 vs Bulls (`asc-nba-sa-chi-2026-11-11-neg-12pt5`) | −12.50 | 0.610 | 17 | $0.38 | $10.75 | HomeRunHazard | **Loss** (taker) | −$10.75 |

**Pipeline settled record: 15 wins, 9 losses, net +$32.48 on $155.52 of cost, including $3.89 in fees.**

### Open resting orders (pending, unfilled as of 10:35 PM PT Nov 11)

| Resting since (PT) | Market (US slug) | Side | Rest price | Shares | Wallet copied | Status |
|---|---|---|---|---|---|---|
| Nov 11 22:04 | Giants ML vs Commanders (`aec-nfl-was-nyg-2026-11-12`) | Giants (short) | 0.55 | 18 | 0xBc43 | **Pending** (post-only, expires 5 min before kickoff) |
| Nov 11 22:04 | G2 +1.5 maps vs Team Spirit (`asc-cs2-ts-g2-2026-11-12-hcap-neg-1pt5`) | +1.5 (short) | 0.54 | 18 | vibing123 | **Pending** (post-only, expires 5 min before start) |
| Nov 11 22:34 | Wizards +11.5 vs Pistons (`asc-nba-det-was-2026-11-12-neg-11pt5`) | +11.50 (short) | 0.55 | 18 | HomeRunHazard | **Pending** (post-only, expires 5 min before tip) |

These three are not in the 15-9 record. None had filled as of the snapshot.

Notes:
- The first ten rows were the original off-league / thin-history copies. They were 4-6 after the 49ers −9.5 settled a win (they had been 3-6 with that bet still open in the previous log). All ten would be rejected by the current v3/v4 rules.
- From the Nov 8 specialist copies onward (Hawks, Cal, Ducks, and later), the pipeline is **11-3, net +$54.48**.
- The Spurs −12.5 and Texas Tech +2.5 were taker fills; the rest of the later book was fee-free maker fills at or near the copied entry.
- The account also has two Nov 8 NFL moneylines the owner placed manually, not counted above: Cardinals ML (loss, −$10.00) and Bears ML (win, +$4.03).
