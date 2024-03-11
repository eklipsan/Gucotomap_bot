from workers.database import create_connection

con = create_connection()
cur = con.find({})
for user in cur:
    if 'user_id' in user.keys():
        if user.get("username", None) is None:
            user_id = user['user_id']
            updates = {'$set': {
                        'first_name': 'Unknown',
                        'last_name': 'Unknown',
                        'username': 'Unknown',
                        'is_premium': False,
                        'is_bot': False,
                        'language_code': 'en',
            }}
            con.update_one(filter={"user_id": user_id}, update=updates)

cur2 = con.find({})
for user in cur2:
    print(user)
