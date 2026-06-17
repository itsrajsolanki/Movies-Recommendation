from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import numpy as np
import pickle
import pandas as pd
import urllib.parse

app = FastAPI()

# Load files
movies_data=pickle.load(open("Movies_NewData.pkl","rb"))
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

data=np.load("Newsimilarity.npz")
similarity = data['similarity']

users_file = "users.pkl"

def load_users():
    try:
        return pickle.load(open(users_file, "rb"))
    except FileNotFoundError:
        users = {"admin": "password"}
        pickle.dump(users, open(users_file, "wb"))
        return users


def save_users(users):
    pickle.dump(users, open(users_file, "wb"))


users = load_users()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates"), name="static")
app.mount("/images", StaticFiles(directory="."), name="images")

def recommend(movie: str):
    if movie not in movies["title"].values:
        return["Movie not found"]
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movies_list:
        recommended_movies.append(
            movies.iloc[i[0]].title
        )

    return recommended_movies

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    movie_list = movies['title'].values.tolist()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "movies": movie_list
        }
    )


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "request": request,
            "error": None
        }
    )


@app.post("/login", response_class=HTMLResponse)
async def login_submit(request: Request):
    username = None
    password = None
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
    else:
        body = await request.body()
        decoded = body.decode("utf-8", errors="ignore")
        parsed = urllib.parse.parse_qs(decoded)
        username = parsed.get("username", [None])[0]
        password = parsed.get("password", [None])[0]

    if username in users and users[username] == password:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "request": request,
            "error": "Invalid username or password."
        }
    )


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(
        request,
        "signup.html",
        {
            "request": request,
            "error": None,
            "success": False
        }
    )


@app.post("/signup", response_class=HTMLResponse)
async def signup_submit(request: Request):
    username = None
    password = None
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
    else:
        body = await request.body()
        decoded = body.decode("utf-8", errors="ignore")
        parsed = urllib.parse.parse_qs(decoded)
        username = parsed.get("username", [None])[0]
        password = parsed.get("password", [None])[0]

    if not username or not password:
        return templates.TemplateResponse(
            request,
            "signup.html",
            {
                "request": request,
                "error": "Username and password are required.",
                "success": False
            }
        )

    if username in users:
        return templates.TemplateResponse(
            request,
            "signup.html",
            {
                "request": request,
                "error": "This username is already taken.",
                "success": False
            }
        )

    users[username] = password
    save_users(users)

    return templates.TemplateResponse(
        request,
        "signup.html",
        {
            "request": request,
            "error": None,
            "success": True,
            "username": username
        }
    )


# API route
@app.get("/recommend/{movie}")
async def get_recommendations(movie: str):

    recommendations = recommend(movie)

    return {
        "recommendations": recommendations
    }
    
@app.get("/movie/{movie}")
async def movie_details(movie:str):
    movie_row=movies_data[movies_data["title"]==movie]
    
    if movie_row.empty:
        return{"error":"Movie not found"}
    
    movie_row=movie_row.iloc[0]
    
    return{
        "title":movie_row["title"],
        "genres":movie_row["genres"],
        "keywords":movie_row["keywords"],
        "overview":movie_row["overview"],
        "cast":movie_row["cast"],
        "director":movie_row["crew"],
        "release_date":movie_row["release_date"]
    }

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    uvicorn.rin("maim:app", host-"0.0.0.0", port=port)
