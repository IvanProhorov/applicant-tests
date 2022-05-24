from typing import List

import requests
from pydantic import BaseModel, ValidationError


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class PostList(BaseModel):
    all: List[Post]


class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str


class CommentList(BaseModel):
    all: List[Comment]


url_post = 'http://jsonplaceholder.typicode.com/posts'
url_comments = 'http://jsonplaceholder.typicode.com/comments'

resp = requests.get(url=url_post)
posts = resp.json()
resp = requests.get(url=url_comments)
comments = resp.json()

try:
    post_list = PostList(all=posts)
except ValidationError as e:
    print(e)
try:
    comment_list = CommentList(all=comments)
except ValidationError as e:
    print(e)
temp = {}
for post in post_list.all:
    if post.userId not in temp.keys():
        temp[post.userId] = [1, 0]
    else:
        temp[post.userId][0] += 1
    for comment in comment_list.all:
        if comment.postId == post.id:
            temp[post.userId][1] += 1
results = {}
for result in temp.items():
    results[result[0]] = result[1][1] / result[1][0]
print(results)
