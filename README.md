# Polymarket Sports Bettor MCP

MCP server for discovering and monitoring high-quality sports bettors on Polymarket. Designed for conversational querying (Claude, Cursor, Grok, etc.).

Primary focus: **football (NFL / CFB)** copy-trading of consistent specialists.

## Tools

| Tool | Description |
|------|-------------|
| `get_football_copy_candidates` | **Main tool** — finds consistent specialists who have open positions on today's NFL/CFB games and shows which side they're on |
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
- "Show me NFL copy candidates for tomorrow"
- "Which specialists have sides on CFB today?"
- "Show me the best sports bettors to copy this month"
- "What positions does BreakTheBank have open?"

## Notes

- Filters use volume-to-PnL ratio to deprioritize likely market makers (default max ratio 40 for the football tool).
- All data comes from Polymarket's public Data API v2 + Gamma API — no auth required for these tools.
- Slippage and delay will reduce edge when copying. Start small.
- Series IDs for NFL (10187) and CFB (10210) are used; these can change over time.
