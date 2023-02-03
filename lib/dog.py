import sqlite3
import ipdb

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    all = []

    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id integer PRIMARY KEY,
                name text,
                breed text
            )
        """
        CURSOR.execute(sql)


    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed) 
            VALUES(?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        # ipdb.set_trace()
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(dog) for dog in all]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            where name = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        # ipdb.set_trace()
        return cls.new_from_db(dog) if dog else None

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            where id = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        # ipdb.set_trace()
        return cls.new_from_db(dog)

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT * FROM dogs
            WHERE name = ? AND breed = ? 
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name, breed, )).fetchone()
        # ipdb.set_trace()
        if(not dog):
            dog = cls.create(name, breed)
            # dog.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()
        return dog

    def update(self):
        sql = """
            update dogs
            set name = ?, breed = ?
            where id = ?
            LIMIT 1
        """
        # ipdb.set_trace()
        CURSOR.execute(sql, (self.name, self.breed, self.id,))
        