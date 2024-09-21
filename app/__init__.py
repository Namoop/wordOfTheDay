import sqlite3
from time import sleep

from flask import Flask, request
from flask_apscheduler import APScheduler
from flask_svelte import render_template

from app.python.randword import randword

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    posts = [dict(post) for post in posts]
    conn.close()
    return posts

@app.route("/")
def index():
    posts = get_posts()
    return render_template("index.html", name="Flask Svelte", posts=posts)

# ...
from feedgen.feed import FeedGenerator
from flask import make_response
# ...

@app.route('/rss')
def rss():
    fg = FeedGenerator()
    fg.title('Feed title')
    fg.description('Feed description')
    fg.link(href=request.host_url, rel='self')

    for article in get_posts():
        article_id = str(article['id'])
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=request.host_url + article_id)
        fe.description(article['content'])
        fe.guid(article_id, permalink=False) # Or: fe.guid(article.url, permalink=True)
        fe.author(name=article['author'], email=article['author_email'])
        fe.pubDate(article['created'] + " GMT")

    response = make_response(fg.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')

    return response

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# run randword_task every day at noon pacific time and 6pm pacific time
@scheduler.task('cron', id='randword', hour='12,18', timezone='US/Pacific')
def randword():
    data = None
    retries = 4
    for x in range(0, retries):  # try 4 times
        str_error = None
        try:
            data = randword()
        except Exception as e:
            str_error = str(e)
            pass

        if str_error:
            sleep(2)  # wait for 2 seconds before trying to fetch the data again
            pass
        else:
            break
        if x == retries - 1:
            raise Exception("Failed to fetch data after " + str(retries) + " retries")

    content = data['word'] + "\n" + data['definition']

    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content, author, author_email) VALUES (?, ?, ?, ?)',
                 ("Word of the Day", content, "The Wordmaster", "capinski@berkeley.edu"))
    conn.commit()
    conn.close()

# Route to get a random word
@app.route("/randword")
def get_randword():
    return randword()