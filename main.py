from app.database import init_database, seed_talents, get_talents, add_kigu_player, add_social_account, \
    get_talent_by_name, add_appearance, get_player_details, get_kigu_players, deactivate_kigu_player, \
    add_is_active_column


def main():
    init_database()
    seed_talents()
    print("Database rebuilt and talents seeded.")


if __name__ == "__main__":
    main()

