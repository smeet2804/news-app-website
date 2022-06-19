from datetime import datetime
import json
from newsapi.newsapi_client import NewsApiClient
from essential_generators import DocumentGenerator

gen = DocumentGenerator()
from urllib.parse import unquote

from fastapi import FastAPI
import urllib.parse

print(unquote(
    "https%3A%2F%2Fwww.thetimes.co.uk%2Farticle%2Fineos-owner-sir-jim-ratcliffe-makes-late-4billion-bid-for-chelsea-sg99tzdxj"))
import psycopg2

# establishing the connection


# Executing an MYSQL function using the execute() method
# cursor.execute("select version()")
#
# # Fetch a single row using fetchone() method.
# data = cursor.fetchone()
# print("Connection established to: ",data)

# Closing the connection
# conn.close()


# Setting auto commit false
# conn.autocommit = True

# Creating a cursor object using the cursor() method

# Preparing SQL queries to INSERT a record into the database.


newsapi = NewsApiClient(api_key='e5aadfb7ba204aadb59dcec9f6f3d268')

top_headlines = newsapi.get_top_headlines(language='en')

Headlines = top_headlines['articles']
count=0
if Headlines:
    for articles in Headlines:
        count=count+1
        cursor.execute("INSERT INTO NEWS (URL,TITLE,AUTHOR,DESCRIPTION,PUBLISHEDAT,IMAGEURL,CONTENT) VALUES(%s, %s, %s,%s,%s,%s,%s)", (articles["url"], articles["title"],articles["author"],articles["description"],articles["publishedAt"],articles["urlToImage"],gen.paragraph(20,25)+"\n"+gen.paragraph(20,25)+"\n"+gen.paragraph(20,25)))
#        cursor.execute('''INSERT INTO NEWS (URL,TITLE,AUTHOR,DESCRIPTION,PUBLISHEDAT,CONTENT,IMAGEURL) VALUES (title_inp, articles["title"],articles["author"],articles["description"],articles["publishedAt"],articles["urlToImage"],gen.paragraph(20,25)+"\n"+gen.paragraph(20,25)+"\n"+gen.paragraph(20,25))''')
        b = articles['title'][::-1].index("-")
        if "news" in (articles['title'][-b + 1:]).lower():
            print(f"{articles['title'][-b + 1:]}: {articles['title'][:-b - 2]}.")
        else:
            print(f"{articles['title'][-b + 1:]} News: {articles['title'][:-b - 2]}.")
else:
   print(f"Sorry no articles found for, Something Wrong!!!")
#
# print(count)
# Commit your changes in the database
# conn.commit()
print("Records inserted........")

app = FastAPI()


@app.get("/api/news")
async def get_news_from_db():
    #    return query_db("select * from news limit %s", (20,))
    return query_db("select * from news limit %s", (20,))


@app.get("/api/news/")
async def get_news_from_url(url_inp: str):
    #    return query_db("select * from news limit %s", (20,))
    #    url_inp="https://"+unquote(url_inp)
    return query_db("select * from news where url= %s", (url_inp,))


#    return query_db("select * from news where url= %s", (unquote(url_inp),))


def query_db(query, args=(), one=False):
    #    cur = db().cursor()
    conn = psycopg2.connect(
        database="newsDB", user='postgres', password='smeet', host='127.0.0.1', port='5432'
    )
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    cursor.execute(query, args)
    print(args)
    #        records = cursor.fetchone()
    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.connection.close()
    return (r[0] if r else None) if one else r

# my_query = query_db("select * from news limit %s", (3,))
#
# json_output = json.dumps(my_query)
# Closing the connection
# conn.close()


# print(gen.paragraph(20,25)+"\n"+gen.paragraph(20,25)+"\n"+gen.paragraph(20,25))
