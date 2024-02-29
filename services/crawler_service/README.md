1 A service which downloads csv every day from government website and checks whether csv is new. If the csv is new , the csv is downloaded

2 Each page of csv is extracted and different company information is put to database. The database is MongoDB.

3 This scans will delete companies from the database, if the company no longer sponsors. The deleted data is moved to a new table, so as to display it back to users.

4 This service scrapes google and find the company's website or find the company's carrers page and website based on the company's name and location ()

5. Data is saved in a database.

Addition (Nice to have)

Another service, will fetch the company address, and SIC codes from Companies House API. https://developer.companieshouse.gov.uk/api/docs/



Written with Flask