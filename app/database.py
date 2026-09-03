import sqlite3
from pathlib import Path

from app.seed_talents import TALENTS

DB_PATH = Path("data/kigu.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn

if __name__ == "__main__":
    conn = get_connection()
    print("Connected to:", DB_PATH)
    conn.close()

def init_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS talent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                branch TEXT NOT NULL,
                unit TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS kigu_player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_code TEXT NOT NULL UNIQUE,
                public_name TEXT NOT NULL,
                region TEXT NOT NULL,
                maker TEXT,
                notes TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS social_account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                platform TEXT NOT NULL,
                handle TEXT,
                url TEXT,

                FOREIGN KEY (player_id)
                    REFERENCES kigu_player(id)
                    ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS appearance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                talent_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,

                FOREIGN KEY (talent_id)
                    REFERENCES talent(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (player_id)
                    REFERENCES kigu_player(id)
                    ON DELETE CASCADE,

                UNIQUE (talent_id, player_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS appearance_image (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                appearance_id INTEGER NOT NULL,
                image_path TEXT,
                source_url TEXT,

                FOREIGN KEY (appearance_id)
                    REFERENCES appearance(id)
                    ON DELETE CASCADE
            )
        """)

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn

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
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO kigu_player (
                player_code,
                public_name,
                region,
                maker,
                notes
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (player_code, public_name, region, maker, notes)
        )

        return cursor.lastrowid


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