"""Module db - provides sqlite3 db functions"""
import sqlite3

# List of banks that get loaded. TODO Can look to get the list from online
BANKS = ["Abbey","American Express","Barclays","Citigroup","Lloyds TSB","HBOS","Bank of Ireland Group",
         "HSBC","NatWest","RBOS","Standard Chartered Bank","Alliance & Leicester","Bradford & Bingley",
         "Northern Rock","The Woolwich","Adam & Company","Airdrie Savings Bank","Arbuthnot Latham & Co",
         "Butterfield Private Bank","Cater Allen Private Bank","C.Hoare & Co","Clydesdale Bank ","Co-operative Bank",
         "Coutts & Co","Drummonds","DB(UK)Bank","Egg","ICICI Bank UK","Icesave","ING Direct","Julian Hodge Bank",
         "Kleinwort Benson Private Bank Ltd","Raphaels Bank","First Direct","Monzo","Nutmeg","Reliance Bank","Yorkshire Bank","Sainsbury's Bank",
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
        print('Database Created')

        # For how to add Bank Accounts to the database
        #
        # bank_id = """SELECT name FROM bank WHERE name=?"""
        # accounts = [("Barclays", "Current Account"), ("Barclays", "Help To Buy"), ("Barclays", "Saver"),
        #             ("Barclays", "Initial Barclaycard"), ("Barclays", "Platinum Barclaycard"), ("TSB", "Classic Plus"),
        #             ("Nationwide", "Flex Plus"), ("Nationwide", "Flex Saver"), ("Nutmeg", "LISA"),
        #             ("Charles Stanley", "ISA"), ("Co-Op", "Student Account"), ("First Direct", "First Acount"),
        #             ("First Direct", "Regular Saver")]
        #
        # for bank, acc in accounts:
        #     id_n = cursor1.execute(bank_id, (bank,)).fetchone()
        #     print(id_n)
        #     cursor1.execute("""INSERT INTO account(id, name, bank) VALUES (NULL, ?,?)""", (acc, bank))

    except Exception as e:
        print(e)
        print('Database not created')
        connection.rollback()

    else:
        connection.commit()


def add_bank(connection, bank):
    """Takes the database connection and adds bank to the bank(name) table"""
    # TODO bank -> banks
    if bank is str:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO bank(name) VALUES (?)""", tuple(bank))
    else:
        raise TypeError("Bank supplied is not a string")
    return



