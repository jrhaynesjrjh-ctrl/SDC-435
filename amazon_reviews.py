# Name: John Haynes
# Assignment: Python Application Accessing a Column Family Database
# Date: 11/25/2026
# Purpose:
# Create a menu-driven Cassandra application that imports
# Amazon review data from a JSON file and performs CRUD
# operations on a Cassandra column family database.

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import os

# --------------------------------------------------
# Connect to Cassandra
# --------------------------------------------------

auth = PlainTextAuthProvider(
    username="cassUser",
    password="cassPass"
)

cluster = Cluster(
    ["localhost"],
    port=9042,
    auth_provider=auth
)

session = cluster.connect()

# --------------------------------------------------
# Create Amazon Keyspace
# --------------------------------------------------

session.execute("""
CREATE KEYSPACE IF NOT EXISTS Amazon
WITH REPLICATION = {
    'class':'SimpleStrategy',
    'replication_factor':1
};
""")

session.set_keyspace("amazon")

# --------------------------------------------------
# Create Reviews Table
# --------------------------------------------------

session.execute("""
CREATE TABLE IF NOT EXISTS Reviews (
    review_id text PRIMARY KEY,
    product_id text,
    reviewer_id text,
    stars int,
    review_body text,
    review_title text,
    product_category text
);
""")

# --------------------------------------------------
# Create ProductCategories Table
# --------------------------------------------------

session.execute("""
CREATE TABLE IF NOT EXISTS ProductCategories (
    product_id text PRIMARY KEY,
    stars int,
    language text,
    product_category text
);
""")

# --------------------------------------------------
# Import JSON Dataset
# --------------------------------------------------

def import_data():

    result = session.execute(
        "SELECT COUNT(*) FROM Reviews;"
    )

    existing = list(result)[0][0]

    if existing > 0:
        print("\nDataset already loaded.\n")
        return

    filename = "dataset_en_dev.json"

    if not os.path.exists(filename):
        print("\nJSON file not found.\n")
        return

    print("\nImporting dataset...\n")

    count = 0

    with open(filename, "r", encoding="utf-8") as file:

        for line in file:

            try:

                review = json.loads(line)

                review_id = review.get("review_id", "")
                product_id = review.get("product_id", "")
                reviewer_id = review.get("reviewer_id", "")

                try:
                    stars = int(review.get("stars", 0))
                except:
                    stars = 0

                review_body = review.get("review_body", "")
                review_title = review.get("review_title", "")
                language = review.get("language", "")
                product_category = review.get(
                    "product_category",
                    ""
                )

                session.execute(
                    """
                    INSERT INTO Reviews
                    (
                        review_id,
                        product_id,
                        reviewer_id,
                        stars,
                        review_body,
                        review_title,
                        product_category
                    )
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        review_id,
                        product_id,
                        reviewer_id,
                        stars,
                        review_body,
                        review_title,
                        product_category
                    )
                )

                session.execute(
                    """
                    INSERT INTO ProductCategories
                    (
                        product_id,
                        stars,
                        language,
                        product_category
                    )
                    VALUES
                    (%s,%s,%s,%s)
                    """,
                    (
                        product_id,
                        stars,
                        language,
                        product_category
                    )
                )

                count += 1

            except Exception:
                pass

    print(f"{count} records imported.\n")


# --------------------------------------------------
# Display Categories
# --------------------------------------------------

def display_categories():

    print()

    rows = session.execute(
        """
        SELECT product_category
        FROM ProductCategories;
        """
    )

    categories = sorted(
        set(
            row.product_category
            for row in rows
            if row.product_category
        )
    )

    for category in categories:
        print(category)

    print()


# --------------------------------------------------
# High Rating Count
# --------------------------------------------------

def high_review_count():

    category = input(
        "\nWhich category would you like to "
        "check the high review count of?\n\n"
    )

    rows = session.execute(
        """
        SELECT stars, product_category
        FROM ProductCategories
        """
    )

    count = 0

    for row in rows:

        if (
            row.product_category == category
            and row.stars >= 4
        ):
            count += 1

    print()
    print(
        f"Number of 4 and 5 star reviews "
        f"in the {category} category: {count}"
    )
    print()


# --------------------------------------------------
# Low Rating Count
# --------------------------------------------------

def low_review_count():

    category = input(
        "\nWhich category would you like to "
        "check the low review count of?\n\n"
    )

    rows = session.execute(
        """
        SELECT stars, product_category
        FROM ProductCategories
        """
    )

    count = 0

    for row in rows:

        if (
            row.product_category == category
            and row.stars == 1
        ):
            count += 1

    print()
    print(
        f"Number of 1 star reviews "
        f"in the {category} category: {count}"
    )
    print()


# --------------------------------------------------
# Execute SELECT Query
# --------------------------------------------------

def user_query():

    query = input(
        "\nEnter a SELECT statement:\n\n"
    )

    if not query.lower().startswith("select"):
        print(
            "\nOnly SELECT statements "
            "are allowed.\n"
        )
        return

    try:

        rows = session.execute(query)

        print()

        for row in rows:
            print(row)

        print()

    except Exception as error:
        print("\nError:", error, "\n")


# --------------------------------------------------
# Add / Remove Columns
# --------------------------------------------------

def alter_columns():

    print("\n1. Add Column")
    print("2. Remove Column\n")

    choice = input("Choice: ")

    table = input(
        "Table name (Reviews/ProductCategories): "
    )

    column = input("Column name: ")

    try:

        if choice == "1":

            session.execute(
                f"""
                ALTER TABLE {table}
                ADD {column} text
                """
            )

            print("\nColumn added.\n")

        elif choice == "2":

            session.execute(
                f"""
                ALTER TABLE {table}
                DROP {column}
                """
            )

            print("\nColumn removed.\n")

    except Exception as error:
        print("\nError:", error, "\n")


# --------------------------------------------------
# Delete Tables
# --------------------------------------------------

def delete_tables():

    confirm = input(
        "\nDelete Reviews and "
        "ProductCategories tables? (y/n): "
    )

    if confirm.lower() == "y":

        session.execute(
            "DROP TABLE IF EXISTS Reviews;"
        )

        session.execute(
            """
            DROP TABLE IF EXISTS
            ProductCategories;
            """
        )

        print("\nTables deleted.\n")


# --------------------------------------------------
# Delete Keyspace
# --------------------------------------------------

def delete_keyspace():

    confirm = input(
        "\nDelete Amazon keyspace? (y/n): "
    )

    if confirm.lower() == "y":

        session.execute(
            "DROP KEYSPACE IF EXISTS Amazon;"
        )

        print("\nKeyspace deleted.\n")


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

import_data()

# --------------------------------------------------
# Menu Loop
# --------------------------------------------------

while True:

    print()
    print(
        "Type in a number and press enter "
        "to execute the menu option."
    )
    print()

    print("1. Display product category list")
    print("2. Display high (4+) star review count")
    print("3. Display low (1) star review count")
    print("4. Enter a query")
    print("5. Add/Remove table columns")
    print("6. Delete tables")
    print("7. Delete keyspace")
    print("8. Exit the program")
    print()

    choice = input()

    if choice == "1":
        display_categories()

    elif choice == "2":
        high_review_count()

    elif choice == "3":
        low_review_count()

    elif choice == "4":
        user_query()

    elif choice == "5":
        alter_columns()

    elif choice == "6":
        delete_tables()

    elif choice == "7":
        delete_keyspace()

    elif choice == "8":

        print("\nGoodbye.\n")

        session.shutdown()
        cluster.shutdown()

        break

    else:
        print("\nInvalid selection.\n")
