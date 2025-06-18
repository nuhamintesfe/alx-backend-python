import seed

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    cursor.close()
    connection.close()

def average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    avg = total_age / count if count else 0
    print(f"Average age of users: {avg:.2f}")

if __name__ == "__main__":
    average_age()
