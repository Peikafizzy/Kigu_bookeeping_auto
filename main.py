from app.database import init_database, seed_talents, get_talents, add_kigu_player, add_social_account, \
    get_talent_by_name, add_appearance, get_player_details


def main():
    init_database()
    seed_talents()

    details = get_player_details()

    for row in details:
        print(
            row["player_code"],
            "|",
            row["public_name"],
            "|",
            row["region"],
            "|",
            row["maker"],
            "| Talent:",
            row["talent_name"],
            "|",
            row["branch"],
            row["unit"],
            "|",
            row["platform"],
            row["handle"],
            row["url"]
        )


if __name__ == "__main__":
    main()

