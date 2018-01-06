"""Module db - provides sqlite3 db functions"""
import sqlite3

# List of banks that get loaded. TODO Can look to get the list from online
BANKS = ["Abbey","American Express","Barclays","Citigroup","Lloyds TSB","HBOS","Bank of Ireland Group",
         "HSBC","NatWest","RBOS","Standard Chartered Bank","Alliance & Leicester","Bradford & Bingley",
         "Northern Rock","The Woolwich","Adam & Company","Airdrie Savings Bank","Arbuthnot Latham & Co",
         "Butterfield Private Bank","Cater Allen Private Bank","C.Hoare & Co","Clydesdale Bank ","Co-operative Bank",
         "Coutts & Co","Drummonds","DB(UK)Bank","Egg","ICICI Bank UK","Icesave","ING Direct","Julian Hodge Bank",
         "Kleinwort Benson Private Bank Ltd","Raphaels Bank","Reliance Bank","Yorkshire Bank","Sainsbury's Bank",
         "Whiteaway Laidlaw Bank","Nationwide","Britannia","Yorkshire","Coventry","Chelsea","Skipton","Leeds",
         "West Bromwich","Derbyshire","Principality","Cheshire","Newcastle","Norwich & Peterborough","Dunfermline",
         "Stroud & Swindon","Nottingham","Scarborough","Kent Reliance","Progressive","Cumberland","National Counties",
         "Furness","Cambridge","Leek United","Manchester","Saffron","Hinckley & Rugby","Darlington","Newbury",
         "Monmouthshire","Melton Mowbray","Market Harborough","Ipswich","Barnsley","Marsden","Tipton & Coseley",
         "Hanley Economic","Mansfield","Teachers'","Loughborough","Chesham","Dudley","Vernon","Scottish",
         "Bath Investment &","Chorley & District","Harpenden","Holmesdale","Stafford Railway","Beverley",
         "Buckinghamshire","Swansea","Earl Shilton","Shepshed","Penrith","Ecology","Catholic","City of Derry",
         "Century Building Society"]


def create_new_database(connection):
    """Creates a set of databases. One for Accounts, one for transactions, one for categories,
        and 2 tables to act as the many to many table"""
    # Create a cursor from the connection to exeucute code
    try:
        cursor = connection.cursor()
        sqlcom = """CREATE TABLE bank( name TEXT);"""
        cursor.execute(sqlcom)
        sqlcom2 = """ INSERT INTO bank(name) VALUES (?)"""
        cursor.executemany(sqlcom2, BANKS)
        print('executed')

        sqlcom = """CREATE TABLE account(id INTEGER PRIMARY KEY, name TEXT, bank TEXT, 
                    FOREIGN KEY(bank) REFERENCES bank(name));"""
        cursor.execute(sqlcom)

        # todo Need to create transaction table before link and look at the primary key for it
        # The repeat column will be defaulted to 0 and for any duplicate transactions will look at increasing the value
        sqlcom5 = """CREATE TABLE transactions(id INTEGER NOT NULL PRIMARY KEY, DATE TIMESTAMP, account text NOT NULL, value integer NOT NULL,
                repeat integer NOT NULL, description text, unique(date, account, value)) """
        cursor.execute(sqlcom5)
        sqlcom6 = """CREATE TABLE category(id INTEGER PRIMARY KEY , category TEXT);
                CREATE TABLE ml_category(id INTEGER PRIMARY KEY , category TEXT);
                CREATE TABLE transaction_category(trans_id INTEGER NOT NULL, category_id INTEGER NOT NULL, PRIMARY KEY (trans_id
                , category_id), FOREIGN KEY(trans_id) REFERENCES transactions(id), FOREIGN KEY(category_id) REFERENCES 
                category(id));"""
        cursor.executescript(sqlcom6)

    except Exception as e:
        print(e)
        print('Database not created')
        connection.rollback()

    else:
        connection.commit()
