from flask import Flask,redirect,render_template,request,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = False
app.secret_key = "asdfgh"

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120),nullable=False)
    body = db.Column(db.Text)

    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/blogs')
def blogs():
    
    blogs = Blog.query.all()
    if request.args.get("id") is not None:
        blogs = Blog.query.filter_by(id=request.args['id']).all()
    return render_template("blogs.html",blogs=blogs)

@app.route('/new_blog',methods=['GET','POST'])
def new_blog():
 
    if request.method == 'POST':
        title=request.form["title"]
        body=request.form["body"]
        title_error = ''
        body_error = ''

        if len(title)==0:
            title_error = "Please enter title"

        if len(body)==0:
            body_error = "Please enter body"

        if title_error or body_error:
            return render_template('new_blog.html',title = title,body=body,title_error=title_error,body_error=body_error)
        
        new_blog = Blog(title,body)
        db.session.add(new_blog)
        db.session.commit()

        return redirect('/blogs')
    return render_template("new_blog.html" )

if __name__ == "__main__":
    app.run()
