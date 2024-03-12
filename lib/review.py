# lib/review.py
from __init__ import CURSOR, CONN
from department import Department
from employee import Employee

class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in a local dictionary using the table row's PK as a dictionary key"""
        sql = """
        INSERT INTO reviews(year, summary, employee_id, id)
        VALUES(?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        self.__class__.all[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        """Return a Review instance having the attribute values from the table row."""
        # Check the dictionary for an existing instance using the row's primary key
        if row[0] in cls.all:
            return cls.all[row[0]]

        # If not found, create a new instance
        review = cls(row[1], row[2], row[3], id=row[0])
        cls.all[row[0]] = review
        return review

    @classmethod
    def find_by_id(cls, review_id):
        """Return a Review instance having the attribute values from the table row."""
        sql = """
        SELECT *
        FROM reviews
        WHERE id = ?
        """

        row = CURSOR.execute(sql, (review_id,)).fetchone()

        return cls.instance_from_db(row) if row else None

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        sql = """
        UPDATE reviews
        SET year=?, summary=?, employee_id=?
        WHERE id=?
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        sql = """
        DELETE FROM reviews
        WHERE id=?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del self.__class__.all[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        sql = """
        SELECT *
        FROM reviews
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    # @property
    # def year(self):
    #     return self._year

    # @year.setter
    # def year(self, value):
    #     if not isinstance(value, int) or value < 2000:
    #         raise ValueError("Year must be an integer greater than or equal to 2000")
    #     self._year = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if not isinstance(value, int) or value < 2000:
            raise ValueError("Year must be an integer greater than or equal to 2000")
        self._year = value


    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Summary must be a non-empty string")
        self._summary = value

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        # You may want to add additional validation here, e.g., checking if the employee_id exists in the Employee table
        self._employee_id = value


