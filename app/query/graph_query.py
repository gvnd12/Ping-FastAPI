from pydantic_settings import BaseSettings

class QueryClass(BaseSettings):
    CREATE_USER_QUERY:str = """
    CREATE(user:User{
    _id:$_id,
    user_code:$user_code,
    name:$name,
    username:$username,
    account_privacy:$account_privacy})
    RETURN user.user_code AS user_code
    """

    CHECK_DUPLICATE:str = """
    RETURN EXISTS {
      MATCH (u:User {username: $username})
    } AS username_exists;
    """

    LOGIN_USER_QUERY:str = """
    MATCH (user:User{username:$username,password:$password})
    RETURN user.username AS username,user.password AS password
    """

    DELETE_QUERY:str = """
    MATCH (user:User {_id: $_id})
    DETACH DELETE user
    """

    def edit_query(update_dict:dict):
        for key, value in update_dict.items():
            EDIT_QUERY:str = f"""
            MATCH (user:User)
            WHERE user.user_id = $_id
            SET user.{key} = ${value}
            """
        return EDIT_QUERY

    def search_query(key:str):
        SEARCH_QUERY:str = f"""
        MATCH (user:User)
        WHERE toLower(user.{key}) STARTS WITH toLower($param)
        RETURN user
        """
        return SEARCH_QUERY

    FOLLOW_QUERY:str = """
    MATCH (current_user:User {_id: $current_user_id}), (user_to_follow:User {_id:$user_to_follow_id})
    CREATE (current_user)-[:FOLLOWS]->(user_to_follow)
    """

queryclass = QueryClass()