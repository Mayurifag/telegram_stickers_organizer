from tinydb import TinyDB, Query

db = TinyDB("sticker_sets.json")
sticker_sets_table = db.table("sticker_sets")


def db_save_sticker_set(user_id: int, set_name: str, title: str):
    sticker_sets_table.upsert(
        {"user_id": user_id, "set_name": set_name, "title": title},
        Query().set_name == set_name,
    )


def db_get_sticker_set(set_name: str):
    return sticker_sets_table.get(Query().set_name == set_name)


def db_get_user_sticker_sets(user_id: int):
    return sticker_sets_table.search(Query().user_id == user_id)
