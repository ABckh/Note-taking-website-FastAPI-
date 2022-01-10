from fastapi import FastAPI, Form, Request
from fastapi.responses import Response, HTMLResponse
import psycopg2
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from pydantic import BaseModel

DB_NAME = "notes"
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASSWORD = "qwerty"
templates = Jinja2Templates(directory="templates")
connection = psycopg2.connect(dbname = DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

app = FastAPI()
USERNAME = "abehod_y"

class Note(BaseModel):
    username: str
    note_id: Optional[str] = '-1'
    note: str



@app.get("/", response_class = HTMLResponse)
def start_page(request: Request):
    res = read_all_notes()
    context = {
        "request": request,
        "content": res,
    }
    return templates.TemplateResponse('home.html', context)


    

@app.post("/", response_class=HTMLResponse )
def add_note_html(request: Request,note: str = Form(...)):
    add_new_note_db(username=USERNAME, note=note)
    res = read_all_notes()
    context = {
        "request": request,
        "content": res[0:],
        "boolean": True,
    }
    return templates.TemplateResponse('home.html', context)


@app.post("/del", response_class=HTMLResponse)
async def delete_note(request: Request):
    tab = await request.json()
    noteId = tab['noteId']
    with connection.cursor() as cur:
        query = "DELETE FROM tb_notes WHERE note_id = '{}'".format(noteId)
        cur.execute(query)
        connection.commit()
        cur.close()

    

def configure_static(app: FastAPI):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def add_new_note_db(username: str, note: str):
    with connection.cursor() as cur:
        create_tb = "CREATE TABLE IF NOT EXISTS tb_notes (" \
            "username VARCHAR(50) NOT NULL," \
           "note_id BIGSERIAL PRIMARY KEY, " \
            "note VARCHAR (2000) NOT NULL);"
        cur.execute(create_tb)
        insert_note = "INSERT INTO tb_notes (username, note)"\
                "VALUES (%s, %s);"
        val = (username, note)        
        cur.execute(insert_note, val)
        connection.commit()

        cur.close()

def read_all_notes(): 
        with connection.cursor() as cur:
            create_tb = "CREATE TABLE IF NOT EXISTS tb_notes (" \
            "username VARCHAR(50) NOT NULL," \
           "note_id BIGSERIAL PRIMARY KEY, " \
            "note VARCHAR (2000) NOT NULL);"
            cur.execute(create_tb)
            query = "SELECT note_id, note FROM tb_notes WHERE username = '{}';".format(USERNAME)
            cur.execute(query)
            fetch_all_notes = cur.fetchall()
            #all_notes = '\n'.join(str(x[0]) for x in fetch_all_notes)
            list_with_notes = []
            for elem in fetch_all_notes:
                list_with_notes.append(elem)
            return list_with_notes

@app.get("/static/index.js")
def return_js():
    with open("static/index.js", "r") as f:
        result = f.read()
    return result