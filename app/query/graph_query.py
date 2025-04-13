CREATE_USER_QUERY = """
CREATE(user:User{
user_code:$user_code,
name:$name,
username:$username,
password:$password,
mobile_no:$mobile_no,
date_of_birth:$date_of_birth,
gender:$gender,
account_privacy:$account_privacy})
RETURN user.user_code AS user_code
"""

LOGIN_USER_QUERY = """
MATCH (n:user{username:$username,password:$password})
RETURN n.username AS username,n.password AS password
"""

DELETE_QUERY = """
MATCH (n:User {username: $username})
DETACH DELETE n
"""

EDIT_QUERY = """
MATCH (n:User {username: $username})
SET n.username = $newUsername
"""

def search_query(key):
    SEARCH_QUERY = f"""MATCH (n:user) WHERE n.{key} = $value RETURN n"""
    return SEARCH_QUERY