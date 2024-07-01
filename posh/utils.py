import hashlib
import os
import time
import math, random 
   
def generate_class_code(total_digits,existing_codes) :  
    digits = ''.join([str(i) for i in range(0,10)])
    code = ""  
    while True:
        for i in range(total_digits) : 
            code += digits[math.floor(random.random() * 10)] 
        if code not in existing_codes:
            # print('Code not in existing codes')
            break
    return code 

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


def generate_unique_establishment(phone_number, email):
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
    return 'ES' + hashed_string[:10].upper()

def generate_unique_ngo(phone_number, email):
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
    return 'NGO' + hashed_string[:10].upper()

def generate_unique_consultancy(phone_number, email):
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
    return 'CON' + hashed_string[:10].upper()