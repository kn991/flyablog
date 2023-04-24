from helpers import (
    session,
    sqlite3,
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
)

dashboardBlueprint = Blueprint("dashboard", __name__)


@dashboardBlueprint.route("/dashboard/<userName>")
def dashboard(userName):
    if "userName" in session:
        if session["userName"].lower() == userName.lower():
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select * from posts where author = "{session["userName"]}"'
            )
            posts = cursor.fetchall()
            connection = sqlite3.connect("db/comments.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select * from comments where lower(user) = "{userName.lower()}"'
            )
            comments = cursor.fetchall()
            if posts:
                showPosts = True
            elif not posts:
                showPosts = False
            if comments:
                showComments = True
            elif not comments:
                showComments = False
            return render_template(
                "/dashboard.html",
                posts=posts,
                comments=comments,
                showPosts=showPosts,
                showComments=showComments,
            )
        else:
            message(
                "1",
                f'ЭТА ПАНЕЛЬ НЕ ПРИНАДЛЕЖИТ: "{session["userName"]}"',
            )
            return redirect(f'/dashboard/{session["userName"].lower()}')
    else:
        message("1", "ДОСТУП К ПАНЕЛИ ТОЛЬКО ПОСЛЕ РЕГИСТРАЦИИ")
        flash("вы должны зарегистрироваться", "error")
        return redirect("/login/redirect=&dashboard&user")
