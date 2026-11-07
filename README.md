# Polymarket Sports Bettor MCP

MCP server for discovering and monitoring high-quality sports bettors on Polymarket. Designed for conversational querying (Claude, Cursor, Grok, etc.).

Primary focus: **football (NFL / CFB)** copy-trading of consistent specialists, with support for other major sports when needed.

## Tools

| Tool | Description |
|------|-------------|
| `get_sport_copy_candidates` | **Main tool** — finds consistent specialists who have open positions on today's games in a given sport and shows which side they're on. Football is the default. |
| `get_sports_candidates` | Ranked sports wallets filtered to prefer discretionary bettors over market makers |
| `get_wallet_positions` | Open positions for a specific wallet |
| `get_sports_leaderboard` | Raw sports leaderboard (no filtering) |

## Setup

```bash
# Clone
git clone https://github.com/maxraulugarte-a11y/polymarket-sports-mcp.git
cd polymarket-sports-mcp

# Install
pip install -r requirements.txt

# Run (stdio)
python src/server.py
```

## Claude Desktop / Cursor config

```json
{
  "mcpServers": {
    "polymarket-sports": {
      "command": "python",
      "args": ["/absolute/path/to/polymarket-sports-mcp/src/server.py"]
    }
  }
}
```

## Example queries

- "What positions can I copy from consistent specialists on today's football games?"
- "Show me NBA copy candidates for tonight"
- "Which specialists have sides on EPL today?"
- "Get NFL copy candidates for tomorrow"
- "Show me March Madness copy candidates"
- "What positions can I copy on today's golf?"

## Supported sports

- `football` (default — NFL + CFB)
- `nfl`, `cfb`
- `nba`, `cbb`, `basketball`, `college basketball`, `march madness`
- `mlb`, `nhl`
- `epl`, `mls`, `soccer`
- `ufc`, `mma`
- `pga`, `liv`, `golf`
- `baseball`, `hockey`

## Notes

- Filters use volume-to-PnL ratio to deprioritize likely market makers (default max ratio 40 for the copy tool).
- All data comes from Polymarket's public Data API v2 + Gamma API — no auth required for these tools.
- Slippage and delay will reduce edge when copying. Start small.
- Series IDs are current as of November 2026 and may change over time.
