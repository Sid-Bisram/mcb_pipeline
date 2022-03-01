import configparser
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from sqlalchemy import create_engine

def getSQLCONFIG(filename):
    cf = configparser.ConfigParser()
    cf.read(filename)  # Read configuration file
    # Read corresponding file parameters
    _database = cf.get("current", "database")
    _host = cf.get("current", "host")
    _user = cf.get("current", "user")
    _pwd = cf.get("current", "pwd")

    return _database, _host, _user, _pwd  # return required parameters

db_config = getSQLCONFIG(r'..\dbconfig.config')
database = db_config[0]
host=db_config[1]
user = db_config[2]
password = db_config[3]



def create_db_connection():


    connection=pymysql.connect(database=database,host=host,user=user,password=password)
    print("Connection with database established ..........")

    return connection

def create_db_engine():
    db_data="mysql+mysqldb://{0}:{1}@{2}/{3}".format(user,password,host,database)
    engine=create_engine(db_data)

    return engine

def get_company_name(region_code):
    with create_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
                "Select country from tbl_country_region where region_code={0}".format(region_code))
        response = cursor.fetchone()

        if(response is not None):
            return response[0]
        else:
            return None

def close_connection(connection):
    """ Close connection with the database.
    """
    connection.commit()
    connection.close()
    print("Connection with database closed ..........")
