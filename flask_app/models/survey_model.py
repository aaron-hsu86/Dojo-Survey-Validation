from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Dojos:

    DB = 'dojo_survey_schema'
    tables = 'dojos'

    def __init__(self, data) -> None:
        self.name = data['name']
        self.location = data['location']
        self.language = data['language']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = f'SELECT * FROM {cls.tables};'
        results = connectToMySQL(cls.DB).query_db(query)
        dojos = []
        if results:
            for dojo in results:
                dojos.append( cls(dojo) )
        return dojos
    
    @classmethod
    def get_one(cls, id):
        query = f'SELECT * FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = f'''INSERT INTO {cls.tables} (name, location, language, comment) 
                VALUES (  %(name)s, %(location)s, %(language)s, %(comment)s  );'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = f'''UPDATE {cls.tables}
                SET name = %(name)s, location = %(location)s, language = %(language)s, comment = %(comment)s
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_dojo(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if 'location' not in data:
            flash('Please select location')
            is_valid = False
        return is_valid