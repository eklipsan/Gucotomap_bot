from workers.database import create_connection

con = create_connection()
cur = con.find({})
for user in cur:
    if user.get("user_id", None) is not None:
        user_id = user['user_id']
        updates = {'$unset': {
            'map_invalid_state': 1
        }}
        con.update_one(filter={"user_id": user_id}, update=updates)

cur2 = con.find({})
for user in cur2:
    print(user)
