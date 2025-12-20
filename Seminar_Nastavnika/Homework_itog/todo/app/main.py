from fastapi import FastAPI, HTTPException, Response
from .database import get_connection, init_db
from .schemas import ItemCreate, ItemUpdate, ItemOut
from datetime import datetime

app = FastAPI(title="TODO Service")

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/items", response_model=ItemOut)
def create_item(item: ItemCreate):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO todos (title, description, completed)
            VALUES (?, ?, ?)
            """,
            (item.title, item.description, False)
        )

        item_id = cursor.lastrowid

        row = conn.execute("SELECT * FROM todos WHERE id = ?", (item_id,)).fetchone()

    return map_row_to_item(row)

@app.get("/items", response_model=list[ItemOut])
def get_items():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, description, completed, created_at FROM todos"
        )
        rows = cursor.fetchall()

    return [
        map_row_to_item(row)
        for row in rows
    ]

@app.get("/items/search", response_model=list[ItemOut])
def search_items(q: str):
    query = f"%{q}%"
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM todos WHERE title LIKE ?",
            (query,)
        ).fetchall()
    return [map_row_to_item(row) for row in rows]

@app.get("/items/status", response_model=list[ItemOut])
def get_items_by_status(completed: bool):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM todos WHERE completed = ? ORDER BY created_at DESC",
            (completed,)
        ).fetchall()
    return [map_row_to_item(row) for row in rows]

@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, description, completed, created_at FROM todos WHERE id = ?",
            (item_id,)
        )
        row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Item not found")

    return map_row_to_item(row)


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (item_id,))

    return Response(status_code=204)

@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemUpdate):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE todos
            SET
                title = COALESCE(?, title),
                description = COALESCE(?, description),
                completed = COALESCE(?, completed)
            WHERE id = ?
            """,
            (
                item.title,
                item.description,
                item.completed,
                item_id,
            )
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")

        row = conn.execute("SELECT * FROM todos WHERE id = ?", (item_id,)).fetchone()

    return map_row_to_item(row)

def map_row_to_item(row) -> ItemOut:
    return ItemOut(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        completed=bool(row["completed"]),
        created_at=row["created_at"],
    )
