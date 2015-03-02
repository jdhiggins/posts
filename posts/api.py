import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

import models
import decorators
from posts import app
from database import session

@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """Get a list of posts"""
    #Get the querystring arguments
    title_like = request.args.get("title_like")
    body_like = request.args.get("body_like")
    
    #Get and filter the posts from the database
    posts = session.query(models.Post)
    
    if title_like:
        posts = posts.filter(models.Post.title.contains(title_like))
        
    if body_like:
        posts = posts.filter(models.Post.body.contains(body_like))
    
    posts = posts.all()
        
    
    #Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/posts/<int:id>", methods=["GET", "DELETE"])
@decorators.accept("application/json")
def post_get_delete(id):
    if request.method == "GET":
        """ Single post endpoint """
        #Get the post from the database
        post = session.query(models.Post).get(id)
    
        #Check whether the post exists
        #If not return 404 with a helpful message
        if not post:
            message = "Could not find post with id {}".format(id)
            data = json.dumps({"message": message})
            return Response(data, 404, mimetype="application/json")
    
        #return the post as JSON
        data = json.dumps(post.as_dictionary())
        return Response(data, 200, mimetype="application/json")
    
    elif request.method == "DELETE":
        #Delete the post from the database
        post = session.query(models.Post).get(id)
    
    
        #Check whether the post exists
        #If not return 404 with a helpful message
        if not post:
            message = "Could not find post with id {}".format(id)
            data = json.dumps({"message": message})
            return Response(data, 404, mimetype="application/json")
    
        session.delete(post)
        session.commit()
        
        posts = session.query(models.Post).all()
    
        #return the remaining posts as JSON
        #could choose to return data as empty by doing a query on the deleted post id
        data = json.dumps([post.as_dictionary() for post in posts])
        return Response(data, 200, mimetype="application/json")




