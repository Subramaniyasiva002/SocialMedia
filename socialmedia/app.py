from flask import Flask,redirect,render_template,request,url_for
from flask.globals import session,request
from flask_sqlalchemy import SQLAlchemy
from flask import flash,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_manager,UserMixin,LoginManager,login_required,logout_user
from flask_login import current_user
import os
from werkzeug.utils import secure_filename 
from datetime import datetime    #for likes and commds
from sqlalchemy.inspection import inspect  # ✅ This works with SQLAlchemy models

local_server=True
app=Flask(__name__)
app.secret_key="SS_Shiva005"


login_manager=LoginManager(app)
login_manager.login_view='login'


#db connection
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/database name'

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/leo'
db=SQLAlchemy(app)



#Configuration for handling files
app.config['UPLOAD_FOLDER']='static/uploads/'  #path important & ''
app.config['ALLOWED_EXTENSIONS']={'png','jpg','gif','jpeg'}
app.config['MAX_CONTENT_LENGTH']=16*1024*1024 #16MB 

@login_manager.user_loader                       #Login inbuilt function
def load_user(signup_id):
    return Signup.query.get(int(signup_id))




class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(60))


class Serializer(object):
    def serialize(self):
        return {c:getattr(self,c) for c in inspect(self).attrs.keys()}
    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class Signup(UserMixin,db.Model,Serializer):                     #Usemixin added 
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(50))
    lastname=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    phone_no=db.Column(db.String(10),unique=True)
    profileimage=db.Column(db.String(500))

    def get_id(self):
        return self.id
    
# for posts model
class Posts(db.Model):
    post_id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(50))
    name=db.Column(db.String(100))
    title=db.Column(db.String(100))
    description=db.Column(db.String(500))
    image=db.Column(db.String(500))
    date=db.Column(db.String(500))
    time=db.Column(db.String(500))
    likes=db.Column(db.Integer,nullable=True)      


class Comments(db.Model):
    comment_id=db.Column(db.Integer,primary_key=True)
    post_id=db.Column(db.Integer)
    comment=db.Column(db.String(500))
    commentedBy=db.Column(db.String(100))
    commentedOn=db.Column(db.String(100))

class Friends(db.Model):
    friends_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    request_id=db.Column(db.Integer)
    isAccepted=db.Column(db.String(10))

class Contact(db.Model):
    contact_id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100))
    description=db.Column(db.String(500))



@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))     #it is used for if user is not authenticated 
    data=Posts.query.all()
    return render_template("index.html",data=data)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method=='POST':
        email=request.form.get("email")
        description=request.form.get("message")
        query=Contact(email=email,description=description)
        db.session.add(query)
        db.session.commit()
        flash("We will back to you soon!","success")
        return render_template("contact.html")
    return render_template("contact.html")



@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        first_name=request.form.get("fname")
        last_name=request.form.get("lname")
        email=request.form.get("email")
        phoneno=request.form.get("number")
        password=request.form.get("pass1")
        confirmpassword=request.form.get("pass2")
        print(first_name,last_name,email,password,phoneno,confirmpassword)
        if password!=confirmpassword:
            flash("Password is not matching","warning")
            return redirect(url_for("signup"))
        
        fetchemail=Signup.query.filter_by(email=email).first()
        fetchphone=Signup.query.filter_by(phone_no=phoneno).first()    #left is DB ,Right is form value
        
        if fetchemail or fetchphone :
            flash("User already exist!","warning")
            return redirect(url_for("signup"))
        
        if len(phoneno)!=10 :
            flash("Please enter 10 Digit Number!","warning")
            return redirect(url_for("signup"))
        gen_pass=generate_password_hash(password)                 #Generate the hash value of password
        query=f"INSERT into `signup` (`firstname`,`lastname`,`email`,`password`,`phone_no`) VALUES ('{first_name}','{last_name}','{email}','{gen_pass}','{phoneno}')"
        with db.engine.begin() as conn:
            conn.exec_driver_sql(query)
            flash("signup success!","success")
            return redirect(url_for("login"))


    return render_template("signup.html")


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("pass1")
        user=Signup.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)                     #provide the login to the user
            flash("Login Successfull","success")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","info")
            return render_template("login.html")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout Successfull","primary")
    return redirect(url_for('login'))


@app.route("/test/")
def test():
    try:
        sql_query="select * from test"
        with db.engine.begin() as conn:
            response=conn.exec_driver_sql(sql_query).all()
            print(response)
        return "Database is connected"
    except Exception as e:
        return f"Database is not connected,{e}"


#for posts

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/posts",methods=['GET','POST'])
def posts():
    if request.method=="POST":
        email=request.form['email']
        name=request.form['name']
        title=request.form['title']
        description=request.form['description']
        file=request.files['file']
        date=datetime.now()
        datee=date.date()
        time=date.time()
        if file and allowed_files(file.filename):
            #save the file in upload folder
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #write the query to save into the db
            query=Posts(email=email,name=name,title=title,description=description,image=file.filename,date=datee,time=time)
            db.session.add(query)
            db.session.commit()
            flash("Post is uploaded!","info")
            return redirect(url_for('index'))  #note url qoutes is must double qoutes
        else:
            flash("Please use 'png','jpg','gif','jpeg' formate","warning")


    return render_template("posts.html")


