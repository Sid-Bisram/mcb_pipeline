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
    # print("Connection with database established ..........")

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

def get_company_list():
    with create_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
                "Select distinct country from tbl_country_region")
        response = list(cursor.fetchall())

        if(response is not None):
            return [data[0] for data in response]
        else:
            return None

def get_Q5_dataset():
    with create_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
                "SELECT main.report_year,country.country,country.image_url,country.latitude,country.longitude,main.happiness_score,case when main.happiness_score>5.6 then 'green' else case when main.happiness_score between 2.6 and 5.6 then 'amber' else 'red' end end as happiness_status FROM db_hp.happiness_report_maintable main left join tbl_country_region country on main.country_id=country.id")
        response = cursor.fetchall()

        if(response is not None):
            return response
        else:
            return None

def get_Q6_dataset():
    with create_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
                "select id,alpha_2,capital_city,latitude,longitude from tbl_country_region where alpha_2 is not null or alpha_2 <> ''")
        response = cursor.fetchall()

        if(response is not None):
            return response
        else:
            return None

def update_Q6_dataset(table_name,key_name,key_value,field_name,field_value):
    with create_db_connection() as connection:
        cursor = connection.cursor()
        sql = "Update {0} set {1}=%s where {2}= %s".format(table_name,field_name,key_name)
        val = (field_value, key_value)
        cursor.execute(sql, val)
        connection.commit()

def close_connection(connection):
    """ Close connection with the database.
    """
    connection.commit()
    connection.close()
    print("Connection with database closed ..........")
