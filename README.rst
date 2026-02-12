This repository was made to demonstrate an issue with SQLAlchemy async engine
query modification, the issue being that ``before_cursor_execute`` events are
correctly run, but the result is ignored (whereas the result should be
used instead of the original serialized comment).

Output of the script::

    Modified query: SELECT $1::INTEGER AS anon_1 -- My comment here

Relevant logs on the PostgreSQL side::

    2026-02-12 20:39:55.982 UTC [1] LOG:  database system is ready to accept connections
    2026-02-12 20:40:06.876 UTC [69] LOG:  statement: BEGIN;
    2026-02-12 20:40:06.877 UTC [69] LOG:  execute __asyncpg_stmt_1__: select pg_catalog.version()
    2026-02-12 20:40:06.878 UTC [69] LOG:  execute __asyncpg_stmt_2__: select current_schema()
    2026-02-12 20:40:06.879 UTC [69] LOG:  execute __asyncpg_stmt_3__: show transaction isolation level
    2026-02-12 20:40:06.879 UTC [69] LOG:  execute __asyncpg_stmt_4__: show standard_conforming_strings
    2026-02-12 20:40:06.879 UTC [69] LOG:  statement: ROLLBACK;
    2026-02-12 20:40:06.881 UTC [69] LOG:  statement: BEGIN;
    2026-02-12 20:40:06.881 UTC [69] LOG:  execute __asyncpg_stmt_5__: SELECT $1::INTEGER AS anon_1
    2026-02-12 20:40:06.881 UTC [69] DETAIL:  Parameters: $1 = '1'
    2026-02-12 20:40:06.881 UTC [69] LOG:  statement: ROLLBACK;

Notice the missing comment at the end of the query on the PostgreSQL side.
This also occurs with the MySQL+aiomysql combo, unfortunately.

If you want to run this, here are a few commands::

    # In a first terminal window, run the PostgreSQL database with the
    # correct options. It will run on ``localhost:5432``.
    docker compose run

    # In a second terminal window, install poetry>=2.2.1 via your native
    # package manager or pip, then:
    poetry install
    poetry run python poc.py
