"""Module db - provides sqlite3 db functions"""
import sqlite3
import collections
import datetime

# List of banks that get loaded. TODO Can look to get the list from online or file that gets updated
BANKS = ["Abbey", "American Express", "Barclays", "Citigroup", "Lloyds TSB", "HBOS", "Bank of Ireland Group", "HSBC",
         "NatWest", "RBOS", "Standard Chartered Bank", "Alliance & Leicester", "Bradford & Bingley", "Northern Rock",
         "The Woolwich", "Adam & Company", "Airdrie Savings Bank", "Arbuthnot Latham & Co", "Butterfield Private Bank",
         "Cater Allen Private Bank", "C.Hoare & Co", "Clydesdale Bank ", "Co-operative Bank", "Coutts & Co",
         "Drummonds", "DB(UK)Bank", "Egg", "ICICI Bank UK", "Icesave", "ING Direct", "Julian Hodge Bank",
         "Kleinwort Benson Private Bank Ltd", "Raphaels Bank", "First Direct", "Monzo", "Nutmeg", "Reliance Bank",
         "Yorkshire Bank", "Sainsbury's Bank", "Whiteaway Laidlaw Bank", "Nationwide", "Britannia", "Yorkshire",
         "Coventry", "Chelsea", "Skipton", "Leeds", "West Bromwich", "Derbyshire", "Principality", "Cheshire",
         "Newcastle", "Norwich & Peterborough", "Dunfermline", "Stroud & Swindon", "Nottingham", "Scarborough",
         "Kent Reliance", "Progressive", "Cumberland", "National Counties", "Furness", "Cambridge", "Leek United",
         "Manchester", "Saffron", "Hinckley & Rugby", "Darlington", "Newbury", "Monmouthshire", "Melton Mowbray",
         "Market Harborough", "Ipswich", "Barnsley", "Marsden", "Tipton & Coseley", "Hanley Economic", "Mansfield",
         "Teachers'", "Loughborough", "Chesham", "Dudley", "Vernon", "Scottish", "Bath Investment &",
         "Chorley & District", "Harpenden", "Holmesdale", "Stafford Railway", "Beverley", "Buckinghamshire", "Swansea",
         "Earl Shilton", "Shepshed", "Penrith", "Ecology", "Catholic", "City of Derry", "Century Building Society",
         "Santander"]

ONE_DAY = datetime.timedelta(1)

DATE_FORMAT = collections.OrderedDict({'dd mm yy': ['%d', '%m','%y'] , 'dd mm yyyy': ['%d', '%m', '%Y'],
                                       'mm dd yy': ['%m', '%d', '%y'], 'mm dd yyyy': ['%m', '%d', '%Y'],
                                       'yy mm dd': ['%y', '%m', '%d'], 'yyyy mm dd': ['%Y', '%m', '%d'],
                                       'yy dd mm': ['%y', '%d', '%m'], 'yyyy dd mm': ['%Y', '%d', '%m']})

DATE_DELIMITER = {'Space ( )':' ','Forward Slash (/)':'/','Comma (,)':','}

def create_new_database(connection):
    """Creates a set of databases. One for Accounts, one for transactions, one for categories,
        and 2 tables to act as the many to many table"""
    if type(connection) is not sqlite3.Connection:
        raise TypeError("Connection supplied is not an sqlite3.Connection")
    try:
        # Create a cursor from the connection to exeucute code
        cursor = connection.cursor()
        sqlcom = """CREATE TABLE bank( name TEXT);"""
        cursor.execute(sqlcom)
        # TODO Look at storing bitcoin transactions/value
        sqlcom2 = """ INSERT INTO bank(name) VALUES (?)"""
        # Turn the BANKS list into a list of single value tuples, what the executemany function requires
        banks = [tuple(x) for x in BANKS]
        cursor.executemany(sqlcom2, banks)

        # TODO add a format identifier so can know how to parse data
        # (datefmt, col, ...)
        # Could this be an object that stores the data?

        sqlcom = """CREATE TABLE account(id INTEGER PRIMARY KEY, name TEXT, bank TEXT, 
                    FOREIGN KEY(bank) REFERENCES bank(name));"""
        cursor.execute(sqlcom)

        # todo Need to create transaction table before link and look at the primary key for it
        # The repeat column will be defaulted to 0 and for any duplicate transactions will look at increasing the value
        sqlcom5 = """CREATE TABLE transactions(id INTEGER NOT NULL PRIMARY KEY, DATE TIMESTAMP, account text NOT NULL, 
                    value integer NOT NULL, repeat integer NOT NULL, description text, unique(date, account, value)) """
        cursor.execute(sqlcom5)
        sqlcom6 = """CREATE TABLE category(id INTEGER PRIMARY KEY , category TEXT);
                CREATE TABLE ml_category(id INTEGER PRIMARY KEY , category TEXT);
                CREATE TABLE transaction_category(trans_id INTEGER NOT NULL, category_id INTEGER NOT NULL,
                PRIMARY KEY (trans_id, category_id), FOREIGN KEY(trans_id) REFERENCES transactions(id),
                FOREIGN KEY(category_id) REFERENCES category(id));"""
        cursor.executescript(sqlcom6)
        print('Database Created')

    except Exception as e:
        print('Database not created')
        print(e)
        connection.rollback()

    else:
        connection.commit()


def add_bank(connection, bank):
    """Takes the database connection and adds bank to the bank(name) table"""
    # TODO bank -> banks
    if type(bank) is str:
        try:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO bank(name) VALUES (?)""", tuple(bank))

        except Exception as e:
            print("Error inserting bank into table")
            print(e)
            connection.rollback()

        else:
            connection.commit()
    else:
        raise TypeError("Bank supplied is not a string")
    return
# TODO add account

def add_transaction(connection, date, account, value, repeat=0, initial=False, description=None):
    """Adds a line to the transaction(id, date, account, value, repeat, initial, description) table. Connection is
    not committed when finished"""
    cursor_ob = connection.cursor()
    try:
        cursor_ob.execute("""INSERT INTO transactions(id, date, account, value, repeat, initial, description) VALUES(NULL, ?,?,?,
    ?,?,?)""", (date, account, value, repeat, initial, description))

    except sqlite3.IntegrityError:
        # When a line already exists in the table, do not add and continue TODO (Check repeat flag when parsing CSV)
        print("Line duplicated in table")
    return


def clear_database(connection):
    try:
        cursor = connection.cursor()
        # Empties the database and then re-initialises it with the create_new_database command
        cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
        for item in cursor.fetchall():
            cursor.execute("""DROP table IF EXISTS ?""", item)
        print("All transactions deleted")
        # Repopulate database with defaults
        create_new_database(connection)
    except Exception as e:
        print("Error deleting data from database")
        print(e)
        connection.rollback()
    else:
        connection.commit()


def get_data(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("Something went wrong, no data for you")
        print(e)
        return None


def sumtrans(data):
    """Sums the transactions that are extracted in date order and fills in all the blank days"""
    total = 0
    dct = collections.defaultdict(float)
    first_date = data[0][0]
    last_date = data[-1][0]
    current_day = first_date
    for x, y in data:
        total += y
        dct[x] = total
    while current_day != last_date:
        if current_day not in dct:
            value = dct[current_day - ONE_DAY]
            dct[current_day] = value

        current_day = current_day + ONE_DAY
    return list(dct.items())


# Function that can handle the filtering when getting data, or handle that in the front side, when connected to the gui
