import os
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql


def fetch_all_insurance_data(cur):
    cur.execute("SELECT * FROM customer_insurance")
    return cur.fetchall()

def fetch_insurance_data_by_customer_id(cur, customer_id):
    cur.execute(sql.SQL("SELECT * FROM customer_insurance WHERE customer_id = %s"), [customer_id])
    return cur.fetchall()


# Load environment variables
load_dotenv()
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

     # Fetch all data from insurance table
    print("Fetching all data from insurance table:")
    all_data = fetch_all_insurance_data(cur)
    for row in all_data:
        print(row)

    print("\n" + "-"*50 + "\n")

    # Fetch data where customer_id = 101
    customer_id = 101
    print(f"Fetching data from insurance table where customer_id = {customer_id}:")
    customer_data = fetch_insurance_data_by_customer_id(cur, customer_id)
    for row in customer_data:
        print(row)

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if conn:
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")
