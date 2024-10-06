import streamlit as st
from typing import Optional, List, Dict, Any

from pandasai.connectors import SQLConnector
from pandasai.connectors import SqliteConnector
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
            super().__init__(config=self.get_config())
            return self
        except Exception as e:
            # Log the exception and raise it for further handling
            st.error(f"Failed to establish a connection: {e}")
            st.stop()


        

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

def handle_database_connection(credentials: Dict) -> Any:
    """
    Handles the database connection based on the credentials provided.

    Args:
        credentials (Dict): A dictionary containing the database credentials.
    """
    # Implement the logic to handle the database connection based on the credentials
    for db in credentials:
        match db:
            case 'MySQL':
                try:
                    connector = MySQLConnector(**credentials[db]).connect()
                    st.success("Connected to MySQL")
                    
                except Exception as e:
                    st.error(e)
                    st.stop()
            case 'SQLite':
                try:
                    connector = SqliteConnector(config=credentials[db])
                    st.success("Connected to SQLite")
                except Exception as e:
                    st.error(e)
                    st.stop()
            case 'PostgreSQL':
                try:
                    
                    connector = PostgresConnector(**credentials[db]).connect()
                    st.success("Connected to Postgress")
                except Exception as e:
                    st.error(e)
                    st.stop()
            case _:
                st.error("Database not supported")
    st.session_state['is_connected'] = True
    return connector
