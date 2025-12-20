from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from datetime import datetime
import random
import string

from .database import get_connection, init_db
from .schemas import URLCreate, URLShortenResponse, URLStats

app = FastAPI(title="Short URL Service")

@app.on_event("startup")
def startup():
    init_db()

@app.post("/shorten", response_model=URLShortenResponse)
def shorten_url(data: URLCreate, request: Request):
    short_id = generate_short_id()

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO urls (short_id, full_url) VALUES (?, ?)",
            (short_id, data.url)
        )

    base_url = str(request.base_url).rstrip("/")
    return URLShortenResponse(
        short_id=short_id,
        short_url=f"{base_url}/{short_id}"
    )


@app.get("/{short_id}")
def redirect(short_id: str):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT full_url, visits FROM urls WHERE short_id = ?",
            (short_id,)
        ).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Short URL not found")

        full_url, visits = row
        conn.execute(
            "UPDATE urls SET visits = ? WHERE short_id = ?",
            (visits + 1, short_id)
        )

    return RedirectResponse(url=full_url)


@app.get("/stats/{short_id}", response_model=URLStats)
def get_stats(short_id: str):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT short_id, full_url, visits, created_at FROM urls WHERE short_id = ?",
            (short_id,)
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return map_row_to_url(row)

@app.get("/urls/popular", response_model=list[URLStats])
def popular_urls(limit: int = 10):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM urls ORDER BY visits DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [map_row_to_url(row) for row in rows]

def generate_short_id(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def map_row_to_url(row) -> URLStats:
    return URLStats(
        short_id=row["short_id"],
        full_url=row["full_url"],
        visits=row["visits"],
        created_at=row["created_at"]
    )
