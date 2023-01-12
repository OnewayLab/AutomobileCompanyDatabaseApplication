import pymysql
from typing import Union

class MysqlDb:
    """Management of a connection to the database

    Args:
        host: host where the database server is located
        port: MySQL port to use
        user: username to log in as
        password: password to use
        database: database to use
    """

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        # connect to the database
        self.conn = pymysql.connect(
            host=host, port=port, user=user, password=password, database=database
        )
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        # close the cursor
        self.cur.close()
        # close the connection to the database
        self.conn.close()

    def init(self, schema_path: str, test_data: Union[str, None] = None):
        """Initialize the database

        Args:
            schema_path: path of the schema file
            test_data: path of the test data file to insert, None to not insert
        """
        with open(schema_path, "r") as f:
            # read the schema file
            schema = f.read()
            commands = schema.split(";")
            # execute the sql statement
            for command in commands:
                self.cur.execute(command)
            self.conn.commit()

        if test_data is not None:
            with open(test_data, "r") as f:
                # read the test data file
                data = f.read()
                commands = data.split(";")
                # execute the sql statement
                for command in commands:
                    self.cur.execute(command)
                self.conn.commit()

    def query(self, sql: str):
        """Query

        Args:
            sql: SQL statement

        Returns:
            data: tuple of the result
        """
        # check the connect is break, if it's break, reconnect
        self.conn.ping(reconnect=True)

        # execute the sql statement
        self.cur.execute(sql)

        # fetch the result
        data = self.cur.fetchall()
        return data

    def execute(self, sql):
        """Update/Delete/Create

        Args:
            sql: SQL statement
        """
        # check the connect is break, if it's break, reconnect
        self.conn.ping(reconnect=True)

        # execute the sql statement
        self.cur.execute(sql)
        self.conn.commit()

    def get_attributes(self, table):
        """Get attributes of a table

        Args:
            table: table to get attributes

        Returns:
            tuple of all the attributes
        """
        # check the connect is break, if it's break, reconnect
        self.conn.ping(reconnect=True)

        # get the attributes of the table
        self.cur.execute(f"desc {table}")
        data = self.cur.fetchall()
        return data
