import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def delete_all_data(conn, cur):
    try:
        # Delete all data from customer_insurance table
        cur.execute("DELETE FROM customer_insurance;")
        print("All data deleted from customer_insurance table.")

        # Delete all data from customers table
        cur.execute("DELETE FROM customers;")
        print("All data deleted from customers table.")

        # Commit the changes
        conn.commit()
        print("All data has been successfully deleted from both tables.")

    except (Exception, psycopg2.Error) as error:
        print("Error while deleting data:", error)
        conn.rollback()  # Rollback the transaction if an error occurs

    finally:
        # Reset the auto-incrementing primary keys
        cur.execute("ALTER SEQUENCE customers_customer_id_seq RESTART WITH 1;")
        cur.execute("ALTER SEQUENCE customer_insurance_customer_policy_id_seq RESTART WITH 1;")
        conn.commit()
        print("Primary key sequences reset.")
db_params = {
    "dbname": os.getenv("POSTGRES_DB", "fastapi-db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

try:
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Delete all data
    delete_all_data(conn, cur)

    # Your other operations (creating tables, inserting data, etc.)
    # ...

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if conn:
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")
