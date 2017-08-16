Documentation 

 Hello :)
The purpose of this script is to create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.
it was last edited in 15/6/2017 

Prerequisites:

Python3
Vagrant
VirtualBox

Virtual Environment Setup:

-Install Vagrant and VirtualBox

-Download fullstack-nanodegree-vm repository from this link 
"https://github.com/udacity/fullstack-nanodegree-vm"

-Download the data from this link
"https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip"

-Unzip this file after downloading it. The file inside is called newsdata.sql.

-Add newsdata.sql file to the vagrant directory under VM.

-Launch vagrant with $ vagrant up, connect to the VM with $ vagrant ssh.

-Change directory to /vagrant.

-Load the data in local database using the command:
 > psql -d news -f newsdata.sql

- Run the log_analysis.py script. 


VIEWS created in the BATABASE:
 
view1 = "create or replace view popular_articles as
         select title,count(title) as views from articles,log
         where log.path = concat('/article/',articles.slug)
         group by title order by views desc limit 3"

view2 = "create or replace view popular_authors as select
         authors.name,count(articles.author) as views from 
         articles, log, authors where 
         log.path =  concat('/article/',articles.slug) and
         articles.author = authors.id
         group by authors.name order by views desc"

view3 = "create or replace view log_status as SELECT percentage,   
         date FROM(SELECT (error_log.count+0.0)/all_log.count*       
         100 AS percentage , all_log.date FROM
         (SELECT COUNT(status), DATE(time), status FROM log
         WHERE status NOT IN('200 OK')
         GROUP BY status, DATE(time)) AS error_log
         JOIN (SELECT COUNT(status), DATE(time) FROM log
         GROUP BY DATE(time)) AS all_log
         ON error_log.date=all_log.date) AS percentage_err_log
         WHERE percentage>1"


 
Contents 
the folder of the project should have the following files:
log_analysis.py
README.md
log_analysis.txt


you can contact me for any problem 
shimamostafa344@gmail.com

Thanks for Udacity full stack web developer nanodegree
















