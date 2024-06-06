from flask import Flask, render_template_string
import requests
import random
import os
from datetime import datetime
# This line creates a Flask application instance.
app = Flask(__name__)

# This line defines the name of the index file.
INDEX_FILE = "index.txt"

# This function generates a random index based on the current date.
def get_random_index():
    # Get the current date.
    today = datetime.today().date()

    # Check if the index file exists.
    if os.path.exists(INDEX_FILE):
        # Read the data from the index file.
        with open(INDEX_FILE, "r") as file:
            data = file.read().split(",")
            last_date = datetime.strptime(data[0], "%Y-%m-%d").date()
            last_index = int(data[1])

            # Check if the last date in the index file is the same as the current date.
            if last_date == today:
                # Return the last index.
                return last_index

    # Generate a new random index.
    new_index = random.randint(0, 9)

    # Write the current date and the new index to the index file.
    with open(INDEX_FILE, "w") as file:
        file.write(f"{today},{new_index}")

    # Return the new index.
    return new_index


# This code defines a function called "home" that will be called when someone visits the home page of the website.
@app.route("/")
def home():
    # This line creates a variable called "api_key" and assigns it a value.
    api_key = ""
    
    # This line creates a variable called "url" and assigns it a value.
    # The value is a web address that we will use to get news articles.
    url = f"https://newsapi.org/v2/everything?q=funny+technology&apiKey={api_key}&pageSize=10&sortBy=Popularity"

    try:
        # This line sends a request to the web address and gets a response.
        response = requests.get(url)
        
        # This line checks if the response was successful.
        response.raise_for_status()
        
        # This line converts the response into a format that we can work with.
        data = response.json()
        
        # This line calls a function called "get_random_index" to get a random number.
        index = get_random_index()
        
        # This line gets an article from the data if there are any articles available.
        # Otherwise, it assigns None to the variable "article".
        article = data["articles"][index] if data["articles"] else None
    except requests.exceptions.RequestException:
        # This line assigns None to the variable "article" if there was an error making the request.
        article = None

    # This block of code defines the structure and content of the webpage that will be shown to the user.
    return render_template_string(
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>News Article</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0px;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: #f4f4f4;
            }
            .article-container {
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid #ccc;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                max-width: 800px;
                width: 100%;
            }
            .article-image {
                flex: 1;
                padding-right: 20px;
            }
            .article-image img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
            }
            .article-content {
                flex: 2;
            }
            .article h2 {
                margin-top: 0;
            }
            .error-message {
                color: red;
                font-weight: bold;
                text-align: center;
            }
        </style>
    </head>
    <body>
        {% if article %}
            <div class="article-container">
                <div class="article-image">
                    <a href="{{ article.url }}" target="_blank">
                        <img src="{{ article.urlToImage }}" alt="{{ article.title }}">
                    </a>
                </div>
                <div class="article-content">
                    <h2>{{ article.title }}</h2>
                    <p>{{ article.description }}</p>
                </div>
            </div>
        {% else %}
            <p class="error-message">No articles found or unable to connect to the internet. Please try again later.</p>
        {% endif %}
    </body>
    </html>
    """,
        article=article,
    )


if __name__ == "__main__":
    app.run(debug=True)
