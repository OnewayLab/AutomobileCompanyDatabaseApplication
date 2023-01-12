import pymysql


class MysqlDb():
    """Management of a connection to the database

    Args:
        host: host where the database server is located
        port: MySQL port to use
        user: username to log in as
        password: password to use
        database: database to use
    """
    def __init__(self, host, port, user, password, database):
        # connect to the database
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self): # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # close the cursor
        self.cur.close()
        # close the connection to the database
        self.conn.close()

    def query(self, sql):
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