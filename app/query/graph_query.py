from pydantic_settings import BaseSettings

class QueryClass(BaseSettings):
    CREATE_USER_QUERY:str = """
    CREATE(u:User{
    _id:$_id,
    user_code:$user_code,
    name:$name,
    email:$email,
    username:$username,
    account_privacy:$account_privacy,
    is_active:$is_active,
    is_deleted:$is_deleted
    })
    RETURN u.user_code AS user_code
    """

    CHECK_DUPLICATE:str = """
    RETURN EXISTS {
    MATCH (u:User)
    WHERE u.username = $username OR u.email = $email
    } AS username_or_email_exists;
    """

    LOGIN_USER_QUERY:str = """
    MATCH (api:User{username:$username,password:$password})
    RETURN api.username AS username,api.password AS password
    """

    DELETE_QUERY:str = """
    MATCH (api:User)
    WHERE api.user_id = $_id
    SET api.is_deleted = true
    """

    @staticmethod
    def edit_query(update_dict:dict):
        for key, value in update_dict.items():
            EDIT_QUERY:str = f"""
            MATCH (api:User)
            WHERE api.user_id = $_id
            SET api.{key} = ${value}
            """
        return EDIT_QUERY

    SEARCH_QUERY:str = """
    MATCH (api:User)
    WHERE toLower(api.username) STARTS WITH toLower($param) 
    OR toLower(api.name) STARTS WITH toLower($param)
    RETURN api
    """

    FOLLOW_QUERY:str = """
    MATCH (current_user:User {_id: $current_user_id}), (user_to_follow:User {_id:$user_to_follow_id})
    CREATE (current_user)-[:FOLLOWS]->(user_to_follow)
    """

    UNFOLLOW_QUERY: str = """
    MATCH (current_user:User {_id: $current_user_id})-[r: FOLLOWS]->(user_to_unfollow:User {_id:$user_to_unfollow_id})
    DELETE r
    """

queryclass = QueryClass()