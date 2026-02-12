from __future__ import annotations

import asyncio
from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine


def _comment_sql_statements(
    conn: Any,
    cursor: Any,
    statement: str,
    parameters: Any,
    context: Any,
    executemany: Any,
) -> tuple[str, Any]:
    statement += " -- My comment here"
    print("Modified query:", statement)
    return statement, parameters


async def main() -> None:
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:password@localhost:5432/mydb",
    )
    sa.event.listen(
        engine.sync_engine,
        "before_cursor_execute",
        _comment_sql_statements,
    )

    async with engine.connect() as conn:
        await conn.execute(sa.select(sa.literal(1)))


if __name__ == "__main__":
    asyncio.run(main())
