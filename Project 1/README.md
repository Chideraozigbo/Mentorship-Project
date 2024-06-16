# Mentorship Program Project: Database Management Script

## Overview

This script, created as part of a collaborative project during a 6-month mentorship program, demonstrates how to manage and manipulate data in a SQL Server database using Python. The project was done by me and three other team members: @Alice, @Bob, and @Charlie.

## Script Breakdown

### Libraries and Logging Setup
The script starts by importing necessary libraries such as `pyodbc`, `sqlalchemy`, `pandas`, and `logging`. It then sets up logging to record the execution of the script, both to a file and the console.

### Functions for Database Operations
Three key functions are defined for interacting with the database:
1. `get_engine(server, database)`: Creates a SQLAlchemy engine for database connections.
2. `execute_sql(query, server, database)`: Executes SQL queries on the specified server and database.
3. `upload_data(dataframe, table, server, database, upload_type='replace')`: Uploads data from a pandas DataFrame to a specified table in the database.
4. `retrieve_data(query, server, database)`: Retrieves data from the database into a pandas DataFrame.

### Exercise 1: Customer Feedback Table
1. **Create Table**: A new table `CustomerFeedback` is created to store customer feedback data.
2. **Upload Sample Data**: Sample data is uploaded to the `CustomerFeedback` table.
3. **Update Data**: An update is performed to modify feedback data.
4. **Delete Data**: A record is deleted from the `CustomerFeedback` table.

### Exercise 2: Product Reviews Table
1. **Read CSV**: A CSV file containing product reviews is read into a pandas DataFrame.
2. **Create Table**: A new table `ProductReviews` is created in the database.
3. **Upload Data**: The data from the CSV file is uploaded to the `ProductReviews` table.

### Exercise 3: Sales Data Query
1. **Query Sales Data**: A query is run to retrieve total sales per product for orders placed in the last year.
2. **Export to CSV**: The retrieved sales data is exported to a CSV file.

## Contributors
- @Chideraozigbo
- @irorohgloryebube
- @Glaciux
- @HaticeMelikzade


