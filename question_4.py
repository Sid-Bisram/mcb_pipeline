import db

import pandas as pd

def func_step_4(country_name):
    with db.create_db_connection() as connection:
        cursor=connection.cursor()
        # cursor.callproc('report_3',(country_name))
        cursor.callproc('report_4', [country_name])
        answer=cursor.fetchall()

    ans_dataframe=pd.DataFrame(answer,columns=['Country','Highest Rank','Lowest Rank','Highest Happiness Score','Lowest Happiness Score'])

    ans_dataframe.to_json('reports/Report_4.json')

    print("File has been saved to reports folder on root directory")

if __name__ == '__main__':
    country_name=input("Enter country name: ")

    func_step_4(country_name)



