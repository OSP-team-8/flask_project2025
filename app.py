from flask import Flask, render_template, request, flash, redirect, url_for, session
# import database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

@application.route("/")
def hello():
    return render_template("index.html") #index.html을 홈화면에 연결

@application.route("/list")
def view_list():
    return render_template("list.html")

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    # if DB.insert_user(data,pw_hash):
    #     return render_template("login.html")
    # else:
    #     flash("user id already exist!")
    #     return render_template("signup.html")

@application.route("/submit_item", methods=['POST'])
def reg_item_submit():

    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form

    #결과 화면 로그 생성
    print("====== 상품 등록 데이터 수신 ======")
    print(f"Item name: {data.get('name')}")
    print(f"Seller ID: {data.get('seller')}")
    print(f"Address: {data.get('addr')}")
    print(f"Email: {data.get('email')}")
    print(f"Category: {data.get('category')}")
    print(f"Credit Card?: {data.get('card')}")
    print(f"Status: {data.get('status')}")
    print(f"Phone: {data.get('phone')}")
    print(f"Image Filename: {image_file.filename}")
    print("===================================")
    
    return render_template("submit_item_result.html", data = data,
                           img_path = "static/images/{}".format(image_file.filename))

if __name__ == "__main__":
    application.run(host="0.0.0.0")