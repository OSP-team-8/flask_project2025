from flask import Flask, render_template, request
import sys

application = Flask(__name__)

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

@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # just log for now; backend can wire later
        print("로그인 시도:", request.form)
        return render_template("list.html")
    return render_template("login.html")


@application.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print("회원가입 데이터:", request.form)  # backend teammate will handle later
        return render_template("login.html")
    return render_template("signup.html")

@application.route("/wishlist")
def wishlist():
    return render_template("wishlist.html")


if __name__ == "__main__":
    application.run(host="0.0.0.0")