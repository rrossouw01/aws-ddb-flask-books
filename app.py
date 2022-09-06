from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from collections.abc import Mapping

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import dynamodb_handler as dynamodb

#@app.route('/')
#def root_route():
#    dynamodb.CreatATableBook()
#    return 'ddb updater'

@app.route("/")
def view_home():
    return render_template("index.html", pagetitle="Home page")

@app.route("/listbooks/<int:id>", methods=['GET'])
def list_books(id):
    if request.method == 'GET':
        ## TODO: doing GetAllBooks for now but is should be a query for only this author request.args['id']
        #return "build dynamo query for return only this author: " + request.args['id']
        response = dynamodb.GetAllBooksById(id)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            return render_template("listbooks.html", pagetitle="List Books", items = response['Items'])
        
        
        return {  
            'msg': 'Some error occcured',
            'response': response
        }

#@app.route('/get_books_by_id')
#def get_books_by_id():
#    author_id = request.form['author_id']
#    #all_options = models.Content.query.filter_by(id=option_id)
#    response = dynamodb.GetAllBooksById(author_id)
#    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
#        #return render_template("listbooks.html", pagetitle="List Books", items = response['Items'])
#        return jsonify({'items': response['Items']})
#
#    return {  
#            'msg': 'Some error occcured',
#            'response': response
#    }

@app.route("/listauthors", methods=['GET'])
def list_authors():
    if request.method == 'GET':
        response = dynamodb.GetAllAuthors()
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            return render_template("listauthors.html", pagetitle="List Authors", items = response['Items'])
        
        return {  
            'msg': 'Some error occcured',
            'response': response
        }

@app.route("/about")
def about():
    return render_template("about.html", pagetitle="About")

#  Add a book entry
#  Route: http://localhost:5000/book
#  Method : POST
@app.route('/book', methods=['GET','POST'])
def addABook():

    #data = request.get_json()
    # id, title, author = 1001, 'Angels and Demons', 'Dan Brown'
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        id = int(request.form['id'])
        author = request.form['author']
        title = request.form['title']    

    response = dynamodb.addItemToBook(id, title, author)    
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Added successfully',
        }

    return {  
        'msg': 'Some error occcured',
        'response': response
    }

# TODO: DELETE all books route


#  Read a book entry
#  Route: http://localhost:5000/book/<id>
#  Method : GET
@app.route('/book/<int:id>', methods=['GET'])
def getBook(id):
    response = dynamodb.GetItemFromBook(id)
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        
        if ('Item' in response):
            #return { 'Item': response['Item'] }
            return render_template("editbook.html", pagetitle="Edit Book", id = id, item = response['Item'])

        return { 'msg' : 'Item not found!' }

    return {
        'msg': 'Some error occured',
        'response': response
    }


#  Delete a book entry
#  Route: http://localhost:5000/book/<id>
#  Method : DELETE
@app.route('/book/<int:id>', methods=['DELETE'])
def DeleteABook(id):

    if request.method == 'POST':
        response = dynamodb.DeleteAnItemFromBook(id)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Deleted successfully',
        }

    return {  
        'msg': 'Some error occcured',
        'response': response
    } 


#  Update a book entry
#  Route: http://localhost:5000/book/<id>
#  Method : PUT
@app.route('/book/<int:id>', methods=['POST'])
def UpdateABook(id):

    #data = request.get_json()
    data = {
        'title': request.form.get('title'),
        'author_id': request.form.get('author_id')
    }
    # data = {
    #     'title': 'Angels And Demons',
    #     'author': 'Daniel Brown'
    # }

    response = dynamodb.UpdateItemInBook(id, data)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        flash('Successfull update')
        return redirect(url_for('list_books',id=0))
        #return {
        #    'msg'                : 'Updated successfully',
        #    'ModifiedAttributes' : response['Attributes'],
        #    'response'           : response['ResponseMetadata']
        #}

    return {
        'msg'      : 'Some error occured',
        'response' : response
    }   
    


# like a book - api

#  Like a book
#  Route: http://localhost:5000/like/book/<id>
#  Method : POST
@app.route('/like/book/<int:id>', methods=['POST'])
def LikeBook(id):

    response = dynamodb.LikeABook(id)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'      : 'Likes the book successfully',
            'Likes'    : response['Attributes']['likes'],
            'response' : response['ResponseMetadata']
        }

    return {
        'msg'      : 'Some error occured',
        'response' : response
    }


if __name__ == '__main__':
    app.run(host='192.168.1.111', port=5000, debug=True)
