from project1.models import User , Posts , LikedPosts
from flask import *
from flask_login import LoginManager, login_manager, login_user, logout_user,  login_required, UserMixin, current_user 
from project1 import db , app
from datetime import datetime
import calendar

@app.route('/')
def index():
    return render_template("parallax_1.html")


@app.route('/signin')
def signin():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pass')
    res = User.query.filter_by(email=email , password = password).first()
    remember = True if request.form.get('rem') else False
    print(remember)
    if not res:
        flash('Wrong email or password')
        return redirect(url_for('signin'))
    
    login_user(res , remember = remember)
    return redirect(url_for('like'))


@app.route('/signupget')
def signupget():
    return render_template("how_signup.html")


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('pass')
    email = request.form.get('email')
    print(name, username, email, password)
    user = User.query.filter_by(email=email).first()
    if user:
        flash("Account already exixts. LOGIN")
        return redirect(url_for('signin'))
    new_user = User(username=username, name=name, email=email,
                    password=password)
    db.session.add(new_user)
    db.session.commit()
    flash("Account created. LOGIN")
    return redirect(url_for('signin'))


@app.route('/like')
@login_required
def like():
    p = Posts.query.all()
    #print(type(p))
    #print(current_user.id) 
    u = LikedPosts.query.filter_by(user_id = current_user.id).all()
    if u:
        #print(u)
        lipos = []
        new_list = []
        for x in u:
            lipos.append(x.post_id)
        #print(current_user.name , "liked posts"  , lipos)
        for n in p :
            if n.id  not in lipos:
                print(n)
                new_list.append(n)
            else:
                continue
        print("new posts" , new_list)
        if(new_list == []):
            flash("You have viewed all the posts")
            return render_template("disp_post.html" ) 
        return render_template("disp_post.html", data=new_list,  user = current_user.id )
    else:
        po = Posts.query.all()
        return render_template("disp_post.html" , data = po)


@app.route('/post_like', methods=['POST'])
def post_like():
    like_rev = request.get_json('likes')
    #print(like_rev)
    val = list(like_rev.values())
    postid = int(val[0])
    #print("Post id : ", postid)
    #Querying for likes
    req = Posts.query.filter(Posts.id == postid).first()
    print(req)
    nm = req.likes
    req.likes = nm + 1
    db.session.commit()
    req = Posts.query.filter(Posts.id == postid).first()

    #adding to liked_post table
    u = LikedPosts(user_id = current_user.id , post_id = val)
    db.session.add(u)
    db.session.commit()

    res = make_response(
        jsonify({"message": "ok", "postid": req.id, "likes": req.likes}), 200)
    return res

@app.route('/account')
@login_required
def account():
    det = User.query.filter_by(id = current_user.id).first()
    postbyuser = Posts.query.filter_by(userid = current_user.id).all()
    print(postbyuser)
    print(det)
    return render_template("account.html" , data = det , posts = postbyuser)


@app.route('/update' , methods=['POST'])
@login_required
def update():
    new_det = request.get_json('details')
    data = list(new_det.values())
    for i in data:
        print(i)
    det = User.query.filter_by( id = current_user.id).first()
    if det.name != data[0]:
        det.name = data[0]
    if det.username != data[1]:
        det.username = data[1]
    if det.email != data[2]:
        det.email = data[2]
    if det.password != data[3]:
        det.password = data[3]
    db.session.commit()
    new_data = User.query.filter_by( id = current_user.id).first()
    result = make_response(jsonify({"message" : "DETAILS UPDATED" , "name":new_data.name , "username":new_data.username , "email":new_data.email , "password":new_data.password}) , 200)
    return result

#liked by
@app.route('/liked_by' , methods = ['POST'])
def liked_post():
    num = request.get_json('postid')
    data = list(num.values())
    liked = LikedPosts.query.filter_by(post_id = data[0]).all()
    names = []
    for x in liked:
        print(x.user_id)
        u = User.query.filter_by(id = x.user_id).first()
        names.append(u.name)
    print(names)
    j_names = json.dumps(names)
    print(j_names)
    res = make_response(jsonify({"message":"People who liked known" , "name":j_names}) , 200)
    return res

#posting a post
@app.route('/mypost')
@login_required
def mypost():
    return render_template("mypost.html")

@app.route('/rev_post' , methods = ['POST'])
def rev_post():
    rev = request.get_json('send_post')
    po = list(rev.values())
    title = po[0]
    bdy = po[1]
    print("title:" , title , "body:" , po[1])
    t = str(datetime.now())
    d = t[:t.find(" ")]
    ti = t[t.find(" ")+1:t.find(".")-3]
    x = datetime.strptime(d , "%Y-%m-%d")
    fi = ti + " " + str(x.day) +" "+ calendar.month_name[x.month]
    print(fi)
    f = Posts(userid = current_user.id , title = title , post = bdy , regdate = fi)
    db.session.add(f)
    db.session.commit()
    print(f"Post added of {current_user.name}")
    res = make_response(jsonify({"message":"ALL OK !"}))
    return res 



#deleting a post
@app.route('/delete' , methods = ['POST'])
def delete():
    rev = request.get_json('del')
    data = list(rev.values())
    poid = int(data[0])
    uid = int(data[1])
    print(poid , uid)
    check = Posts.query.filter_by(id = poid , userid = uid).first()
    print(check)
    if check:
        db.session.delete(check)
        db.session.commit()
        return make_response(jsonify({"message":"Post Deleted"}))
    else:
        return make_response(jsonify({"message":"ALL OK! but now such post"}))

#updating a post
@app.route('/updatepost/<int:postid>')
def updatepost(postid):
    print(postid)
    u = Posts.query.filter_by(id = postid , userid = current_user.id).first()
    print(u)

    return render_template("updatepost.html" , data = u)

#to update post in db
@app.route('/updatedpost' , methods=['POST'])
def updatedpost():
    rev = request.get_json('newpost')
    data = list(rev.values())
    print(data[0], data[1] , data[2])
    newp = Posts.query.filter_by(id = data[0] , userid = current_user.id).first()
    if(newp.title != data[1] and len(data[1]) != 0):
        newp.title = data[1]
        
    if(newp.post != data[2] and len(data[2]) != 0):
        newp.post = data[2]
       
    t = str(datetime.now())
    d = t[:t.find(" ")]
    ti = t[t.find(" ")+1:t.find(".")-3]
    x = datetime.strptime(d, "%Y-%m-%d")
    fi = ti + " " + str(x.day) + " " + calendar.month_name[x.month]
    newp.regdate = fi
    db.session.commit()
    return make_response(jsonify({"message":"Your Post Is Updated"}))


@app.route('/logout')
@login_required
def logout():
    print(current_user.name)
    logout_user()
    
    return redirect(url_for('index'))
