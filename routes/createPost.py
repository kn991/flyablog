from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    addPoints,
    currentDate,
    currentTime,
    render_template,
    Blueprint,
    createPostForm,
)

createPostBlueprint = Blueprint("createPost", __name__)


@createPostBlueprint.route("/createpost", methods=["GET", "POST"])
def createPost():
    if "userName" in session:
        form = createPostForm(request.form)
        if request.method == "POST":
            postTitle = request.form["postTitle"]
            postTags = request.form["postTags"]
            postContent = request.form["postContent"]
            if postContent == "":
                flash("контент не может быть пустым", "error")
                message(
                    "1",
                    f'контент не может быть пустым: "{session["userName"]}"',
                )
            else:
                connection = sqlite3.connect("db/posts.db")
                cursor = connection.cursor()
                cursor.execute(
                    f"""
                    insert into posts(title,tags,content,author,views,date,time,lastEditDate,lastEditTime) 
                    values("{postTitle}","{postTags}","{postContent}",
                    "{session["userName"]}",0,
                    "{currentDate()}",
                    "{currentTime()}",
                    "{currentDate()}",
                    "{currentTime()}")
                    """
                )
                connection.commit()
                message("2", f'POST: "{postTitle}" POSTED')
                addPoints(20, session["userName"])
                flash("Вы заработали 20 очков за пост ", "success")
                return redirect("/")
        return render_template("createPost.html", form=form)
    else:
        message("1", "Пользователь не вошел")
        flash("вам нужно войти чтобы создать пост", "error")
        return redirect("/login")
