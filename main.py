from flask import Flask, render_template_string  # type: ignore
import requests  # type: ignore

app = Flask(__name__)


@app.route("/")
def home():
    api_key = ""
    url = f'https://newsapi.org/v2/everything?q=funny+tiktok+"feel good"+technology+&apiKey={api_key}&pageSize=1&sortBy=popularity'

    response = requests.get(url)
    data = response.json()
    article = data["articles"][0] if data["articles"] else None

    return render_template_string(
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The Feel Good Press</title>
        <style>
    body {
    font-family: Arial, sans-serif;
    margin: 20px;
    }
 .article {
        display: flex;
        justify-content: space-between;
    }
 .article img {
        max-width: 250px;
        height: auto;
        flex: 1; /* This will allow the image to take up the available space */
    }
 .article-content {
        flex: 2; /* This will allow the content to take up the remaining space */
    }

    .article h2 {
        margin-top: 0;
        margin-right: 400px;                 
    }
    .article p {
        margin-right: 400px;
    }
    h1 {
        text-align: center;
    }
        </style>
    </head>
    <body>
         <h1>The Feel Good Press</h1>
        <div class="article">
            {% if article %}
                <a href="{{ article.url }}" target="_blank">
                    <img src="{{ article.urlToImage }}" alt="{{ article.title }}">
                 <div class="article-content">
                     <h2>{{ article.title }}</h2>
                </a>
                <p>{{ article.publishedAt }}</p>
                <p>{{ article.description }}</p>
                <p>{{ article.content }}</p>
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
