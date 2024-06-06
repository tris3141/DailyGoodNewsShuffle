from flask import Flask, render_template_string
import requests
import random
import os
from datetime import datetime

app = Flask(__name__)

INDEX_FILE = "index.txt"


def get_random_index():
    today = datetime.today().date()
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as file:
            data = file.read().split(",")
            last_date = datetime.strptime(data[0], "%Y-%m-%d").date()
            last_index = int(data[1])
            if last_date == today:
                return last_index

    new_index = random.randint(0, 9)
    with open(INDEX_FILE, "w") as file:
        file.write(f"{today},{new_index}")
    return new_index


@app.route("/")
def home():
    api_key = ""
    url = f"https://newsapi.org/v2/everything?q=funny+technology&apiKey={api_key}&pageSize=10&sortBy=Popularity"

    response = requests.get(url)
    data = response.json()
    index = get_random_index()
    article = data["articles"][index] if data["articles"] else None

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
                margin: 20px;
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
                max-width: 1200px;
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
        </style>
    </head>
    <body>
        <div class="article-container">
            {% if article %}
                <div class="article-image">
                    <a href="{{ article.url }}" target="_blank">
                        <img src="{{ article.urlToImage }}" alt="{{ article.title }}">
                    </a>
                </div>
                <div class="article-content">
                    <h2>{{ article.title }}</h2>
                    <p>{{ article.description }}</p>
                    
                </div>
            {% else %}
                <p>No articles found.</p>
            {% endif %}
        </div>
    </body>
    </html>
    """,
        article=article,
    )


if __name__ == "__main__":
    app.run(debug=True)
