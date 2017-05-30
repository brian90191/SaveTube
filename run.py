import os
from flask import Flask, url_for, render_template, request, session, redirect
from modles import method
from modles.user import user
from modles.video import video
from common.database import Database

app = Flask(__name__)
app.secret_key = "brian@gmail.com"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route("/")
def hello():
    return render_template("index.html")

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route("/login", methods=['GET', 'POST'])
def login_method():
    if request.method == 'POST':
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        check = user.account_valid(account, password)
        if check is True:
            session['account'] = account
            # session['email'] = user.find_user_data(account).get('email')
            return redirect("/")
        else:
            session.clear()
            message = "Your account or password is wrong."
            return render_template("home.html", fail_msg=message)
    else:
        return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register_method():
    if request.method == 'POST':
        account = request.form['reg-InputAccount']
        password = request.form['reg-InputPassword']
        email = request.form['reg-InputEmail']

        register_status = user.register_user(account, password, email)
        if register_status is False:
            session.clear()
            message = "This account is exists, please change your account name."
            return render_template("home.html", fail_msg=message)
        else:
            session['account'] = account
            message = "Register is successful."
            return render_template("home.html", success_msg=message)
    else:
        return render_template("login.html")


@app.route("/logout", methods=['GET', 'POST'])
def logout_method():
    if request.method == 'POST':
        session.clear()
        message = "Successfully logout."
        return render_template("home.html", success_msg=message)
    else:
        return render_template("login.html")


@app.route("/results", methods=['GET', 'POST'])
def result_page():
    page = request.args.get("sp")
    if page is None:
        return_url = request.url
        search = request.args.get("search")
        soup = method.find_search_content(search)
        all_item = method.every_video(soup)
        all_page = method.page_bar(soup);
        return render_template("result_page.html", search=search, all_item=all_item, all_page=all_page, return_url=return_url)
    elif page is not None:
        return_url = request.url
        search = request.args.get("q")
        page = request.args.get("sp")
        current_page = request.args.get("current_page")
        value = "q={}".format(search) + "&" + "sp={}".format(page)
        soup = method.find_page_content(value)
        all_item = method.every_video(soup)
        all_page = method.page_bar(soup);
        return render_template("current_page.html", search=search, all_item=all_item, all_page=all_page,
                               current_page=current_page, return_url=return_url, int=int)
    else:
        return redirect("/")

@app.route('/favorite', methods=["GET", "POST"])
def add_favorite():
    if session['account']:
        if request.method == 'POST':
            return_url = request.form['return_url']
            account = session['account']
            tag = request.form['tag']
            title = request.form['title']
            link = request.form['link']
            img = request.form['img']
            time = request.form['time']

            video_data = video.find_video(account, title, link)
            if video_data.count() <= 0:
                video(account, tag, title, link, img, time).save_to_DB()
            else:
                video.remove_video(account, title, link)
            return redirect(return_url)
        else:
            account = session['account']
            user_video = video.find_video_data(account)
            favorite_tags = video.find_favorite_tags(account)
            return render_template("favorite.html", user_video=user_video, favorite_tags=favorite_tags)
    else:
        return redirect("/")


@app.route('/load_ajax', methods=["GET", "POST"])
def load_ajax():
    if request.method == "POST":
        search = request.args.get("q")
        page = request.args.get("sp")
        current_page = request.args.get("current_page")
        value = "q={}".format(search) + "&" + "sp={}".format(page)
        soup = method.find_page_content(value)
        all_item = method.every_video(soup)
        all_page = method.page_bar(soup);

        return str({"search": search, "page": page, "current_page": current_page, "all_item": all_item,
                    "all_page": all_page})

@app.route("/download")
def download():
    value = request.args.get("value")
    download_type, url = value.split("&")
    if download_type == "MP3":
        method.download_mp3(url)
        return render_template("download.html")
    elif download_type == "MP4":
        method.download_mp4(url)
        return render_template("download.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9900))
    app.run(debug=True, host='127.0.0.1', port=port)
