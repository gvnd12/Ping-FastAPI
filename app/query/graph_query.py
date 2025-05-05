CREATE_USER_QUERY = """
CREATE(user:User{
user_code:$user_code,
name:$name,
username:$username,
account_privacy:$account_privacy})
RETURN user.user_code AS user_code
"""

CHECK_DUPLICATE = """
RETURN EXISTS {
  MATCH (u:User {username: $username})
} AS username_exists;
"""

LOGIN_USER_QUERY = """
MATCH (user:User{username:$username,password:$password})
RETURN user.username AS username,user.password AS password
"""

DELETE_QUERY = """
MATCH (user:User {username: $username})
DETACH DELETE user
"""

EDIT_QUERY = """
MATCH (user:User {username: $username})
SET user.username = $newUsername
"""

def search_query(key):
    SEARCH_QUERY = f"""MATCH (n:user) WHERE n.{key} = $value RETURN n"""
    return SEARCH_QUERY