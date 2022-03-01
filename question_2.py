

import db

import json
import pandas as pd
import glob

def geolocate(country):
    import numpy as np
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="MCB_pipeline")
    try:
        # Geolocate the center of the country
        loc = geolocator.geocode(country)
        # And return latitude and longitude
        return (loc.latitude, loc.longitude)
    except:
        # Return missing value
        return np.nan


def convert_json_to_dict(filename):
    """ Convert json file to python dictionary
    """
    with open(filename, 'r') as JSON:
        json_dict = json.load(JSON)
    return json_dict

def convert_dict_to_df(filename):
    """ Convert python dictionary to pandas dataframe
    """
    return pd.json_normalize(convert_json_to_dict(filename))


def upload_to_sql(dataframe, db_name, debug=False):

    engine=db.create_db_engine()

    dataframe.to_sql(db_name,engine,if_exists='append',index=False)

    engine.dispose()


def preprocess_dataframe(dataframe,df_type='other'):

    if(df_type=='country'):
        map_relabel = {
            'Last Update': 'country',
            'images_file': 'images_file',
            'image_url': 'image_url',
            'alpha-2': 'alpha_2',
            'alpha-3': 'alpha_3',
            'country-code': 'country_code',
            'iso_3166-2': 'iso_3166_2',
            'region': 'region',
            'sub-region': 'sub_region',
            'intermediate-region': 'intermediate_region',
            'region-code': 'region_code',
            'sub-region-code': 'sub_region_code',
            'intermediate-region-code': 'intermediate_region_code'
        }
    else:
        map_relabel = {
            'Country': 'country',
            'Country or region':'country',

            'Happiness Score': 'happiness_score',
            'Happiness.Score': 'happiness_score',
            'Score': 'happiness_score',

            'Standard Error': 'standard_error',

            'Lower Confidence Interval': 'lower_limit',
            'Whisker.low': 'lower_limit',

            'Upper Confidence Interval': 'upper_limit',
            'Whisker.high': 'upper_limit',

            'Economy (GDP per Capita)': 'economy_gdp',
            'Economy..GDP.per.Capita.': 'economy_gdp',
            'GDP per capita': 'economy_gdp',

            'Family': 'family',
            'Social support': 'family',

            'Health (Life Expectancy)': 'health_life_expectancy',
            'Health..Life.Expectancy.': 'health_life_expectancy',
            'Healthy life expectancy': 'health_life_expectancy',

            'Freedom': 'freedom',
            'Freedom to make life choices': 'freedom',

            'Trust (Government Corruption)': 'trust',
            'Trust..Government.Corruption.': 'trust',
            'Perceptions of corruption': 'trust',

            'Generosity': 'generosity',

            'Dystopia Residual': 'dystopia_residual',
            'Dystopia.Residual': 'dystopia_residual'
        }





        #relabelling
    for label in dataframe:
        if label in map_relabel:
            dataframe=dataframe.rename(columns={label: map_relabel[label]})

    return dataframe

def import_country_data():
    # Extract
    country_data = convert_dict_to_df("../MCB Technical Assessment/data_cache/countries_continents_codes_flags_url.json")

    ## Transform
    country_data = preprocess_dataframe(country_data,df_type='country')

    upload_to_sql(country_data, 'tbl_country_region')

    print("Country data imported...")

def import_happiness_reports():
    # Get all csv files
    filelist = glob.glob("../MCB Technical Assessment/data_cache/hr_reports/*.csv")

    for filename in filelist:
        csv_file = pd.read_csv(filename)

        csv_file = preprocess_dataframe(csv_file)

        report_year = filename.replace('./MCB Technical Assessment/data_cache/hr_reports\\', "")
        report_year = report_year.replace(".csv", '')
        report_year = report_year.replace(".", '')
        elements = report_year.split('_')
        report_year = [a for a in elements if a.isdigit()][0]

        csv_file.insert(0, 'report_year', report_year)

        upload_to_sql(csv_file, 'happiness_report_sourcetable')

    with db.create_db_connection() as connection:
        cursor=connection.cursor()
        cursor.callproc('transfer_to_maintable',())

    print("Happiness reports imported...")

def update_coordinates_in_country_table():
    from math import isnan

    with db.create_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,alpha_2 FROM db_hp.tbl_country_region country where latitude is null and (alpha_2 is not null and alpha_2 <> '')")

        geo_info = cursor.fetchall()
        update_query='Update tbl_country_region set latitude=%s,longitude=%s where id=%s'
        for rec in geo_info:

            update_id=rec[0]
            alpha_2=rec[1]
            coo=geolocate(alpha_2)
            latitude=coo[0]
            longitude=coo[1]
            val=(latitude,longitude,update_id)
            cursor.execute(update_query,val)
            connection.commit()

if __name__ == '__main__':
    import_country_data()

    import_happiness_reports()









