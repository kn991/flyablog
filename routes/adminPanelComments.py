from helpers import sqlite3, render_template, Blueprint, session, redirect

adminPanelCommentsBlueprint = Blueprint("adminPanelComments", __name__)


@adminPanelCommentsBlueprint.route("/admin/comments")
@adminPanelCommentsBlueprint.route("/adminpanel/comments")
def adminPanelComments():
    if "userName" in session:
        connection = sqlite3.connect("db/users.db")
        cursor = connection.cursor()
        cursor.execute(
            f'select role from users where userName = "{session["userName"]}"'
        )
        role = cursor.fetchone()[0]
        if role == "admin":
            connection = sqlite3.connect("db/comments.db")
            cursor = connection.cursor()
            cursor.execute("select * from comments")
            comments = cursor.fetchall()
            return render_template("adminPanelComments.html", comments=comments)
        else:
            return redirect("/")
    else:
        return redirect("/")
