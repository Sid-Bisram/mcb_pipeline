if __name__ == '__main__':
    import requests
    import db

    counter=0

    ds=db.get_Q6_dataset()
    for country in ds:
        id=country[0]
        alpha_2=country[1]
        db_capital_city=country[2]
        db_latitude=country[3]
        db_longitude=country[4]
        response = requests.get(" http://api.worldbank.org/v2/country/{0}?format=json".format(alpha_2))

        if(response.status_code==200):
            country_json=response.json()[1][0]

            capital=country_json['capitalCity']
            longitude=country_json['longitude']
            latitude=country_json['latitude']

            db.update_Q6_dataset('tbl_country_region','id',id,'capital_city',capital)
            db.update_Q6_dataset('tbl_country_region', 'id', id, 'latitude', latitude)
            db.update_Q6_dataset('tbl_country_region', 'id', id, 'longitude', longitude)
            counter += 1
        else:
            print("Api cant be accessed")

    print("{0} fields have been updated".format(counter))
