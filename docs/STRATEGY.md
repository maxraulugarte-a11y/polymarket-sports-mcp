# Copy-trading strategy: Polymarket sports specialists → Polymarket US

This document stands on its own, so another LLM or a person can follow how picks are made. Last updated 2026-11-12 (pipeline v4: fresh rankings, manual-trial overrides, conditional-edge analysis; HomeRunHazard NBA-spread rule; $10 flat stakes). Code lives outside this repo in the operator's workspace. The rules here are the spec.

## Goal
Copy pre-game sports bets that **reliably profitable specialist wallets** on global Polymarket hold, and place small bets (about $10) on the matching **Polymarket US** market. A human approves every pick before it is placed.

## 1. Data sources (global Polymarket, public, no key)
| Purpose | Endpoint |
|---|---|
| Candidate pool | `GET https://data-api.polymarket.com/v2/leaderboard?category=<sports or esports>&timePeriod=<DAY, WEEK, MONTH or ALL>&limit=50` (paginate with `cursor` only; `offset` is rejected and `window=` is silently ignored, which returns the DAY board) |
| Wallet history | `GET https://data-api.polymarket.com/v2/activity?user=<wallet>&limit=500&cursor=` (TRADE, SPLIT, MERGE, REDEEM; we cap at 30k-90k records) |
| Open positions | `GET https://data-api.polymarket.com/v2/positions?user=<wallet>&status=OPEN&limit=500` (fields `event_slug`, `slug`, `condition_id`, `token_id`, `opposite_token_id`, `outcome`, `avg_price`, `current_size`, `current_price`) |
| Market metadata and resolution | `GET https://gamma-api.polymarket.com/events?slug=<event_slug>` (`markets[].conditionId`, `outcomes`, `outcomePrices`, `clobTokenIds`, `gameStartTime`, `sportsMarketType`, `closed`) |
| Closing price (CLV) | `GET https://clob.polymarket.com/prices-history?market=<token>&startTs=&endTs=&fidelity=5` (last price before kickoff) |

**Game events** are slugs that match `^<league>-<team>-<team>-YYYY-MM-DD(-suffix)?$`. Examples: `nfl-tb-chi-2026-11-09`, `cfb-ala-lsu-2026-11-07`.

**A bet** is one wallet in one market. It is summarized by:
- the main outcome bought
- total stake
- average entry price
- the first-buy timestamp, which makes it pre-game if earlier than `gameStartTime`
- whether the wallet sold it before settlement (more than 10% sold counts as not held)
- whether the wallet also bought the other side or split (two-sided)
- the settled result from Gamma `outcomePrices`. A push counts as 0.5.

## 2. Mapping to Polymarket US
The SDK is `polymarket_us.PolymarketUS(key_id, secret_key)`, with keys only in env vars. Event slugs are the same on both sites, with one important exception below.
- **Moneyline / winner:** the global market slug equals the event slug, and the US slug is `aec-<event>`. Outcome index 0 (the away team, listed first on both sites) is `ORDER_INTENT_BUY_LONG`, and index 1 is `ORDER_INTENT_BUY_SHORT`.
- **Spread:** global `<event>-spread-home|away-<X>pt5` maps to US `asc-<event>-pos|neg-<X>pt5`. Match the outcome by team name or by the signed line. US order previews report spread outcomes as the signed line, for example `+6.50`.
- **Total:** global `<event>-total-<X>pt5` maps to US `tsc-<event>-total-<X>pt5`, where index 0 is Over (LONG). Spreads and totals copy **only if the exact same line** exists on US.
- **Soccer 3-way legs:** `atc-<global market slug>`, Yes = LONG.
- **UTC vs. local date fix:** global slugs carry the **UTC** date, while Polymarket US uses the **local game date**. Games starting after about 4-5 PM PT (most NBA/NHL games, SNF/MNF) sit under **date − 1** on US. For example, global `nfl-tb-chi-2026-11-09` is US `nfl-tb-chi-2026-11-08`. Try the global slug first, then date − 1.
- **Price convention:** US limit prices are always in **LONG terms**. To buy the short side at price q, send `intent=BUY_SHORT, price = 1 − q`.
- **Tick:** respect the market's `orderPriceMinTickSize` (often 0.0025 or 0.01). Preview accepts off-tick prices, but create can reject them.
- **Quotes:** `markets.bbo(slug)` gives bestBid and bestAsk in LONG terms. For the short side, ask = 1 − bestBid and bid = 1 − bestAsk.

