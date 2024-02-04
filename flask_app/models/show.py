from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Show:
    db_name = "mvcusersshows"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.comment = data['comment']
        self.network = data['network']
        self.date = data['date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO shows (title, comment, network, date, user_id) VALUES (%(title)s, %(comment)s, %(network)s, %(date)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
     

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.db_name).query_db(query)
        shows = []
        if results:
            for show in results:
                shows.append(show)
        return shows

    @classmethod
    def get_show_by_id(cls, data):
        query = "SELECT * FROM shows LEFT JOIN users on shows.user_id = users.id WHERE shows.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            comments = []
            query2 = "SELECT * FROM comments left join users on comments.user_id = users.id where comments.show_id = %(id)s ORDER BY comments.created_at DESC;"
            result2 = connectToMySQL(cls.db_name).query_db(query2, data)
            if result2:
                for comment in result2:
                    comments.append(comment)
            result[0]['comments'] = comments
            query3 = "SELECT users.firstName, users.lastName FROM likes left join users on likes.user_id = users.id where likes.book_id = %(id)s;"
            result3 = connectToMySQL(cls.db_name).query_db(query3, data)
            likes = []
            if result3:
                for like in result3:
                    likes.append(like)
            result[0]['likes'] = likes
            return result[0]
        return False
    
    @classmethod
    def get_comment_by_id(cls, data):
        query = "SELECT * FROM comments where comments.id = %(id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    @classmethod
    def get_show_by_title(cls, data):
        query = "SELECT * FROM shows where shows.title = %(title)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shows where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_all_show_comments(cls, data):
        query ="DELETE FROM comments where comments.show_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE shows set title=%(title)s, comment = %(comment)s, network=%(network)s, date = %(date)s WHERE shows.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    # functionality for comments
    @classmethod
    def addComment(cls, data):
        query = "INSERT INTO comments (comment, user_id, show_id) VALUES (%(comment)s, %(user_id)s, %(show_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def update_comment(cls, data):
        query = "UPDATE comments set comment = %(comment)s where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
      

    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO likes (user_id, show_id) VALUES (%(user_id)s, %(show_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def removeLike(cls, data):
        query = "DELETE FROM likes WHERE show_id=%(book_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_users_who_liked_by_show_id(cls, data):
        query ="SELECT user_id FROM likes where show_id = %(show_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        usersId = []
        if results:
            for userId in results:
                usersId.append(userId['user_id'])
        return usersId
                

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title'])< 2:
            flash('Title should be more  or equal to 2 characters', 'title')
            is_valid = False
        if len(show['comment'])< 10:
            flash('Comment should be more  or equal to 10 characters', 'comment')
            is_valid = False
        if len(show['network'])< 1:
            flash('Network should be more  or equal to 2 characters', 'network')
            is_valid = False
        if len(show['date'])< 1:
            flash('Date is required', 'date')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_showUpdate(show):
        is_valid = True
        
        if len(show['comment'])< 10:
            flash('Comment should be more  or equal to 10 characters', 'comment')
            is_valid = False
        if len(show['network'])< 1:
            flash('Network should be more  or equal to 2 characters', 'network')
            is_valid = False
        if len(show['date'])< 1:
            flash('Price is required', 'date')
            is_valid = False
        return is_valid