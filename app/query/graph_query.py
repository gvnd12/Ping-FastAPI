CREATE_USER_QUERY = """
CREATE(user:User{
_id:$_id,
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
MATCH (user:User {_id: $_id})
DETACH DELETE user
"""

def edit_query(update_dict:dict):
    for key, value in update_dict.items():
        EDIT_QUERY = f"""
        MATCH (user:User)
        WHERE user.user_id = $_id
        SET user.{key} = ${value}
        """
    return EDIT_QUERY

def search_query(key:str):
    SEARCH_QUERY = f"""
    MATCH (user:User)
    WHERE user.{key} = $param
    RETURN user
    """
    return SEARCH_QUERY