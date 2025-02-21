from flask import Flask, render_template
import redis

app = Flask(__name__)
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.route("/")
def index():
    return '''
        <h2>Vote for your favorite option:</h2>
        <form action="/vote" method="POST">
            <button name="option" value="Cats">Vote Cats</button>
            <button name="option" value="Dogs">Vote Dogs</button>
        </form>
    '''

@app.route("/vote", methods=["POST"])
def vote():
    redis_client.incr("cats")
    return "Thanks for voting!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
