from contextlib import closing
from sqlite3 import connect

DATABASE_URL = "file:lux.sqlite?mode=ro"

OBJECTS_SRCH = """WITH 
    agent_data AS (
        SELECT id,
        IFNULL(group_concat(part || ': ' || name), '') AS 'ag'
        FROM (
            SELECT o.id, a.name AS name, p.part AS 'part'
            FROM objects o
            LEFT JOIN productions p ON o.id = p.obj_id
            LEFT JOIN agents a ON a.id = p.agt_id
            ORDER BY p.part ASC, a.name ASC
            )
        GROUP BY id
        )
    SELECT o.id AS ID, o.label AS label, o.date AS date, a.ag AS ag
    FROM objects o
    LEFT JOIN agent_data a ON a.id = o.id
    """

def get_ids():
    with connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:

        # Building the Table of details for the object
        with closing(connection.cursor()) as cursor:
            query = "SELECT objects.id FROM objects"
            cursor.execute(query)
            results = cursor.fetchall()

            return [res[0] for res in results]

def query_details(id : str):
    with connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:

        # Building the Table of details for the object
        with closing(connection.cursor()) as cursor:
            query = OBJECTS_SRCH
            query += " WHERE o.id=?"
            cursor.execute(query, [id])
            results = cursor.fetchall()

            return results