import db

import pandas as pd
def func_step_3(report_year,country_name,export_type):
    with db.create_db_connection() as connection:
        cursor=connection.cursor()
        cursor.callproc('Report_3',(report_year,country_name))
        answer=cursor.fetchall()

    ans_dataframe=pd.DataFrame(answer,columns=['Year','Country','Country Url','Region Code','Region','Rank Per Region','Overall Rank','Happiness Score','Happiness Status','GDP per Capita',
                                               'Family','Social Support','Healthy life expectancy','Freedom to make life choices','Generosity','Perceptions of Corruptions'])

    if(export_type=='csv'):
        ans_dataframe.to_csv('reports/Report_3.csv',index=False)
    else:
        ans_dataframe.to_parquet('reports/Report_3.gzip',compression='gzip')

    print("File has been saved to reports folder on root directory")

if __name__ == '__main__':
    # func_step_3()

    report_year=input("Specify year of report: ")
    country_name=input("Enter country name: ")
    region_code=input("Enter region code: ")
    export_type=input("Do you want the report in csv or parquet please: ")

    if(region_code != ''):
        country_name=db.get_company_name(region_code)

    func_step_3(report_year,country_name,export_type)



