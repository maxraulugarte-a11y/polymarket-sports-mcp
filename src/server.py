#!/usr/bin/env python3
"""
Polymarket Sports Bettor MCP Server
Tools for discovering and monitoring high-quality sports bettors on Polymarket.
Focused on football (NFL / CFB) copy-trading of consistent specialists.
"""

import asyncio
import json
from datetime import datetime, timezone, timedelta
from typing import Any

import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("polymarket-sports-mcp")

BASE_URL = "https://data-api.polymarket.com/v2"
GAMMA_URL = "https://gamma-api.polymarket.com"


def get_leaderboard(category: str = "sports", time_period: str = "month",
                    sort_by: str = "PNL", limit: int = 50) -> list[dict[str, Any]]:
    url = f"{BASE_URL}/leaderboard"
    params = {
        "category": category,
        "time_period": time_period,
        "sort_by": sort_by,
        "limit": limit,
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("data", [])


def get_positions(user: str, limit: int = 30) -> list[dict[str, Any]]:
    url = f"{BASE_URL}/positions"
    params = {"user": user, "limit": limit, "status": "OPEN"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("data", [])


def filter_candidates(traders: list[dict[str, Any]]) -> list[dict[str, Any]]:
    filtered = []
    for t in traders:
        pnl = t.get("pnl", 0) or 0
        volume = t.get("volume", 0) or 0
        if pnl <= 0:
            continue
        ratio = volume / pnl if pnl > 0 else float("inf")
        is_likely_mm = ratio > 50
        score = pnl / (1 + ratio / 20)
        filtered.append({
            "rank": t.get("rank"),
            "user_id": t.get("user_id"),
            "name": t.get("user_name") or (t.get("user_id", "")[:10] + "..."),
            "pnl": pnl,
            "volume": volume,
            "ratio": round(ratio, 1),
            "likely_mm": is_likely_mm,
            "score": round(score, 0),
            "verified": t.get("verified", False),
            "x_username": t.get("x_username", ""),
        })
    filtered.sort(key=lambda x: x["score"], reverse=True)
    return filtered


def get_todays_football_events(league: str = "both", date_str: str | None = None) -> list[dict[str, Any]]:
    """Fetch NFL and/or CFB events for a given date (defaults to today UTC)."""
    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    series_map = {
        "nfl": "10187",
        "cfb": "10210",
    }
    leagues = []
    if league in ("nfl", "both"):
        leagues.append(("NFL", series_map["nfl"]))
    if league in ("cfb", "both"):
        leagues.append(("CFB", series_map["cfb"]))

    events = []
    for league_name, series_id in leagues:
        try:
            r = requests.get(
                f"{GAMMA_URL}/events",
                params={
                    "series_id": series_id,
                    "active": "true",
                    "closed": "false",
                    "limit": 50,
                },
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            for ev in data:
                end = ev.get("endDate", "") or ""
                start = ev.get("startDate", "") or ""
                title = ev.get("title", "") or ""
                if date_str in end or date_str in start or date_str in title:
                    events.append({
                        "league": league_name,
                        "id": ev.get("id"),
                        "title": title,
                        "slug": ev.get("slug"),
                        "endDate": end,
                        "markets": [
                            {
                                "question": m.get("question"),
                                "conditionId": m.get("conditionId"),
                                "slug": m.get("slug"),
                                "sportsMarketType": m.get("sportsMarketType"),
                            }
                            for m in (ev.get("markets") or [])[:8]
                        ],
                    })
        except Exception:
            continue
    return events


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_sports_candidates",
            description="Get ranked sports bettor candidates from Polymarket, filtered to prefer discretionary wallets over market makers. Returns top wallets by quality score.",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_period": {
                        "type": "string",
                        "enum": ["day", "week", "month", "all"],
                        "description": "Time window for the leaderboard",
                        "default": "month",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "How many candidates to return after filtering",
                        "default": 15,
                        "minimum": 1,
                        "maximum": 50,
                    },
                    "include_mm": {
                        "type": "boolean",
                        "description": "Include likely market makers in results",
                        "default": False,
                    },
                },
            },
        ),
        Tool(
            name="get_wallet_positions",
            description="Get open positions for a specific Polymarket wallet. Useful for seeing what top sports bettors are currently holding.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "Wallet address (user_id from leaderboard)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max positions to return",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50,
                    },
                    "sports_only": {
                        "type": "boolean",
                        "description": "Prefer sports-related positions when possible",
                        "default": True,
                    },
                },
                "required": ["user_id"],
            },
        ),
        Tool(
            name="get_sports_leaderboard",
            description="Raw sports leaderboard from Polymarket Data API (no filtering).",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_period": {
                        "type": "string",
                        "enum": ["day", "week", "month", "all"],
                        "default": "month",
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["PNL", "VOLUME"],
                        "default": "PNL",
                    },
                    "limit": {
                        "type": "integer",
                        "default": 25,
                        "minimum": 1,
                        "maximum": 100,
                    },
                },
            },
        ),
        Tool(
            name="get_football_copy_candidates",
            description="Find consistent sports specialists (not market makers) who have open positions on today's NFL or CFB games. Returns the game, the side they're on, and their size so you know what is copyable.",
            inputSchema={
                "type": "object",
                "properties": {
                    "league": {
                        "type": "string",
                        "enum": ["nfl", "cfb", "both"],
                        "description": "Which football league to look at",
                        "default": "both",
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD (UTC). Defaults to today.",
                    },
                    "time_period": {
                        "type": "string",
                        "enum": ["day", "week", "month", "all"],
                        "description": "Leaderboard window for ranking specialists",
                        "default": "month",
                    },
                    "max_wallets": {
                        "type": "integer",
                        "description": "How many top non-MM specialists to check",
                        "default": 12,
                        "minimum": 3,
                        "maximum": 25,
                    },
                    "max_ratio": {
                        "type": "number",
                        "description": "Maximum volume/PnL ratio to consider a specialist (lower = more selective)",
                        "default": 40,
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    try:
        if name == "get_sports_candidates":
            time_period = arguments.get("time_period", "month")
            limit = arguments.get("limit", 15)
            include_mm = arguments.get("include_mm", False)
            raw = get_leaderboard(time_period=time_period, limit=50)
            candidates = filter_candidates(raw)
            if not include_mm:
                candidates = [c for c in candidates if not c["likely_mm"]]
            result = candidates[:limit]
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_wallet_positions":
            user_id = arguments["user_id"]
            limit = arguments.get("limit", 10)
            sports_only = arguments.get("sports_only", True)
            positions = get_positions(user_id, limit=max(limit * 2, 20))
            if sports_only:
                sports = [
                    p for p in positions
                    if any(kw in (p.get("title", "") + " " + p.get("event_slug", "")).lower()
                           for kw in ["nfl", "nba", "mlb", "nhl", "soccer", "football", "basketball", "sport", "premier", "la liga", "serie a", "bundesliga", "cfb", "college"])
                ]
                positions = sports or positions
            simplified = []
            for p in positions[:limit]:
                simplified.append({
                    "title": p.get("title"),
                    "outcome": p.get("outcome"),
                    "size": p.get("current_size"),
                    "avg_price": p.get("avg_price"),
                    "current_price": p.get("current_price"),
                    "status": p.get("status"),
                    "condition_id": p.get("condition_id"),
                })
            return [TextContent(type="text", text=json.dumps(simplified, indent=2))]

        elif name == "get_sports_leaderboard":
            time_period = arguments.get("time_period", "month")
            sort_by = arguments.get("sort_by", "PNL")
            limit = arguments.get("limit", 25)
            raw = get_leaderboard(time_period=time_period, sort_by=sort_by, limit=limit)
            return [TextContent(type="text", text=json.dumps(raw, indent=2))]

        elif name == "get_football_copy_candidates":
            league = arguments.get("league", "both")
            date = arguments.get("date")
            time_period = arguments.get("time_period", "month")
            max_wallets = arguments.get("max_wallets", 12)
            max_ratio = arguments.get("max_ratio", 40)

            events = get_todays_football_events(league=league, date_str=date)
            if not events:
                return [TextContent(type="text", text=json.dumps({
                    "message": "No football events found for the selected date/league.",
                    "date": date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "league": league,
                }, indent=2))]

            raw = get_leaderboard(time_period=time_period, limit=40)
            candidates = filter_candidates(raw)
            specialists = [c for c in candidates if not c["likely_mm"] and c["ratio"] <= max_ratio][:max_wallets]

            event_keywords = []
            for ev in events:
                title_lower = (ev["title"] or "").lower()
                parts = [p.strip() for p in title_lower.replace(" vs. ", " vs ").replace(" vs ", "|").split("|") if p.strip()]
                event_keywords.append({
                    "event": ev["title"],
                    "league": ev["league"],
                    "keywords": parts + [ev["slug"] or ""],
                })

            results = []
            for spec in specialists:
                positions = get_positions(spec["user_id"], limit=25)
                relevant = []
                for pos in positions:
                    title = (pos.get("title") or "").lower()
                    slug = (pos.get("event_slug") or "").lower()
                    for ek in event_keywords:
                        if any(kw and (kw in title or kw in slug) for kw in ek["keywords"]):
                            relevant.append({
                                "game": ek["event"],
                                "league": ek["league"],
                                "title": pos.get("title"),
                                "outcome": pos.get("outcome"),
                                "size": pos.get("current_size"),
                                "avg_price": pos.get("avg_price"),
                                "current_price": pos.get("current_price"),
                                "condition_id": pos.get("condition_id"),
                            })
                            break
                if relevant:
                    results.append({
                        "wallet": spec["name"],
                        "user_id": spec["user_id"],
                        "monthly_pnl": spec["pnl"],
                        "vol_pnl_ratio": spec["ratio"],
                        "positions_today": relevant,
                    })

            return [TextContent(type="text", text=json.dumps({
                "date": date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "league": league,
                "events_found": len(events),
                "specialists_checked": len(specialists),
                "specialists_with_positions": results,
            }, indent=2))]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
