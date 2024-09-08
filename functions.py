import hashlib
import random

# Get Login
def user_login(db, name, password):
    # Hash Code
    name = hash_code(name)

    # Confirm Name
    if not name_confirmation(db, name):
        return False

    salt = db.execute("SELECT id_salt FROM people WHERE person_id = ?", name)
    salt = salt[0]["id_salt"]
    password = hash_code(salt + password)

    password_confirmation = db.execute("SELECT id_key FROM people WHERE person_id = ?", name)
    password_id = password_confirmation[0]["id_key"]

    # Confirm Password
    if password == password_id:
        return True
    else:
        return False
    

# Register User
def user_register(db, name, password):
    # Hash Code
    name = hash_code(name)

    # Get Salt
    salt = str(random.randint(0, 100000000000000))
    password = salt + password
    password = hash_code(password)

    if not name_confirmation(db, name):
        db.execute("INSERT INTO people (person_id, id_key, id_salt) VALUES (?, ?, ?);", name, password, salt)


# Delete User
def user_deleter(db, name, password):
    name = hash_code(name)

    if not name_confirmation(db, name):
        return

    salt = db.execute("SELECT id_salt FROM people WHERE person_id = ?", name)

    if not salt:
        return
    
    salt = salt[0]["id_salt"]
    hashed_password = hash_code(salt + password)

    password_confirmation = db.execute("SELECT id_key FROM people WHERE person_id = ?", name)

    if not password_confirmation:
        return
    
    password_id = password_confirmation[0]["id_key"]

    if hashed_password == password_id:
        db.execute("DELETE FROM people WHERE person_id = ?", name)
        db.execute("DELETE FROM accounts WHERE person_id = ?", name)

# Name Confirmation
def name_confirmation(db, name):
    # Confirm Name
    name_confirmation = db.execute("SELECT person_id FROM people WHERE person_id = ?", (name,))

    if name_confirmation:
         return True
    else:
        return False


# Hash Code
def hash_code(string):
    # Hash Code
    sha256 = hashlib.sha256()

    sha256.update(string.encode("utf-8"))

    return sha256.hexdigest()
