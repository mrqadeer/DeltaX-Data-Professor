from typing import Optional, List, Dict, Any

from pandasai.connectors import SQLConnector


class DatabaseConnector(SQLConnector):
    """
    Base class for handling database connections using PandasAI SQLConnector.
    This class provides the common functionality for all database connectors,
    while specific dialect and driver configurations are handled by subclasses.

    Attributes:
        host (Optional[str]): Database host address (None for SQLite).
        port (Optional[int]): Database port number (None for SQLite).
        database (str): Database name.
        username (Optional[str]): Database username (None for SQLite).
        password (Optional[str]): Database password (None for SQLite).
        table (str): Database table name to interact with.
        where (List[List[Any]]): Optional conditions to filter the query.
    """

    def __init__(
        self,
        host: Optional[str],
        port: Optional[int],
        database: str,
        username: Optional[str],
        password: Optional[str],
        table: str,
        where: Optional[List[List[Any]]] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.table = table
        self.where = where or []
        # Initialize the parent class with config
        super().__init__(config=self.get_config())

    def get_config(self) -> Dict[str, Any]:
        """
        Generate the configuration dictionary to be used by SQLConnector.

        Returns:
            Dict[str, Any]: Configuration dictionary containing the connection parameters.
        """
        
        
        return {
            "dialect": self.dialect,
            "driver": self.driver,
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "username": self.username,
            "password": self.password,
            "table": self.table,
            "where": self.where,
        }

    def connect(self) -> "SQLConnector":
        """
        Establish a connection to the database using the provided configuration.

        Returns:
            SQLConnector: An initialized instance of SQLConnector.
        """
        try:
            # Attempt to create a connection using the inherited functionality
            return super().__init__(config=self.get_config())
        except Exception as e:
            # Log the exception and raise it for further handling
            print(f"Failed to establish a connection: {e}")
            raise


        

class MySQLConnector(DatabaseConnector):
    """
    Connector class for MySQL databases, which inherits from DatabaseConnector.
    MySQL uses the 'mysql' dialect and 'pymysql' driver by default.
    """

    dialect = "mysql"
    driver = "pymysql"

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        table: str,
        where: Optional[List[List[Any]]] = None,
    ) -> None:
        """
        Initialize a MySQL database connector.

        Args:
            host (str): MySQL database host address.
            port (int): MySQL database port number.
            database (str): The name of the MySQL database.
            username (str): Username for MySQL connection.
            password (str): Password for MySQL connection.
            table (str): The table in the MySQL database to interact with.
            where (Optional[List[List[Any]]]): Optional conditions for filtering data.
        """
        super().__init__(host, port, database, username, password, table, where=where)


class PostgresConnector(DatabaseConnector):
    """
    Connector class for PostgreSQL databases, which inherits from DatabaseConnector.
    PostgreSQL uses the 'postgresql' dialect and 'psycopg2' driver by default.
    """

    dialect = "postgresql"
    driver = "psycopg2"

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        table: str,
        where: Optional[List[List[Any]]] = None,
    ) -> None:
        """
        Initialize a PostgreSQL database connector.

        Args:
            host (str): PostgreSQL database host address.
            port (int): PostgreSQL database port number.
            database (str): The name of the PostgreSQL database.
            username (str): Username for PostgreSQL connection.
            password (str): Password for PostgreSQL connection.
            table (str): The table in the PostgreSQL database to interact with.
            where (Optional[List[List[Any]]]): Optional conditions for filtering data.
        """
        super().__init__(host, port, database, username, password, table, where=where)


# Example usage
if __name__ == "__main__":
    # Example for SQLite connection
    # try:
    #     sqlite_connector = SQLiteConnector(database="my_sqlite_db", table="loans", where=[
    #                                        ["loan_status", "=", "PAIDOFF"]])
    #     sqlite_connector.connect()
    #     print("SQLite connection established successfully.")
    # except Exception as e:
    #     print(f"Error in SQLite connection: {e}")

    # Example for MySQL connection
    try:
        mysql_connector = MySQLConnector(
            host="localhost",
            port=3307,
            database="newdb",
            username="root",
            password="hitmath1122$",
            table="mobiles"
        )
        mysql_connector.connect()
        print("MySQL connection established successfully.")
    except Exception as e:
        print(f"Error in MySQL connection: {e}")

        # # Example for PostgreSQL connection
        # try:
        #     postgres_connector = PostgresConnector(
        #         host="localhost",
        #         port=5432,
        #         database="my_postgres_db",
        #         username="postgres_user",
        #         password="postgres_password",
        #         table="my_table",
        #         where=[["column_name", "=", "some_value"]]
        #     )
        #     postgres_connector.connect()
        #     print("PostgreSQL connection established successfully.")
        # except Exception as e:
        #     print(f"Error in PostgreSQL connection: {e}")