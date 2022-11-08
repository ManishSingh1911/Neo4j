import collections
from flask import Flask, request, jsonify
class NeoFunc:
    def InsertMovieAndShow(self,input_body,session):
        q1 = """MATCH (movie:Movie{title: $title}) RETURN movie"""
        map = {"title":input_body['title']}
        try:
            results = session.run(q1,map)
            records = list(results)
            if(len(records)>=1):
                return "Movie and Show already exists in database"
            else:
                q2 = """create(movie:Movie{show_id:$show_id, type:$type, title:$title, release_year:$release_year, rating:$rating, duration:$duration, description:$description})"""
                map2 = {"title":input_body['title'],"show_id":input_body['show_id'],"type":input_body['type'],"release_year":input_body['release_year'],"description":input_body['description'],"rating":input_body['rating'],"duration":input_body['duration']}
                session.run(q2,map2)
                return "inserted successfully!!!"
        except Exception as e:
            return ("Cannot create movie with the data provided")
    def UpdateMovieAndShow(self, input_body,session,fname):
        try:
            q1 = """MATCH (movie:Movie{title:$title}) SET movie.title = $new_title,movie.description= $description, movie.rating = $rating RETURN movie"""
            map = {"title":fname,"new_title":input_body['title'],"description":input_body['description'],"rating":input_body['rating']}
            session.run(q1,map)
            return "Movie or Show Updated Successfully!!"
        except Exception as e:
            return("Unable to update Movie with the data provided")
    def DeleteMovieAndShow(self, session,fname):
        try:
            q1 = """MATCH (Movie {title:$title}) DETACH DELETE Movie"""
            map1 = {"title":fname}
            session.run(q1,map1)
            return "Movie or Show deleted Successfully!!"
        except Exception as e:
            return("Unable to delete Movie with the data provided")

    def GetMovieAndShowDetail(self, session,fname):
        try:
            collections_Data = []
            q1 = """MATCH (movie:Movie{title:$title})-[r:DISTRIBUTED_IN|ACTED_IN|DIRECTED]-(data) RETURN movie, collect(data.name) as relation_data"""
            map= {"title":fname}
            collections = session.run(q1,map)
            data = collections.data()
            for movie_collection in data:
                json = {
                    "Movie":movie_collection["movie"],
                    "Country,Directors,Actors":movie_collection["relation_data"]
                }
                collections_Data.append(json)
            return collections_Data
        except:
            return "unable to get the data please check the input"

    def GetMovieAndShows(self,session):
        try:
            collections_Data = []
            q1 = """MATCH (movie:Movie) RETURN movie"""
            collections = session.run(q1)
            data = collections.data()
            for movie_collection in data:
                collections_Data.append(movie_collection["movie"])
            return collections_Data
        except:
            return "unable to get the data please check the input"