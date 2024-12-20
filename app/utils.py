# Add utility functions here, such as age validation or formatting strings
def validate_age(age):
    try:
        age = int(age)
        if age <= 0:
            raise ValueError("Age must be a positive number.")
        return age
    except ValueError:
        return None
