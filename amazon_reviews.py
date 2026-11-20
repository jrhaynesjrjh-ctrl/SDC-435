# ==========================================================
# Jonathan Haynes
# Assignment 4 - MongoDB CRUD Application
# November 18, 2026
#
# Purpose:
# This program performs CRUD operations using
# the Amazon ReviewData MongoDB collection.
# ==========================================================


from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Connect to Amazon database
db = client["Amazon"]

# Connect to ReviewData collection
collection = db["ReviewData"]


# ==========================================================
# Create a new review document
# ==========================================================
def create_review():
    print("\n--- Create Review ---")

    review = {
        "review_id": input("Enter Review ID: "),
        "product_id": input("Enter Product ID: "),
        "reviewer_id": input("Enter Reviewer ID: "),
        "stars": input("Enter Stars (1-5): "),
        "review_body": input("Enter Review Body: "),
        "review_title": input("Enter Review Title: "),
        "language": input("Enter Language: "),
        "product_category": input("Enter Product Category: ")
    }

    result = collection.insert_one(review)

    print("\nReview Added Successfully")
    print("MongoDB ID:", result.inserted_id)


# ==========================================================
# Retrieve one document using find_one()
# ==========================================================
def find_one_review():

    print("\n--- Find One Review ---")

    review = collection.find_one()

    if review:

        print("\nDocument Found")

        for key, value in review.items():
            print(f"{key}: {value}")

    else:
        print("No documents found")


# ==========================================================
# Find reviews greater than or equal to chosen stars
# ==========================================================
def find_reviews_greater_equal():

    print("\n--- Reviews Greater Than Or Equal To Stars ---")

    stars = input("Enter minimum stars: ")

    results = collection.find(
        {"stars": {"$gte": stars}}
    )

    count = 0

    for review in results:

        print("\nReview ID:", review.get("review_id"))
        print("Stars:", review.get("stars"))
        print("Title:", review.get("review_title"))

        count += 1

    print("\nDocuments Found:", count)


# ==========================================================
# Find reviews less than chosen stars
# ==========================================================
def find_reviews_less_than():

    print("\n--- Reviews Less Than Stars ---")

    stars = input("Enter maximum stars: ")

    results = collection.find(
        {"stars": {"$lt": stars}}
    )

    count = 0

    for review in results:

        print("\nReview ID:", review.get("review_id"))
        print("Stars:", review.get("stars"))
        print("Title:", review.get("review_title"))

        count += 1

    print("\nDocuments Found:", count)


# ==========================================================
# Search review titles
# ==========================================================
def search_review_title():

    print("\n--- Search Review Title ---")

    word = input("Enter word to search for: ")

    results = collection.find(
        {"review_title": {"$regex": word, "$options": "i"}}
    )

    count = 0

    for review in results:

        print("\nReview ID:", review.get("review_id"))
        print("Title:", review.get("review_title"))

        count += 1

    print("\nDocuments Found:", count)


# ==========================================================
# Search review body
# ==========================================================
def search_review_body():

    print("\n--- Search Review Body ---")

    word = input("Enter word to search for: ")

    results = collection.find(
        {"review_body": {"$regex": word, "$options": "i"}}
    )

    count = 0

    for review in results:

        print("\nReview ID:", review.get("review_id"))
        print("Review Body:", review.get("review_body"))

        count += 1

    print("\nDocuments Found:", count)


# ==========================================================
# Update a document
# ==========================================================
def update_review():

    print("\n--- Update Review ---")

    review_id = input("Enter review_id to update: ")

    document = collection.find_one(
        {"review_id": review_id}
    )

    if document is None:
        print("Review not found")
        return

    print("\nAvailable Fields")
    print("review_id")
    print("product_id")
    print("reviewer_id")
    print("stars")
    print("review_body")
    print("review_title")
    print("language")
    print("product_category")

    field = input("\nEnter field to update: ")
    value = input("Enter new value: ")

    collection.update_one(
        {"review_id": review_id},
        {"$set": {field: value}}
    )

    print("Review Updated Successfully")


# ==========================================================
# Delete one review
# ==========================================================
def delete_review():

    print("\n--- Delete Review ---")

    review_id = input("Enter review_id to delete: ")

    result = collection.delete_one(
        {"review_id": review_id}
    )

    if result.deleted_count > 0:
        print("Review Deleted")
    else:
        print("Review Not Found")


# ==========================================================
# Delete all reviews
# ==========================================================
def delete_all_reviews():

    print("\n--- Delete All Reviews ---")

    confirm = input(
        "Type YES to delete all reviews: "
    )

    if confirm.upper() == "YES":

        result = collection.delete_many({})

        print(
            f"{result.deleted_count} documents deleted"
        )

    else:
        print("Operation Cancelled")


# ==========================================================
# Delete collection
# ==========================================================
def delete_collection():

    print("\n--- Delete Collection ---")

    confirm = input(
        "Type DELETE to delete ReviewData collection: "
    )

    if confirm.upper() == "DELETE":

        collection.drop()

        print("ReviewData collection deleted")

    else:
        print("Operation Cancelled")


# ==========================================================
# Display Menu
# ==========================================================
def display_menu():

    print("\n")
    print("=" * 50)
    print("AMAZON REVIEW DATABASE")
    print("=" * 50)
    print("1. Create Review")
    print("2. Find One Review")
    print("3. Find Reviews >= Stars")
    print("4. Find Reviews < Stars")
    print("5. Search Review Title")
    print("6. Search Review Body")
    print("7. Update Review")
    print("8. Delete Review")
    print("9. Delete All Reviews")
    print("10. Delete Collection")
    print("11. Exit")
    print("=" * 50)


# ==========================================================
# Main Program Loop
# ==========================================================
while True:

    display_menu()

    choice = input("Enter Choice: ")

    if choice == "1":
        create_review()

    elif choice == "2":
        find_one_review()

    elif choice == "3":
        find_reviews_greater_equal()

    elif choice == "4":
        find_reviews_less_than()

    elif choice == "5":
        search_review_title()

    elif choice == "6":
        search_review_body()

    elif choice == "7":
        update_review()

    elif choice == "8":
        delete_review()

    elif choice == "9":
        delete_all_reviews()

    elif choice == "10":
        delete_collection()

    elif choice == "11":
        print("Program Ended")
        break

    else:
        print("Invalid Choice")

client.close()