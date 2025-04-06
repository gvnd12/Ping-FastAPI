CREATE_USER_QUERY = """
CREATE(n:user{
name:$name,
username:$username,
password:$password,
mobile_no:$mobile_no,
date_of_birth:$date_of_birth,
gender:$gender,
account_privacy:$account_privacy})
RETURN n.username AS username
"""

LOGIN_USER_QUERY = """
MATCH (n:user{username:$username,password:$password})
RETURN n.username AS username,n.password AS password
"""