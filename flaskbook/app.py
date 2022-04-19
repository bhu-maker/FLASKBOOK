from ast import Or
from  dataclasses import fields
from operator import or_
from pyexpat import model

from flask_sqlalchemy import SQLAlchemy
from flask import Flask,redirect,render_template,request,Response,session
from sqlalchemy import Column,Integer,String,Float

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost:3306/flaskdatabase'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
app.config['SECRET_KEY']='flaskdatabase'

class Book1(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255),nullable=False)
    author=db.Column(db.String(255),nullable=False)
    price=db.Column(db.Float,nullable=False)
    content=db.Column(db.Integer,nullable=False)
    # manually create table in xampp though we specified model ,table is not creating automatically





    

    def __init__(self,t="",a="",p=0.0,c=0):
        self.title=t
        self.author=a
        self.price=p
        self.content=c

    def __repr__(self) -> str:
        return f"{self.title}-{self.author}"


@app.route("/new",methods=['GET','POST'])   
def creating():
    if request.method=='GET':
        return render_template("create.html")
    else:
        obj=Book1(request.form['title'],request.form['author'],request.form['price'],request.form['content'])    
        db.session.add(obj)
        db.session.commit()
        return redirect ("/list")

@app.route("/list",methods=['GET'])
def listing():
    obj=Book1.query.all()
    return render_template("list.html",key=obj)


@app.route("/read/<int:pk>",methods=['GET'])    
def reading(pk):
    obj=Book1.query.filter_by(id=pk)
    return render_template("list.html",key=obj)

@app.route("/short",methods=['GET'])
def shorting():  
  obj=Book1.query.filter_by(content=76)
  return render_template("list.html",key=obj)

@app.route("/shorttwo/<int:d1>/<int:d2>",methods=['GET'])
def shortingtwo(d1,d2):  
  #obj=Book1.query.filter_by(content=233)
   #obj=Book1.query.filter_by(content>=56)---error
   #obj=Book1.query.filter(Book1.content>=56).all()
   #obj=Book1.query.filter(or_(Book1.content>=56,Book1.content<=233)).all()
   obj=Book1.query.filter(or_(Book1.content>=d1,Book1.content<=d2)).all()
   return render_template("list.html",key=obj)

app.route("/sthree/<str:u>",methods=['GET'])
def shortingthree(u):  
  obj=Book1.query.filter(Book1.title.like(f"{u}%")).all()
  #obj=Book1.query.filter(Book1.title.like(f"ha%")).all()
  #obj=Book1.query.filter_by(title="half")---error
  return render_template("list.html",key=obj)

@app.route("/del/<int:pk>",methods=['GET'])
def deleting(pk):
    obj=Book1.query.filter_by(id=pk).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect("/list")








if __name__ == '__main__':
     app.run(debug=True)




