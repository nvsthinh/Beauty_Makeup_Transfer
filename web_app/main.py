from fastapi import FastAPI,Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
# from typing import Optional
from random import randrange

app  = FastAPI()

class Post(BaseModel):
    title:str
    content: str
    id:int
    publish: bool = True
    rating: int = None

post_warehouse = [{"title":"Title of post 1", "content":"content of post 1", "id":"1","publish":"false"},
              {"title":"The ride was so cooooolll!!!!!", "content":"Look at this picture", "id":"2","publish":"false", "rating":5}]
def find_post(id):
    for p in post_warehouse:
        if p['id'] == id:
            return p

def find_index(id):
    if id == 'latest':
        i = len(post_warehouse)-1
        return i
    else:
        for i, p in enumerate(post_warehouse):
            if p['id'] == id:
                return i
def find_id(index):
    for i,p in enumerate(post_warehouse):
        if i == index:
            return p['id']

@app.get('/')
def root():
    return {"message": "hello to user1 api"}

@app.get("/posts")
def getpost():
    return {"data ": post_warehouse}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def createposts(newpost:Post):
    new_post = newpost.model_dump()
    # new_post['id'] = str(randrange(0,1000000))
    post_warehouse.append(new_post)
    print(new_post)
    return {"data": f"{new_post}"}
    

@app.get('/posts/{id}')
def get_post(id:str, response : Response):
    if id == 'latest':
        id = len(post_warehouse)-1
        posts = post_warehouse[id]
    else:
        posts = find_post(id)

    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND 
        # return{'message': f"post with id {id} was not found"}
    else:
        return {'post_detail':f"{posts}"}
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
        # deleting post
        # find the index in the array that has required id
        # post_warehouse.pop(index)
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    post_warehouse.pop(index)
    print(type(index))
    return {'message': "Post was successfully deleted"}

# @app.put("/posts/{id}")
# def update_post(id:str,post:Post):
#     index = find_index(id)
#     if index == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
#     else:
#         post_dict = post.model_dump()
#         post_dict["id"] = id
#         post_warehouse[index] = post_dict
#         return {'updated_post:': f"{post_warehouse[index]}"}

@app.put("/posts/{id}")
def update_post(id:str,post:Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    else:
        post_dict = post.model_dump()
        post_dict["id"] = find_id(index)
        post_warehouse[index] = post_dict
        return {'updated_post:': f"{post_warehouse[index]}"}
