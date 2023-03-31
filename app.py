from flask import Flask
from script import get_result

app = Flask(__name__)

@app.route('/')
def index():
    result = get_result()
    return f'Output File Successfully Generated{result}'

if __name__ == '__main__':
    app.run()
