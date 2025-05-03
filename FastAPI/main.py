from fastapi import FastAPI
import schema

app = FastAPI()

@app.post('/blog')
def create_blog(request: schema.Blog):
    return request
