import asyncio
import websockets
import json
from essential_generators import DocumentGenerator
import db_connection
import services

gen = DocumentGenerator()
async def echo(websocket):
    cursor,conn = db_connection.dbConnection().getConnection()
    Headlines= services.Service().fetch_news()
    if Headlines:
        for articles in Headlines:
            print(articles)
            print_json = json.dumps(articles)
            await websocket.send(print_json)
            #        time.sleep(10)
            await asyncio.sleep(20)
            try:
                cursor.execute(
                    "INSERT INTO NEWS (URL,TITLE,AUTHOR,DESCRIPTION,PUBLISHEDAT,IMAGEURL,CONTENT) VALUES(%s, %s, %s,%s,%s,%s,%s)",
                    (articles["url"], articles["title"], articles["author"], articles["description"],
                     articles["publishedAt"], articles["urlToImage"],
                     gen.paragraph(20, 25) + "<br>" + gen.paragraph(20, 25) + "<br>" + gen.paragraph(20, 25)))
                conn.commit()

            except:
                continue

#    conn.commit()
    conn.close()

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())