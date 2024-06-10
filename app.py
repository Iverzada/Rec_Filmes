from flask import Flask, request, render_template
from recommendation_system import get_recommendations
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    app.logger.debug('Home page accessed')
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['user_input']
    app.logger.debug(f'Received input: {user_input}')
    recommendations = get_recommendations(user_input)
    app.logger.debug(f'Recommendations: {recommendations}')
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)