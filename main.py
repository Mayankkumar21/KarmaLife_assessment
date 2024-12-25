# ASSIGNMENT BY - MAYANK KUMAR
from pymongo import MongoClient
import pandas as pd
import random
import json
import os
from dotenv import load_dotenv


# Configuration
load_dotenv()
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_URI = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.wfrvy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
DB_NAME = 'university'
COLLECTION_NAME = 'students'
EXPORT_FILE = 'students.json'

def connect_to_mongodb(uri):
    try:
        client = MongoClient(uri)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        exit()

def insert_students(collection):
    courses_list = [
        {"name": "Introduction to Computer Science", "credits": 3},
        {"name": "Linear Algebra", "credits": 4},
        {"name": "Physics I", "credits": 4},
        {"name": "English Literature", "credits": 3}
    ]
    student_names = ["Mayank", "Nandini", "Sayam", "Yash", "Pratiksha", "Mini", "Aryan", "Anmol", "Tanvi", "Anu"]

    students = []
    for i in range(10):
        student = {
            "name": student_names[i],
            "age": random.randint(18, 25),
            "grades": {
                "Mathematics": random.randint(50, 100),
                "Physics": random.randint(50, 100),
                "English": random.randint(50, 100)
            },
            "courses": random.sample(courses_list, random.randint(1, 3))
        }
        students.append(student)

    collection.insert_many(students)

def retrieve_students(collection):
    try:
        print("Students above 20 with avg grade > 80:")
        result1 = collection.find({
            "$expr": {
                "$and": [
                    {"$gt": ["$age", 20]},
                    {"$gt": [
                        {"$avg": ["$grades.Mathematics", "$grades.Physics", "$grades.English"]},
                        80
                    ]}
                ]
            }
        })
        for r in result1:
            print(r)

        print("\nStudents with Mathematics grade > 90:")
        result2 = collection.find({"grades.Mathematics": {"$gt": 90}})
        for r in result2:
            print(r)

        print("\nTop 5 students by avg grades:")
        result3 = collection.find().sort([
            ("grades.Mathematics", -1),
            ("grades.Physics", -1),
            ("grades.English", -1)
        ]).limit(5)
        for r in result3:
            print(r)
    except Exception as e:
        print(f"Error retrieving data: {e}")

def update_students(collection):
    collection.update_one({"name": "Mayank"}, {"$set": {"age": random.randint(18, 25)}})
    collection.update_many({}, {"$inc": {"grades.Mathematics": random.randint(1, 10), "grades.Physics": random.randint(1, 10), "grades.English": random.randint(1, 10)}})

def delete_students(collection):
    collection.delete_many({"grades.Mathematics": {"$lt": 60}})
    collection.delete_many({"courses": {"$size": 0}})

def analyze_data(collection):
    data = list(collection.find())
    df = pd.DataFrame(data)

    print("\nMax Age:", df['age'].max())
    print("Min Age:", df['age'].min())

    average_grades = pd.DataFrame(df['grades'].tolist()).mean().reset_index()
    average_grades.columns = ['Subject', 'Average Grade']
    print(average_grades)

    return df

def export_to_json(df, file_path):
    df = df.drop('_id', axis=1)
    df.to_json(file_path, orient="records", lines=True)

def import_data(client, file_path):
    new_db = client['imported_university']
    new_collection = new_db['students']
    with open(file_path, "r") as file:
        data = [json.loads(line) for line in file]
    new_collection.insert_many(data)
    return new_collection

def query_imported_data(collection):
    print("\nTop Student in Imported Data:")
    result4 = collection.find().sort([
        ("grades.Mathematics", -1),
        ("grades.Physics", -1),
        ("grades.English", -1)
    ]).limit(1)
    for r in result4:
        print(r)

    print("\nStudents with at least 3 courses and avg grade > 85:")
    result5 = collection.find({
        "$expr": {
            "$and": [
                {"$gte": [{"$size": "$courses"}, 3]},
                {"$gt": [
                    {"$avg": ["$grades.Mathematics", "$grades.Physics", "$grades.English"]},
                    85
                ]}
            ]
        }
    })
    for r in result5:
        print(r)

if __name__ == "__main__":
    client = connect_to_mongodb(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    insert_students(collection)
    retrieve_students(collection)
    update_students(collection)
    delete_students(collection)
    df = analyze_data(collection)
    export_to_json(df, EXPORT_FILE)
    new_collection = import_data(client, EXPORT_FILE)
    query_imported_data(new_collection)
