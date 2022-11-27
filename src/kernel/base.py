# Copyright © 2022 @asraelxyz, All Rights Reserved.

import sqlite3

class DataBase:
    """
        Database manager for translations
    """
    
    def __init__(self, database_path):
        self.is_close = False
        self.context = sqlite3.connect(database_path)
        self.cursor = self.context.cursor()

    
    def initialize(self):
        """ Initialise the database if it is not yet ready """
        self.cursor.execute("""
        CREATE TABLE translations (
            "hash" integer NOT NULL,
            "source_lang" varchar(100) NOT NULL,
            "target_lang" varchar(100) NOT NULL,
            "directory" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "source_text" text NOT NULL,
            "target_text" text NOT NULL
        )
        """)

    # def search_all(self):
    #     return self.cursor.execute("""SELECT * FROM translations""").fetchall()

    def search(self, hash_registry, source_lang, target_lang):
        """
            Search only directory, source_text and target_text in the Database
            based on the columns hash_record, source_lang, target_lang.
        """
        search_result = self.cursor.execute("""
            SELECT directory, source_text, target_text FROM translations
            WHERE hash == ? AND source_lang == ? AND target_lang ==  ?
        """, (hash_registry, source_lang, target_lang)).fetchone()

        if search_result is None:
            search_result = (None,) * 3

        return search_result

    
    def add_translation(self, hash_registry, source, target, text, translation):
        """
            Add a new translation to the translation database.
        """
        self.cursor.execute(
            """INSERT INTO translations VALUES (?, ?, ?, NULL, ?, ?)""",
            (hash_registry, source, target, text, translation)
        )

        self.context.commit()

    def __enter__(self):
        return self

    def __del__(self):
        if not self.is_close:
            self.context.close()

    def __exit__(self, _0, _1, _2):
        if not self.is_close:
            self.context.close()
