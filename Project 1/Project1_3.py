#%% Import necessary libraries
import pyodbc
import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine
import logging
from datetime import datetime

# Set up logging
log_filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Also set up logging to print to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

# Log the start of the script
logging.info("Script started.")

#%% Define functions for executing SQL queries and uploading data

def get_engine(server, database):
    connection_string = f'mssql+pyodbc://{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    return sqlalchemy.create_engine(connection_string)

def execute_sql(query, server, database):
    """
    Execute SQL query on specified server and database.

    Parameters:
        query (str): SQL query to execute.
        server (str): Server name/address.
        database (str): Name of the database.

    Returns:
        None
    """
    try: 
        logging.info("Attempting to connect to the database for executing SQL.")
        engine = get_engine(server, database)
        with engine.connect() as conn:
            conn.execute(query)
        logging.info("SQL query executed successfully.")
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        print(f"Error executing query: {e}")

def upload_data(dataframe, table, server, database, upload_type='replace'):
    """
    Upload data to specified table in the database.

    Parameters:
        dataframe (DataFrame): Pandas DataFrame containing data to upload.
        table (str): Name of the table to upload data.
        server (str): Server name/address.
        database (str): Name of the database.
        upload_type (str): Method of upload ('replace', 'append', etc.).

    Returns:
        None
    """
    try:
        logging.info("Attempting to connect to the database for uploading data.")
        engine = create_engine(
            f'mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
        )
        logging.info(f"Uploading data to table: {table}")

        # Upload data to table
        dataframe.to_sql(
            name=table,
            con=engine,
            if_exists=upload_type,
            index=False,
            schema="dbo",
            chunksize=10000
        )
        
        logging.info(f"Data uploaded successfully to {table}.")

    except Exception as e:
        logging.error(f"Error uploading data: {e}")
        print(f"Error uploading data: {e}")

