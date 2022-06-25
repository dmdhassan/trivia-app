# from crypt import methods
import os
from tracemalloc import start
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # creation and configuration of the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

#CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
            )

        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS"
            )

        response.headers.add(
            "Access-Control-Allow-Origin", "*"
            )

        return response

    
    @app.route('/categories')
    def get_categories():
        categories = {}

        for category in Category.query.order_by(Category.type).all():
            id = category.id
            categories[id] = category.type

        return jsonify({
            'success': True,
            'categories': categories
        })
        

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = {}

        for category in Category.query.order_by(Category.type).all():
            id = category.id
            categories[id] = category.type
            
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_id(category_id):
        selection = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
        current_questions = paginate_questions(request, selection)

        categories = {}

        for category in Category.query.order_by(Category.type).all():
            id = category.id
            categories[id] = category.type
        
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': categories,
            'current_category': category_id
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)


            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': current_questions,
            'total_question': len(selection)
            })
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category')

        if quiz_category is None:
            abort(400)

        try:
        
            if quiz_category['id'] == 0:
                question = Question.query.filter(Question.id.notin_(previous_questions)).limit(1).one_or_none()
            else:
                question = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_(previous_questions)).limit(1).one_or_none()

            return jsonify({
                'success': True,
                'question': question.format()
                })
        except:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)
        
        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection.all())
                })

            else:
                new_question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty
                )

                new_question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': current_questions,
                'total_question': len(selection)
                })

        except:
            abort(422)


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'resource unprocessable'
        }), 422


    return app

