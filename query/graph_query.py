create_user_query ="""
create(n:user{
name:$name,
username:$username,
password:$password,
mobile_no:$mobile_no,
date_of_birth:$date_of_birth,
gender:$gender,
account_privacy:$account_privacy})
"""