## 3. Wallet and segment selection (v3 core + v4 ranking)
We compute all numbers ourselves from settled history. **Leaderboard ROI is never used.**

**Core wallet filter (v3):**
- ≥ 100 settled game bets (stake ≥ $10)
- own all-history $ROI (PnL ÷ cost) ≥ 0
- held to settlement ≥ 70%
- ≥ 50% of stake in one league
- < 30% two-sided markets
- first activity ≥ 60 days ago
- mean CLV > 0 over ≥ 30 sampled pre-game bets

**Segment** = wallet × (league, bet type). Clean bets are pre-game, held, and priced 0.05-0.95. Each segment gets a **credibility score**:
- raw `m = mean(res/entry − 1)` and variance `v = Σ((1−p)/p)/n²`
- prior `μ`, `τ²` from method of moments across all segments with ≥ 30 clean bets (2026-11-12: μ = +0.21%, τ² = 0.0063 over 1,382 segments; 2026-11-08 was μ = −0.18%, τ² = 0.0036 over 928)
- `score = μ + τ²/(τ²+v)·(m − μ)`

**Tiers:**
- **keep:** core wallet, segment in its main league, segment flat ROI > 0 over ≥ 30 bets, not a total, score > 0
- **watch** (lower confidence): score > 0 over ≥ 100 clean bets, not a total, hold ≥ 70%, two-sided < 30%, age ≥ 60 days, own ROI ≥ 0
- everything else is **drop**. Dropped wallets go on a suppression list and are rechecked after 30 days. Keep/watch wallets are re-profiled weekly.

**Weekly refresh (rebuilt 2026-11-12 after the Nov 9 refresh failed on a stale cache and Cloudflare 1015 rate limits):**
- one shared throttle per host (data API ≈ 4 requests/s), with exponential backoff plus jitter on 429/1015/5xx that pauses every thread
- incremental activity: only pages newer than the cached history are downloaded and merged; new wallets checkpoint every page to a `.part` file
- a per-wallet manifest makes every stage resumable; a wallet that fails is marked **stale** and listed in `rankings.json` (`stale_wallets`) instead of silently reusing old data
- unsettled cached events are re-fetched so newly settled games count; CLV samples up to 80 pre-game bets per wallet
- the pool grows by about 60 new leaderboard wallets per week from a prioritized backlog

**Pick rule** (for an open position of a keep/watch wallet):
- in an allowed segment, not a total
- position stake ≥ $100 and ≥ 0.5x the wallet's median stake (no token positions)
- wallet average entry 0.40-0.85 (no longshots)
- game not started, and the exact US market exists
- no keep/watch wallet holds the opposite outcome

