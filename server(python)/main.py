from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from essential_generators import DocumentGenerator
import db_connection
import services
from fastapi.middleware.cors import CORSMiddleware

gen = DocumentGenerator()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cursor = None
conn = None


class User(BaseModel):
    name: str
    username: str
    password: str


class Authenticate(BaseModel):
    username: str
    password: str


@app.on_event("startup")
async def startup_event():
    global cursor
    global conn
    cursor, conn = db_connection.dbConnection().getConnection()


@app.post("/api/users/register-user")
async def insert_user(user: User):
    result = services.Service().select_query_db("SELECT username from login WHERE  username=%s", (user.username,),
                                                cursor, one=True)

    if result != None:  # An empty result evaluates to False.
        return {"status": "User already exists!"}

    services.Service().insert_query_db("INSERT INTO LOGIN (NAME,USERNAME,PASSWORD) VALUES(%s, %s, %s)",
                                       (user.name, user.username, user.password), cursor=cursor, conn=conn)
    return {"status": "Success"}


@app.post("/api/users/login")
async def authenticate_user(authenticate: Authenticate):
    result = services.Service().select_query_db("SELECT username from login WHERE  username=%s and password=%s",
                                                (authenticate.username, authenticate.password,),
                                                cursor, one=True)

    if result != None:  # An empty result evaluates to False.
        return {"status": "Success"}
    else:
        return {"status": "Invalid", "errorMsg": "Invalid username or password"}


@app.get("/api/news/all")
async def get_news_from_db():
    json_compatible_item_data = services.Service().select_query_db("select * from news limit %s", (30,), cursor=cursor)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/api/news/url")
async def get_news_from_url(url_inp: str):
    return services.Service().select_query_db("select * from news where url=%s", (url_inp,), cursor=cursor, one=True)


@app.get("/api/news/search/{search_inp}")
async def get_search_news(search_inp: str):
    Headlines = services.Service().fetch_news(inp_search=search_inp)
    cursor, conn = db_connection.dbConnection().getConnection()
    if Headlines:
        for articles in Headlines:
            try:
                services.Service().insert_query_db(
                    "INSERT INTO NEWS (URL,TITLE,AUTHOR,DESCRIPTION,PUBLISHEDAT,IMAGEURL,CONTENT) VALUES(%s, %s, %s,%s,%s,%s,%s)",
                    (articles["url"], articles["title"], articles["author"], articles["description"],
                     articles["publishedAt"], articles["urlToImage"],
                     gen.paragraph(20, 25) + "<br/>" + gen.paragraph(20, 25) + "<br/>" + gen.paragraph(20, 25)),
                    cursor=cursor, conn=conn)
            except:
                continue
    return Headlines


@app.get("/api/news/category/{category_inp}")
async def get_search_news(category_inp: str):
    Headlines = services.Service().fetch_news(category_inp.lower())
    if Headlines:
        for articles in Headlines:
            try:
                services.Service().insert_query_db(
                    "INSERT INTO NEWS (URL,TITLE,AUTHOR,DESCRIPTION,PUBLISHEDAT,IMAGEURL,CONTENT) VALUES(%s, %s, %s,%s,%s,%s,%s)",
                    (articles["url"], articles["title"], articles["author"], articles["description"],
                     articles["publishedAt"], articles["urlToImage"],
                     gen.paragraph(20, 25) + "<br/>" + gen.paragraph(20, 25) + "<br/>   " + gen.paragraph(20, 25)),
                    cursor=cursor, conn=conn)

            except:
                continue
    return Headlines


@app.on_event("shutdown")
def shutdown_event():
    cursor.connection.close()
