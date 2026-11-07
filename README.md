# Polymarket Sports Bettor MCP

MCP server for discovering and monitoring high-quality sports bettors on Polymarket. Designed for conversational querying (Claude, Cursor, Grok, etc.).

## Tools

| Tool | Description |
|------|-------------|
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

- "Show me the best sports bettors to copy this month"
- "What positions does BreakTheBank have open?"
- "Get the raw monthly sports leaderboard sorted by volume"

## Notes

- Filters use volume-to-PnL ratio to deprioritize likely market makers (ratio > 50).
- All data comes from Polymarket's public Data API v2 — no auth required for these tools.
- Slippage and delay will reduce edge when copying. Start small.
