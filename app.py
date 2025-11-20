from os import name
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"
DB = DBhandler()

@application.route("/")
def hello():
    return render_template("index.html") #index.html을 홈화면에 연결

@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)

    per_page = 6      # 한 페이지에 보여줄 아이템 개수
    per_row = 3       # 한 행에 보여줄 아이템 개수

    # 1. 전체 아이템(dict) 가져오기
    all_data = DB.get_items() or {}   # 혹시 None이면 빈 dict로
    item_counts = len(all_data)

    # 2. 이 페이지에서 보여줄 구간 계산
    start_idx = page * per_page
    end_idx = start_idx + per_page

    # dict → list로 바꿔서 슬라이싱
    page_items = list(all_data.items())[start_idx:end_idx]
    # page_items: [(key1, value1), (key2, value2), ...]

    # 3. 행(row) 단위로 자르기
    row1_items = page_items[0:per_row]               # 0~2
    row2_items = page_items[per_row:per_row*2]       # 3~5

    # 4. 페이지 개수 계산 (올림 사용)
    import math
    page_count = math.ceil(item_counts / per_page) if item_counts > 0 else 1

    return render_template(
        "list.html",
        # 템플릿에서는 그대로 for key, value in row1 / row2 사용 가능
        row1=row1_items,
        row2=row2_items,
        total=item_counts,
        page=page,
        page_count=page_count,
    )

@application.route("/view_detail/<name>/")
def view_item_detail(name):
     print("##name:", name)
     data = DB.get_item_byname(str(name))
     print("####data:", data)
     return render_template("detail.html", name = name, data = data)




# 리뷰 등록 화면 
@application.route("/reg_reviews")
def reg_reviews():
    return render_template("reg_reviews.html")

@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    return render_template("reg_reviews.html", name=name)

# 등록된 리뷰 DB에 등록 - 리뷰 등록 화면
@application.route("/reg_review", methods=['POST'])
def reg_review():
    data=request.form
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    DB.reg_review(data, image_file.filename)
    return redirect(url_for('view_review'))

#전체리뷰조회 화면
@application.route("/review")
def view_review():
    page = request.args.get("page", 0, type=int)

    per_page = 6      # 한 페이지에 보여줄 리뷰 개수
    per_row = 3       # 한 줄(row)에 보여줄 리뷰 개수
    row_count = int(per_page / per_row)

    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_reviews() or {}   # None이면 빈 dict로
    item_counts = len(data)

    # 현재 페이지에 필요한 데이터만 잘라내기
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    items_list = list(data.items())

    #교수님이랑 다른 부분 / local 쓰면 오류 나서 따로 수정함 
    rows_dict = {}  # 'data_0', 'data_1' 를 담아둘 딕셔너리

    for i in range(row_count):  
        start = i * per_row
        if start >= tot_count:   
            break

        if (i == row_count - 1) and (tot_count % per_row != 0):
            row_dict = dict(items_list[start:])
        else:
            row_dict = dict(items_list[start:start + per_row])

        rows_dict[f"data_{i}"] = row_dict

    
    row1 = rows_dict.get("data_0", {})
    row2 = rows_dict.get("data_1", {})

    return render_template(
        "review.html",
        datas=data.items(),
        row1=row1.items(),
        row2=row2.items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts / per_page) + 1),
        total=item_counts
    )


#리뷰 상세 페이지 
@application.route("/view_review_detail/<name>/")
def view_review_detail(name):
    print("### review name:", name)
    data = DB.get_review_byname(str(name))
    print("### data:", data)
    return render_template("review_detail.html", name=name, data=data)


@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")
    
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
         return render_template("login.html")
    else:
         flash("user id already exist!")
         return render_template("signup.html")
    

#좋아요 구현
@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'],name)
    return jsonify({'my_heart': my_heart})
 
@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    return jsonify({'msg': '좋아요 완료!'})
 
@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    return jsonify({'msg': '안좋아요 완료!'})



@application.route("/submit_item", methods=['POST'])
def reg_item_submit():

    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form

    DB.insert_item(data.get('name'), data, image_file.filename)

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