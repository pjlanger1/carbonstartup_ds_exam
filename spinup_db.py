from db_helper import *

def setup():
    
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, text
    #import helper functions too

    list_1 = ['2020-v189-24062023-EU MRV Publication of information.xlsx','2019-v215-30062023-EU MRV Publication of information.xlsx','2018-v269-16052023-EU MRV Publication of information.xlsx']
    #list_1 = ['/Users/peter/Downloads/2020-v189-24062023-EU MRV Publication of information.xlsx','/Users/peter/Downloads/2019-v215-30062023-EU MRV Publication of information.xlsx','/Users/peter/Downloads/2018-v269-16052023-EU MRV Publication of information.xlsx']
    gen = process_to_dict(list_1)
    df_2020 = next(gen)
    df_2019 = next(gen)
    df_2018 = next(gen)

    collist, nullablelist,dtype_list,list_of_colnames = list_creation()
    # create an in-memory SQLite database
    #engine = create_engine('sqlite:///:memory:', echo=False)
    engine = create_engine("sqlite:///foo.db",echo = True)
    metadata = MetaData(bind=engine)

    #collist2
    collist_f = collist[4:]
    dtype_f = dtype_list[4:]

    dictionary = dict(zip(collist_f, dtype_f))

    #Instantiating DB in local path
    t = Table('carbon_reporting', metadata, Column('imo_number', Integer, primary_key=True),
            Column('name',String),Column('type',String),Column('reporting_period', Integer, primary_key = True),
        *(Column(key, dictionary[key]) for key in dictionary.keys()))
    metadata.create_all()
    
    ##Loading DB
    Session = sessionmaker(bind=engine)
    session = Session()
    conn = engine.connect()
    # Inser the dataframe into the database in one bulk
    conn.execute(t.insert(), df_2020)
    conn.execute(t.insert(), df_2019)
    conn.execute(t.insert(), df_2018)
    # Commit the changes
    session.commit()

    # Close the session
    session.close()

setup()