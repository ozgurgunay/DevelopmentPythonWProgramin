# Import the pandas library and several functions from SQLAlchemy.
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Float, Integer

# Define a function to load data.
def load_data():
    # Create an engine that connects to a SQLite database.
    engine = create_engine('sqlite:///data_analysis.db')
    # Create a MetaData object to define the database schema.
    metadata = MetaData()

    # Load CSV files into pandas DataFrames
    train_df = pd.read_csv('train.csv')
    test_df = pd.read_csv('test.csv')
    ideal_df = pd.read_csv('ideal.csv')

    # Print column names to check
    print("Training DataFrame Columns:", train_df.columns.tolist())
    print("Ideal DataFrame Columns:", ideal_df.columns.tolist())
    print("Test DataFrame Columns:", test_df.columns.tolist())

    # Define table structures and create the database
    train_table = Table('train', metadata,
                        Column('X', Float, primary_key=True),
                        Column('Y1', Float),
                        Column('Y2', Float),
                        Column('Y3', Float),
                        Column('Y4', Float))

    ideal_table = Table('ideal', metadata,
                        Column('X', Float, primary_key=True),
                        *[Column(f'Y{i}', Float) for i in range(1, 51)])

    test_table = Table('test', metadata,
                       Column('X', Float, primary_key=True),
                       Column('Y', Float),
                       Column('DeltaY', Float),
                       Column('IdealFuncNo', Integer))

    # Create the tables in the database using the defined metadata.
    metadata.create_all(engine)

    # Load DataFrames into the database
    train_df.to_sql('train', con=engine, if_exists='replace', index=False)
    ideal_df.to_sql('ideal', con=engine, if_exists='replace', index=False)
    test_df.to_sql('test', con=engine, if_exists='replace', index=False)

    # Print a message to indicate successful data loading and table creation.
    print("Data loaded and database tables created successfully!")

if __name__ == "__main__":
    load_data()
