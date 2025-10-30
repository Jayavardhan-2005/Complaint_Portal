from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo()

class User:
    @staticmethod
    def create(email, password, role):
        return mongo.db.users.insert_one({
            'email': email,
            'password': password,
            'role': role
        })

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})

class Complaint:
    @staticmethod
    def create(user_id, department, description):
        return mongo.db.complaints.insert_one({
            'user_id': user_id,
            'department': department,
            'description': description,
            'status': 'Pending',
            'solution': ''
        })

    @staticmethod
    def find_by_user_id(user_id):
        return mongo.db.complaints.find({'user_id': user_id})

    @staticmethod
    def find_all():
        return mongo.db.complaints.find()

    @staticmethod
    def update(complaint_id, solution, status, department):
        return mongo.db.complaints.update_one(
            {'_id': ObjectId(complaint_id)},
            {'$set': {'solution': solution, 'status': status, 'department': department}}
        )