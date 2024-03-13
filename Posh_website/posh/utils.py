import hashlib

def generate_unique_id(phone_number, email):
    # Concatenate phone number and email
    unique_string = f"{email}{phone_number}"
    
    # Use hashlib to generate a unique hash
    hashed_string = hashlib.sha512(unique_string.encode()).hexdigest()
    
    # Return the first 10 characters of the hash
    # You can adjust the length as per your requirement
    return hashed_string[:10].upper()