#Logic for likes
@app.route('/like/<int:id>',methods=['GET','POST'])
def like(id):
    post=Posts.query.filter_by(post_id=id).first()
    if post.likes==None:
        post.likes=1
        db.session.commit()
    post.likes=post.likes+1
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/comment/<int:id>',methods=['GET','POST'])
def comment(id):
    if request.method=="POST":
        comment=request.form['comment']
        commentedBy=request.form['commented']
        commentedOn=datetime.now()
        query=Comments(post_id=id,comment=comment,commentedBy=commentedBy,commentedOn=commentedOn)
        db.session.add(query)
        db.session.commit()
        flash("comment Added","success")
        return redirect(url_for('index'))


@app.route("/viewcomment/<int:id>",methods=['GET','POST'])
def viewcomment(id):
    post=Comments.query.filter_by(post_id=id).all()
    return render_template("comments.html",post=post)

@app.route("/connect",methods=['GET','POST'])
def connect():
    users=Signup.query.all()
    return render_template("connect.html",users=users)

@app.route("/connectfriend/<path:ids>",methods=['GET'])
def connectFriends(ids):
    data=ids.split("/")
    users=Signup.query.all()
    d1=Friends.query.filter_by(user_id=data[1]).first()
    d2=Friends.query.filter_by(request_id=data[0]).first()
    if d1 and d2:
        flash("Request already sent","primary")
        return render_template("connect.html",users=users)
    query=Friends(user_id=data[1],request_id=data[0],isAccepted="False")
    db.session.add(query)
    db.session.commit()
    flash("Request is sent","success")

    return render_template("connect.html",users=users)



@app.route("/remove/<path:ids>",methods=['GET'])
def remove(ids):
    data=ids.split("/")
    users=Signup.query.all()
    d1=Friends.query.filter_by(user_id=data[1]).first()
    d2=Friends.query.filter_by(request_id=data[0]).first()
    if d1 and d2:
        query=f"Delete from `friends` where `friends`.`user_id`={data[1]} and `friends`.`request_id`={data[0]}"
        with db.engine.begin() as conn:
            conn.exec_driver_sql(query)
            flash("Request Cancelled","success")
            return render_template("connect.html",users=users)
    return render_template("connect.html",users=users)

@app.route("/profile",methods=['GET','POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    userdata=Signup.query.filter_by(email=current_user.email).first()
    friends=Friends.query.filter_by(user_id=current_user.id).all()
    getallposts=Posts.query.filter_by(email=current_user.email).all()
    myids=[]
    for i in friends:
        signupdata=Signup.query.filter_by(id=i.request_id).first()
        myids.append(signupdata)
    return render_template("profile.html",userdata=userdata,myids=myids,getallposts=getallposts)
        
@app.route("/editprofile/<int:id>",methods=['GET','POST'])
def editprofile(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    userdata=Signup.query.filter_by(id=id).first()
    return render_template("editprofile.html",userdata=userdata)


@app.route("/updateprofile/<int:id>",methods=['GET','POST'])
def updateprofile(id):
    userdata=Signup.query.filter_by(email=current_user.email).first()
    if request.method=="POST":
        firstname=request.form.get("fname")
        lastname=request.form.get("lname")
        email=request.form.get("email")
        phoneno=request.form.get("number")
        file=request.files['profileimage']
        if len(phoneno)!=10:
            flash("Please enter 10 Digit Number!","warning")
            return redirect(url_for("editprofile",id=id))
        if file and allowed_files(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            query=f"UPDATE `signup` SET `firstname`='{firstname}',`lastname`='{lastname}',`email`='{email}',`phone_no`='{phoneno}',`profileimage`='{file.filename}' WHERE `signup`.`id`='{id}'"
            with db.engine.begin() as conn:
                conn.exec_driver_sql(query)
                flash("Profile Update Success","success")
                return redirect(url_for('profile'))
        else:
            query1=f"UPDATE `signup` SET `firstname`='{firstname}',`lastname`='{lastname}',`email`='{email}',`phone_no`='{phoneno}' WHERE `signup`.`id`='{id}'"
            with db.engine.begin() as conn:
                conn.exec_driver_sql(query1)
                flash("Profile Update Success","success")
                return redirect(url_for('profile'))
    return render_template("profile.html",userdata=userdata)


@app.route("/accept/<path:ids>",methods=['GET'])
def acceptfriendreq(ids):
    data=ids.split("/")
    query=f"UPDATE `friends` SET `isAccepted`='{True}' WHERE `friends`.`request_id`='{data[0]}' and `friends`.user_id='{data[1]}'"
    with db.engine.begin() as conn:
        conn.exec_driver_sql(query)
        flash("Friend Request Accepted","success")
        return redirect(url_for('profile'))
    

#flask API

@app.route('/api/users',methods=['GET'])
def users():
    user={
        "username":"siva",
        "salary":10000,
        "role":"developer"
    }
    #return json.dumps(user)
    return jsonify(user)

@app.route("/api/signup",methods=['GET'])
def sign():
    data=Signup.query.all()
    return jsonify(Signup.serialize_list(data))


#for specific id data retieve
@app.route("/api/signup/<int:id>",methods=['GET'])
def signu(id):
    data=Signup.query.get(id)
    return jsonify(data.serialize())