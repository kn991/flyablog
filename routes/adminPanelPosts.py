from helpers import sqlite3, render_template, Blueprint, session, redirect

adminPanelPostsBlueprint = Blueprint("adminPanelPosts", __name__)


@adminPanelPostsBlueprint.route("/admin/posts")
@adminPanelPostsBlueprint.route("/adminpanel/posts")
def adminPanelPosts():
    if "userName" in session:
        connection = sqlite3.connect("db/users.db")
        cursor = connection.cursor()
        cursor.execute(
            f'select role from users where userName = "{session["userName"]}"'
        )
        role = cursor.fetchone()[0]
        if role == "admin":
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute("select * from posts")
            posts = cursor.fetchall()
            return render_template(
                "dashboard.html", posts=posts, showPosts=True
            )
        else:
            return redirect("/")
    else:
        return redirect("/")
