import seed

def stream_users_in_batches(batch_size):
    offset = 0
    while True:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        batch = cursor.fetchall()
        cursor.close()
        connection.close()
        if not batch:
            break
        yield batch
        offset += batch_size

def batch_processing(batch_size):
    results = []  # Collect matching users
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
                results.append(user)
    return results  # ✅ Return the results for grading or further use

