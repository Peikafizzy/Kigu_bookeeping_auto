import sqlite3
from pathlib import Path

from app.seed_talents import TALENTS

DB_PATH = Path("data/kigu.db")
SCHEMA_PATH = Path("app/schema.sql")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

def init_database():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection() as conn:
        conn.executescript(schema)

if __name__ == "__main__":
    conn = get_connection()
    print("Connected to:", DB_PATH)
    conn.close()

def add_talent(name, branch, unit):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO talent (name, branch, unit)
            VALUES (?, ?, ?)
            """,
            (name, branch, unit)
        )


def get_talents():
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, name, branch, unit
            FROM talent
            ORDER BY id
            """
        ).fetchall()

def seed_talents():
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO talent (name, branch, unit)
            VALUES (?, ?, ?)
            """,
            TALENTS
        )

def add_kigu_player(player_code, public_name, region, maker=None, notes=None):
    player_code, region_number = generate_player_code(region)

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO kigu_player (player_code,
                                     public_name,
                                     region,
                                     region_number,
                                     maker,
                                     notes,
                                     is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
            (
                player_code,
                public_name,
                region,
                region_number,
                maker,
                notes
            )
        )

        return cursor.lastrowid, player_code

def add_social_account(player_id, platform, handle, url):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO social_account (
                player_id,
                platform,
                handle,
                url
            )
            VALUES (?, ?, ?, ?)
            """,
            (player_id, platform, handle, url)
        )


def add_appearance(player_id, talent_id):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO appearance (
                talent_id,
                player_id
            )
            VALUES (?, ?)
            """,
            (talent_id, player_id)
        )

def get_talent_by_name(name):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, name, branch, unit
            FROM talent
            WHERE name = ?
            """,
            (name,)
        ).fetchone()

def get_player_details():
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT
                kp.player_code,
                kp.public_name,
                kp.region,
                kp.maker,

                t.name AS talent_name,
                t.branch,
                t.unit,

                sa.platform,
                sa.handle,
                sa.url

            FROM kigu_player kp

            LEFT JOIN appearance a
                ON kp.id = a.player_id

            LEFT JOIN talent t
                ON a.talent_id = t.id

            LEFT JOIN social_account sa
                ON kp.id = sa.player_id

            ORDER BY kp.id
            """
        ).fetchall()

def generate_player_code(region):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT MAX(region_number) AS max_number
            FROM kigu_player
            WHERE region = ?
            """,
            (region,)
        ).fetchone()

        next_number = (row["max_number"] or 0) + 1

        return f"{region}{next_number:04d}", next_number

def deactivate_kigu_player(player_id):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE kigu_player
            SET is_active = 0
            WHERE id = ?
            """,
            (player_id,)
        )

def reactivate_kigu_player(player_id):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE kigu_player
            SET is_active = 1
            WHERE id = ?
            """,
            (player_id,)
        )

def get_kigu_players():
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT *
            FROM kigu_player
            WHERE is_active = 1
            ORDER BY id
            """
        ).fetchall()

def add_is_active_column():
    with get_connection() as conn:
        conn.execute("""
            ALTER TABLE kigu_player
            ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1
        """)

def generate_player_code(region):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT MAX(region_number) AS max_number
            FROM kigu_player
            WHERE region = ?
            """,
            (region,)
        ).fetchone()

        next_number = (row["max_number"] or 0) + 1

        player_code = f"{region}{next_number:04d}"

        return player_code, next_number