def retrieve_data(query, server, database):
    """
    Retrieve data from specified server and database using SQL query.

    Parameters:
        query (str): SQL query to retrieve data.
        server (str): Server name/address.
        database (str): Name of the database.

    Returns:
        DataFrame: Pandas DataFrame containing retrieved data.
    """
    try:
        logging.info("Attempting to connect to the database for retrieving data.")
        conn = pyodbc.connect(
            f'Driver={{ODBC Driver 17 for SQL Server}};'
            f'Server={server};'
            f'Database={database};'
            'Trusted_Connection=yes;'
        )
        
        logging.info(f"Retrieving data with query: {query}")
        
        # Read data using SQL query
        df = pd.read_sql(query, conn)
        
        logging.info("Data retrieved successfully.")
        return df
        
    except Exception as e:
        logging.error(f"Error retrieving data: {e}")
        print(f"Error retrieving data: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error

    finally:
        # Close connection
        if conn:
            conn.close()

# Define parameters
server = "DESKTOP-KHTL27T"  # Your SQL Server instance name
database = "AdventureWorks2022"  # Your database name


##########################################################################################################

#### EXERCISE 1

##########################################################################################################

#%% Create a new table called CustomerFeedback
create_table_query = """
CREATE TABLE dbo.CustomerFeedback (
  FeedbackID INT PRIMARY KEY IDENTITY,
  CustomerID INT NOT NULL,
  FeedbackDate DATE NOT NULL,
  Comments VARCHAR(300)
);
"""
try:
    execute_sql(create_table_query, server, database)
    logging.info("SQL query executed successfully")
    print("SQL query executed successfully")
except Exception as e:
    logging.error(f"Failed to execute SQL query: {e}")
    print(f"Failed to execute SQL query:{e}")

#%% Upload sample data into CustomerFeedback table
data_to_upload = pd.DataFrame({
    'CustomerID': [101, 102, 103, 104, 105],
    'FeedbackDate': ["2024-06-08", "2024-06-09", "2024-06-10", "2024-06-11", "2024-06-12"],
    'Comments': ['Great product!', 'Nice product!', 'Product is okay!', 'Nice', 'It is okay']
})
try:
    upload_data(data_to_upload, 'CustomerFeedback', server, database, upload_type='append')
    logging.info("Data uploaded successfully")
    print("Data uploaded successfully")
except Exception as e:
    logging.error(f"Failed to upload data: {e}")
    print(f"Failed to upload data:{e}")

#%% Update CustomerFeedback table
update_query = """
UPDATE dbo.CustomerFeedback
SET FeedbackDate = '2024-06-09'
WHERE CustomerID = 101
"""
try:
    execute_sql(update_query, server, database)
    logging.info("Record updated successfully")
    print("Record updated successfully")
except Exception as e:
    logging.error(f"Failed to update record: {e}")
    print(f"Failed to update record: {e}")

#%% Delete a record from CustomerFeedback table
delete_query = """
DELETE FROM dbo.CustomerFeedback
WHERE CustomerID = 105
"""
try:
    execute_sql(delete_query, server, database)
    logging.info("Record deleted successfully")
    print("Record deleted successfully")
except Exception as e:
    logging.error(f"Failed to delete record: {e}")
    print(f"Failed to delete record: {e}")


##########################################################################################################

##### EXERCISE 2

##########################################################################################################

#%% Read the CSV file and upload its contents to ProductReviews table
csv_file_path = r'C:\Users\Melikzade\Desktop\SQL Course Materials\productReviews\7817_1.csv'
try:
    df_reviews = pd.read_csv(csv_file_path)  # Add encoding if necessary: , encoding='ISO-8859-1'
    logging.info(f"CSV file {csv_file_path} read successfully.")
except FileNotFoundError as e:
    logging.error(f"Error reading CSV file: {e}")
    print(f"Error reading CSV file: {e}")
    df_reviews = None

if df_reviews is not None:
    # Step 2: Create a new table in the database
    create_table_query = """
    IF OBJECT_ID('dbo.ProductReviews', 'U') IS NOT NULL 
       DROP TABLE dbo.ProductReviews;
    CREATE TABLE dbo.ProductReviews (
        ID INT PRIMARY KEY IDENTITY,
        asins NVARCHAR(255),
        brand NVARCHAR(255),
        categories NVARCHAR(MAX),
        colors NVARCHAR(255),
        dateAdded DATETIME,
        dateUpdated DATETIME,
        dimension NVARCHAR(255),
        ean NVARCHAR(255),
        keys NVARCHAR(MAX),
        manufacturer NVARCHAR(255),
        manufacturerNumber NVARCHAR(255),
        name NVARCHAR(255),
        prices FLOAT,
        reviews_date DATETIME,
        reviews_doRecommend BIT,
        reviews_numHelpful INT,
        reviews_rating FLOAT,
        reviews_sourceURLs NVARCHAR(MAX),
        reviews_text NVARCHAR(MAX),
        reviews_title NVARCHAR(255),
        reviews_userCity NVARCHAR(255),
        reviews_userProvince NVARCHAR(255),
        reviews_username NVARCHAR(255),
        sizes NVARCHAR(255),
        upc NVARCHAR(255),
        weight FLOAT
    );
    """
    execute_sql(create_table_query, server, database)

    # Step 3: Upload data to the new table
    try:
        upload_data(df_reviews, 'ProductReviews', server, database)
        logging.info("Data uploaded successfully to ProductReviews")
        print("Data uploaded successfully to ProductReviews")
    except Exception as e:
        logging.error(f"Failed to upload data to ProductReviews: {e}")
        print(f"Failed to upload data to ProductReviews: {e}")
else:
    logging.error("CSV file could not be read. Data upload skipped.")
    print("CSV file could not be read. Data upload skipped.")

# Log the completion of the script
logging.info("Script completed.")
print("Script completed.")

##########################################################################################################

### EXERCISE 3

##########################################################################################################

#%% Query to get the total sales per product for orders placed in the last year(2014)
query_last_year_sales = """
SELECT
    p.Name AS ProductName,
    SUM(sod.LineTotal) AS TotalSales
FROM
    Sales.SalesOrderDetail sod
JOIN
    Sales.SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
JOIN
    Production.Product p ON sod.ProductID = p.ProductID
WHERE
    soh.OrderDate >= DATEADD(year, -10, GETDATE())
GROUP BY
    p.Name
ORDER BY
    TotalSales DESC;
"""

# Retrieve data for last year's sales
df_last_year_sales = retrieve_data(query_last_year_sales, server, database)
logging.info("Last Year Sales Data:\n%s", df_last_year_sales.head())

# Check if DataFrame is not empty, then export to CSV
if not df_last_year_sales.empty:
    df_last_year_sales.to_csv("lastYearSales.csv", index=False)
    logging.info("Data exported to lastYearSales.csv")
else:
    logging.info("No sales data available for last year.")



# %%
