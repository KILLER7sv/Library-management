from schemas import Address, Student

def createStudentValidator(student: Student):
    if student.address is None:
        return (False, "Address Not Found")
    if student.name is None:
        return (False, "Name Not Found")
    if student.age is None:
        return (False, "Age Not Found")
    if student.address.city is None:
        return (False, "City Not Found")
    if student.address.country is None:
        return (False, "Country Not Found")
    return (True, "Success")
