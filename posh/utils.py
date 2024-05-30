import hashlib
import os
import time

def generate_unique_id(phone_number, email):
    # Concatenate phone number and email
    unique_string = f"{email}{phone_number}"
    
    # Generate a salt
    salt = os.urandom(16).hex()
    
    # Get the current timestamp
    timestamp = str(int(time.time()))
    
    # Combine the unique string, salt, and timestamp
    combined_string = f"{unique_string}{salt}{timestamp}"
    
    # Use hashlib to generate a unique hash
    hashed_string = hashlib.sha512(combined_string.encode()).hexdigest()
    
    # Return the first 10 characters of the hash with a prefix
    return 'IN' + hashed_string[:10].upper()
