import redis
import psycopg2
import time

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Retry mechanism for PostgreSQL connection
while True:
    try:
        conn = psycopg2.connect(host='postgres', database='postgres', user='postgres', password='postgres')
        break
    except psycopg2.OperationalError:
        print("Database not ready, retrying in 5 seconds...")
        time.sleep(5)

cur = conn.cursor()

while True:
    votes = redis_client.keys('*')
    for vote in votes:
        count = redis_client.get(vote)
        cur.execute("INSERT INTO votes (vote) VALUES (%s);", (vote,))
        conn.commit()
        redis_client.delete(vote)
    time.sleep(5)
