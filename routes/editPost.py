from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    currentDate,
    currentTime,
    render_template,
    Blueprint,
    createPostForm,
)

editPostBlueprint = Blueprint("editPost", __name__)


@editPostBlueprint.route("/editpost/<int:postID>", methods=["GET", "POST"])
def editPost(postID):
    if "userName" in session:
        connection = sqlite3.connect("db/posts.db")
        cursor = connection.cursor()
        cursor.execute(f"select id from posts")
        posts = str(cursor.fetchall())
        if str(postID) in posts:
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(f"select * from posts where id = {postID}")
            post = cursor.fetchone()
            message("2", f'ПОСТ: "{postID}" НАЙДЕН')
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select userName from users where userName="{session["userName"]}"'
            )
            if post[4] == session["userName"]:
                form = createPostForm(request.form)
                form.postTitle.data = post[1]
                form.postTags.data = post[2]
                form.postContent.data = post[3]
                if request.method == "POST":
                    postTitle = request.form["postTitle"]
                    postTags = request.form["postTags"]
                    postContent = request.form["postContent"]
                    if postContent == "":
                        flash("ПОСТ НЕ ДОЛЖЕН БЫТЬ ПУСТЫМ", "error")
                        message(
                            "1",
                            f'ПОСТ НЕ МОЖЕТ БЫТЬ ПУСТЫМ: "{session["userName"]}"',
                        )
                    else:
                        connection = sqlite3.connect("db/posts.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            f'update posts set title = "{postTitle}" where id = {post[0]}'
                        )
                        cursor.execute(
                            f'update posts set tags = "{postTags}" where id = {post[0]}'
                        )
                        cursor.execute(
                            f'update posts set content = "{postContent}" where id = {post[0]}'
                        )
                        cursor.execute(
                            f'update posts set lastEditDate = "{currentDate()}" where id = {post[0]}'
                        )
                        cursor.execute(
                            f'update posts set lastEditTime = "{currentTime()}" where id = {post[0]}'
                        )
                        connection.commit()
                        message("2", f'пост: "{postTitle}" изменен')
                        flash("Пост изменили", "success")
                        return redirect(f"/post/{post[0]}")

                return render_template(
                    "/editPost.html",
                    title=post[1],
                    tags=post[2],
                    content=post[3],
                    form=form,
                )
            else:
                flash("этот пост не ваш", "error")
                message(
                    "1",
                    f'Этот пост не принадлежит: "{session["userName"]}"',
                )
                return redirect("/")
        else:
            message("1", f'Пост: "{postID}" не найден')
            return render_template("404.html")
    else:
        message("1", "Ползователь не вошел")
        flash("Вам нужно войти в аккаунт, чтобы редактировать пост", "error")
        return redirect("/login")
