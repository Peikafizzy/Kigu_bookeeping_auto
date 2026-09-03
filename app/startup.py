from app.database import init_database, seed_talents


def initialize_app():
    init_database()
    seed_talents()