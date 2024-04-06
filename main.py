import ssl
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
from schemas import Student, StudentUpdate, AddressUpdate
from validators import createStudentValidator
from pymongo.errors import PyMongoError
from util import merge_dicts

uri = "mongodb+srv://Sarthak:KILLER_7sv08@cosmocloud-db-1.9plqi5e.mongodb.net/?retryWrites=true&w=majority&appName=cosmocloud-db-1"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["cc-db"]
collection = db["cc-collection"]

# Create FastAPI instance
app = FastAPI()


# Add a Student
@app.post("/students", status_code=201, response_model=None)
def create_student(student: Student):
    try:
        student_id = uuid.uuid4()
        student.id = str(student_id)
        validationOutput = createStudentValidator(student)
        if(validationOutput[0] == False):
            raise HTTPException(status_code= 400, detail= validationOutput[1])
        result = collection.insert_one(student.model_dump())
        return {"id": str(student_id)} 
    except PyMongoError as e:
        print(str (e))
        raise HTTPException(status_code=500, detail=f"Failed to add student")
    

# Get all students (filter by country or age or both)
@app.get("/students", response_model=List[Student])
def list_students(country: Optional[str] = None, age: Optional[int] = None):
    try:
        query = {}
        if country:
            query["address.country"] = country
        if age is not None:
            query["age"] = {"$gte": age}
        students = list(collection.find(query))

        return students

    except PyMongoError as e:
        print(str (e))
        raise HTTPException(status_code=500, detail=f"Failed to fetch students")
    

#Get Student by ID
@app.get("/students/{id}", response_model=Student)
def get_student(id: str):
    try:
        student =collection.find_one({"id": id})

        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")

    except PyMongoError as e:
        print(str (e))
        raise HTTPException(status_code=500, detail=f"Failed to fetch student")
    

# Update student (only update the given keys)
@app.patch("/students/{id}", status_code=204)
def update_student(id: str, student_update: StudentUpdate):
    try:
        student_data = student_update.model_dump()
        
        student = collection.find_one({"id": id})

        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        student = Student.model_validate(student)
        merged_update_query = merge_dicts(student.model_dump(), student_data)
        print(merged_update_query)
        result = collection.update_one({"id": id}, {"$set": merged_update_query})

        return None

    except PyMongoError as e:
        print(str (e))
        raise HTTPException(status_code=500, detail=f"Failed to update student")

    
# Delete student by ID
@app.delete("/students/{id}", response_model=None)
def delete_student(id: str):
    try:
        result = collection.delete_one({"id": id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student deleted successfully"}

    except PyMongoError as e:
        print(str (e))
        raise HTTPException(status_code=500, detail=f"Failed to delete student")
    