**Manual overrides** (`data/manual_overrides.json`, applied after scoring on every refresh, so they persist):
- **ianf2026 and chongchong37, NBA spreads: forced to watch as a "manual trial"** (added 2026-11-12 at the user's request, review after 2026-12-12). Both show about +20-35% flat ROI on NBA spreads near even odds, but on fewer than 100 bets and under 60 days of history, so the rules alone would drop them. Rows keep `computed_status` (what the rules said) next to the forced `status`.
- **HomeRunHazard, NBA spreads:** special rule below, which replaces the generic pick rule for him.

**Conditional edges** (`data/conditional_edges.md`): for every keep/watch segment and every segment with ≥ 50 clean bets, stats by bet size relative to the wallet's median stake and by price band. **The headline is the 40-60c band**, because near-even-odds edge is what we want to copy. A high win rate on 70c+ favourites counts only if ROI is clearly positive.

**HomeRunHazard NBA spreads (override):** copy **only his single largest NBA spread** on a game, and only when that position is at least **1.2× his usual size** (the median of the larger side of his NBA spread markets). Rest a fee-free maker order at or below his average entry. **Never mirror his full two-sided book.** He holds opposite-team spreads or moneylines on essentially every game (arbs and middles); those extra legs are not a one-way opinion we can copy in full, and a full mirror as a taker lost money in the backtest (see BACKTEST.md).

Picks are sorted keep-first, then by score. A second agreeing wallet is shown but **is not required**, and token-sized second wallets never count.

## 4. Stake sizing
- Base stake is now **about $10** per pick (raised from $5).
- Conviction scaling `stake = clamp(10·√(their stake / their median stake), $6, $24)` would apply **only to proven sizers**. A proven sizer meets all of these: Spearman(size multiple, z = (res − p)/√(p(1−p))) > 0 with p < 0.001, ≥ 200 clean bets, ROI on above-median-size bets > below-median, and stake-weighted ROI > flat ROI.
- As of 2026-11-11 **no wallet qualifies**, so every pick is about $10 flat. Out of sample, bet size showed no relationship with outcome (see BACKTEST.md). HomeRunHazard's own dollar-weighted NBA book also lagged an equal $10/game copy, which is another reason to keep stakes flat.
- **Daily exposure cap:** 25% of current buying power.

## 5. Execution
- **Default: resting maker order.** Send a limit at `floor_to_tick(min(trader's avg entry, US ask − tick))` with `participateDontInitiate=true` (post-only) and `tif=TIME_IN_FORCE_GOOD_TILL_DATE`, where `goodTillTime` = kickoff − 5 min. `GOOD_TILL_CANCEL` is the fallback, followed by a cancel sweep before kickoff. Maker fee is 0 bps.
- **Taker fallback:** if a resting order is unfilled near kickoff, show the user the current ask and fee. Take the price only with the user's explicit OK, using an IOC limit at the ask.
- Before every create, run `orders.preview` and check that the returned `marketMetadata.outcome` matches the intended side.
- Every pick needs explicit human approval. Never commit keys or account IDs.

## 6. Fees
The Polymarket US taker fee per fill is **0.095 × contracts × p × (1 − p)**, about 4.75% of stake at p = 0.50 (around $0.48 on a $10 bet, or $0.24 on a $5 bet). Resting maker fills are free. The backtests model taker copies at entry + 1¢ slippage plus this fee.

## 7. Known pitfalls (all hit in practice)
- **Leaderboard ROI is a short rolling window, not all-time.** It swung from +19% to −24% overnight for one wallet. Compute ROI from settled history yourself.
- **Unredeemed losers show as OPEN at price ≈ 0.** A position endpoint's "open" bets include dead losing positions. Filter `0.02 < current_price < 0.98`, and value history at Gamma resolution, not by redemptions. Otherwise ROI is badly overstated.
- **Token second-wallet "consensus."** A second wallet holding $300 (0.1x its median) is not agreement. Require ≥ 0.5x median and ≥ $100.
- **Off-league copying.** A wallet that is good at MLB is not good at NFL spreads. Copy only inside the segment with the proven record. Our first 8 settled picks (2-6) were all off-league, except Fresno, which came from a 3-week-old wallet.
- **UTC date slugs.** Without the date − 1 fallback, most NBA/NHL/night games fail to map.
- **Short-sample hot streaks.** +20-40% over fewer than 100 bets is mostly noise. Shrinkage turns +16% over 600 bets into about +7%.
- **Fees dominate.** As a group these wallets have about 0% edge at their own prices, so taker copying loses about 6-7%.
- **Preview ≠ create.** Preview doesn't validate the tick size. Round to the tick before creating.

## 8. Honest expectation
In the walk-forward backtest, v4 picks earned about **+5.5% ± 2.1 if resting orders fill at the trader's price** (an upper bound) and **−0.8% ± 2.1 as taker**, over 1,973 copies in 23 weeks. That is not proven profitable.

The HomeRunHazard NBA-spread study (236 settled games, Oct 3 – Nov 11) is more encouraging **at his prices**: a full mirror was +4.3% and biggest-spread-only was +13.8%, and both 90% bootstrap ranges stayed positive. As a taker, the full mirror lost money. Live copies should rest as makers on the single largest spread, not take his whole book. Keep tracking results in TRADE_LOG.md.
