CREATE TABLE IF NOT EXISTS talent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    branch TEXT NOT NULL,
    unit TEXT
);

CREATE TABLE IF NOT EXISTS kigu_player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_code TEXT NOT NULL UNIQUE,
    public_name TEXT NOT NULL,
    region TEXT NOT NULL,
    region_number INTEGER NOT NULL,
    notes TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS social_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    platform TEXT NOT NULL,
    handle TEXT,
    url TEXT,

    FOREIGN KEY (player_id)
        REFERENCES kigu_player(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS kigu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    talent_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    maker TEXT,

    FOREIGN KEY (talent_id)
        REFERENCES talent(id),

    FOREIGN KEY (player_id)
        REFERENCES kigu_player(id)
);

CREATE TABLE IF NOT EXISTS kigu_image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kigu_id INTEGER NOT NULL,
    image_path TEXT,
    source_url TEXT,

    FOREIGN KEY (kigu_id)
        REFERENCES kigu(id)
        ON DELETE CASCADE
);