#!/usr/bin/env python 3.6.0

import psycopg2

""" Store global database name """
DBNAME = 'news'


def connect():
    """Connecting to the PostgreSQL database """
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        return db, c
    except BaseException:
        print("Unable to connect to the database")


def views():
    db, c = connect()
    view1 = "create or replace view popular_articles as\
             select title,count(title) as views from articles,log\
             where log.path = concat('/article/',articles.slug)\
             group by title order by views desc limit 3"

    view2 = "create or replace view popular_authors as select authors.name,\
             count(articles.author) as views from articles, log, authors\
             where log.path = concat('/article/',articles.slug) and\
             articles.author = authors.id\
             group by authors.name order by views desc"

    view3 = "create or replace view log_status as SELECT percentage, date\
             FROM\
             (SELECT (error_log.count+0.0)/all_log.count*100 AS percentage\
             , all_log.date\
             FROM\
             (SELECT COUNT(status), DATE(time), status\
             FROM log\
             WHERE status NOT IN('200 OK')\
             GROUP BY status, DATE(time)) AS error_log\
             JOIN\
             (SELECT COUNT(status), DATE(time)\
             FROM log\
             GROUP BY DATE(time)) AS all_log\
             ON error_log.date=all_log.date) AS percentage_err_log\
             WHERE percentage>1"

    c.execute(view1)
    c.execute(view2)
    c.execute(view3)

    db.commit()
    db.close()


def popular_article():
    """Prints most popular three articles """
    db, c = connect()
    query = "select * from popular_articles"
    c.execute(query)
    result = c.fetchall()
    db.close()
    print ("\nPopular Articles:\n")
    for i in range(0, len(result), 1):
        print ("\"" + result[i][0] + "\" - " + str(result[i][1]) + " views")


def popular_authors():
    """Prints most popular article authors """
    db, c = connect()
    query = "select * from popular_authors"
    c.execute(query)
    result = c.fetchall()
    db.close()
    print ("\nPopular Authors:\n")
    for i in range(0, len(result), 1):
        print ("\"" + result[i][0] + "\" - " + str(result[i][1]) + " views")


def log_status():
    """Print days on which more than 1% of requests lead to errors"""
    db, c = connect()
    query = "select * from log_status"
    c.execute(query)
    result = c.fetchall()
    db.close()
    print ("\nDays with more than 1% of errors:\n")
    for i in range(0, len(result), 1):
        error_time = str(result[i][1])
        error_percent = ("%.2f" % round((result[i][0]), 2))
        print (error_time + " - " + error_percent + "% errors")
    print (" ")


def execute_methods():
    if __name__ == '__main__':
        views()
        popular_article()
        popular_authors()
        log_status()


execute_methods()
