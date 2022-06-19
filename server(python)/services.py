from newsapi.newsapi_client import NewsApiClient
from essential_generators import DocumentGenerator

import db_connection

gen = DocumentGenerator()

class Service:
    def select_query_db(self, query, args=(), cursor=None, one=False):
        cursor,conn= db_connection.dbConnection().getConnection()
        cursor.execute(query, args)

        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        cursor.close()
        return (r[0] if r else None) if one else r

    def insert_query_db(self, query, args=(), cursor=None, conn=None):
        cursor,conn = db_connection.dbConnection().getConnection()
        cursor.execute(query, args)
        cursor.close()
        conn.commit()

    def fetch_news(self,inp_category=None,inp_search=None):

        newsapi = NewsApiClient(api_key='e5aadfb7ba204aadb59dcec9f6f3d268')
        if inp_search is not None:
            top_headlines = newsapi.get_top_headlines(q=inp_search,category=None,language='en')
        elif inp_category is not None:
            top_headlines = newsapi.get_top_headlines(q=None, category=inp_category, language='en')
        elif inp_category is None and inp_search is None:
            top_headlines = newsapi.get_top_headlines(q=None, category=None, language='en')
        Headlines = top_headlines['articles']

        return Headlines
