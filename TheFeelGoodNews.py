from flask import Flask, render_template_string
import request

app = Flask(__name__)

@app.route('/')
def home():
    api_key = '865100d9a4704df99c24c3e3542c1226'
    url = f'https://newsapi.org/v2/everything?q=funny+technology&apiKey={api_key}&pageSize=10&sortBy=Popularity'

    try:
        response = requests.get(url)
        data = response.json()
        article = data['articles'][0] if data['articles'] else None
    except requests.exceptions.RequestException as e:
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>THE FEEL GOOD NEWS</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    display: flex;
                }
            </style>
        </head>
        <body>
            <h1>No internet connection. Please try reconnecting.</h1>
        </body>
        </html>
        ''')

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>THE FEEL GOOD NEWS</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                display: flex;
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
                    <p>{{ article.content }}</p>
                </div>
            {% else %}
                <p>No articles found.</p>
            {% endif %}
        </div>
    </body>
    </html>
    ''', article=article)

if __name__ == '__main__':
    app.run(debug=True)
