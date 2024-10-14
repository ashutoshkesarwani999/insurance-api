import psycopg2
from psycopg2 import sql
from datetime import date
import os
from dotenv import load_dotenv
import hashlib
import bcrypt

# Load environment variables
load_dotenv()

# Database connection parameters
db_params = {
    "dbname": os.getenv("POSTGRES_DB", "dbtest"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "0.0.0.0"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}


def hash_password(password):
    # First, hash the password with SHA-256
    sha256_hash = hashlib.sha256(password.encode()).digest()

    # Then, use bcrypt to hash the result
    bcrypt_hash = bcrypt.hashpw(sha256_hash, bcrypt.gensalt())

    return bcrypt_hash

# Create customers table query
create_customers_table_query = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) UNIQUE
);
"""

# Create customer_insurance table query with foreign key
create_customer_insurance_table_query = """
CREATE TABLE IF NOT EXISTS customer_insurance (
    customer_policy_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    insurance_id INTEGER NOT NULL,
    customer_policy_url TEXT NOT NULL,
    created_at DATE NOT NULL,
    updated_at DATE,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);
"""

# Sample customer data
sample_customers = [
    ("john.doe@example.com", hash_password("password123")),
    ("jane.smith@example.com", hash_password("securepass456")),
    ("alice.johnson@example.com", hash_password("strongpassword789")),
    ("bob.wilson@example.com", hash_password("mysecretpass321")),
    ("emma.brown@example.com", hash_password("safepassword654")),
    ("michael.davis@example.com", hash_password("davispass987")),
    ("sarah.taylor@example.com", hash_password("taylorpass567")),
    ("david.anderson@example.com", hash_password("andersonpass234")),
    ("olivia.thomas@example.com", hash_password("thomaspass890")),
    ("james.jackson@example.com", hash_password("jacksonpass101"))
]

# Sample customer insurance data
sample_customer_insurance_data = [
    (1, 101, "s3://insurance-files-tokio-m/sample-insurance-1.pdf", date(2023, 1, 15), date(2023, 1, 15)),
    (1, 102, "s3://insurance-files-tokio-m/sample-insurance-2.pdf", date(2023, 1, 15), date(2023, 1, 15)),
    (1, 101, "s3://insurance-files-tokio-m/sample-insurance-3.pdf", date(2023, 1, 15), date(2023, 1, 15)),
    (2, 102, "s3://insurance-files-tokio-m/sample-insurance-2.pdf", date(2023, 2, 1), date(2023, 2, 1)),
    (1, 103, "s3://insurance-files-tokio-m/sample-insurance-3.pdf", date(2023, 2, 15), date(2023, 2, 15)),
    (3, 104, "s3://insurance-files-tokio-m/sample-insurance-4.pdf", date(2023, 3, 1), date(2023, 3, 1)),
    (2, 105, "s3://insurance-files-tokio-m/sample-insurance-5.pdf", date(2023, 3, 15), date(2023, 3, 15)),
    (4, 106, "s3://insurance-files-tokio-m/sample-insurance-6.pdf", date(2023, 4, 1), date(2023, 4, 1)),
    (3, 107, "s3://insurance-files-tokio-m/sample-insurance-7.pdf", date(2023, 4, 15), date(2023, 4, 15)),
    (5, 108, "s3://insurance-files-tokio-m/sample-insurance-8.pdf", date(2023, 5, 1), date(2023, 5, 1)),
    (4, 109, "s3://insurance-files-tokio-m/sample-insurance-9.pdf", date(2023, 5, 15), date(2023, 5, 15)),
    (5, 110, "s3://insurance-files-tokio-m/sample-insurance-10.pdf", date(2023, 6, 1), date(2023, 6, 1))
]
# Insert customer data query
insert_customer_query = sql.SQL("""
INSERT INTO customers ( email,password) VALUES (%s, %s) RETURNING customer_id
""")

# Insert customer insurance data query
insert_customer_insurance_query = sql.SQL("""
INSERT INTO customer_insurance
(customer_id, insurance_id, customer_policy_url, created_at, updated_at)
VALUES (%s, %s, %s, %s, %s)
""")

try:
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Create tables
    cur.execute(create_customers_table_query)
    cur.execute(create_customer_insurance_table_query)
    print("Tables created successfully")

    # Insert customer data
    customer_ids = []
    for customer in sample_customers:
        try:
            email, hashed_password = customer
            cur.execute(insert_customer_query, (email, hashed_password.decode('utf-8')))
            customer_id = cur.fetchone()
            if customer_id is not None:
                customer_ids.append(customer_id[0])
            else:
                print(f"Failed to insert customer: {customer}")
        except psycopg2.Error as e:
            print(f"Error inserting customer {customer}: {e}")

    print(f"Inserted {len(customer_ids)} customers")

    # Insert customer insurance data
    inserted_insurance = 0
    for insurance in sample_customer_insurance_data:
        try:
            if inserted_insurance < len(customer_ids):
                cur.execute(insert_customer_insurance_query, (customer_ids[inserted_insurance],) + insurance[1:])
                inserted_insurance += 1
            else:
                print(f"Skipping insurance record due to insufficient customers: {insurance}")
        except psycopg2.Error as e:
            print(f"Error inserting insurance record {insurance}: {e}")

    print(f"Inserted {inserted_insurance} insurance records")
    conn.commit()
    print(f"{len(sample_customers)} customers and {len(sample_customer_insurance_data)} insurance records inserted successfully")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if conn:
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")
