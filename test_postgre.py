from fastapi import FastAPI, Form
from fastapi.responses import Response
import psycopg2
from fastapi.templating import Jinja2Templates

DB_NAME = "notes"
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASSWORD = "qwerty"
connection = psycopg2.connect(dbname = DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
templates = Jinja2Templates(directory="templates")

username = "abehod_y"

query = "SELECT username, note FROM tb_notes;"

cur = connection.cursor()
cur.execute(query)
res = cur.fetchall()
print("\n".join(str(x[1]) for x in res))