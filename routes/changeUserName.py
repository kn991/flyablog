from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
    changeUserNameForm,
)

changeUserNameBlueprint = Blueprint("changeUserName", __name__)


@changeUserNameBlueprint.route("/changeusername", methods=["GET", "POST"])
def changeUserName():
    if "userName" in session:
        form = changeUserNameForm(request.form)
        if request.method == "POST":
            newUserName = request.form["newUserName"]
            newUserName = newUserName.replace(" ", "")
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select userName from users where userName = "{newUserName}"'
            )
            userNameCheck = cursor.fetchone()
            if newUserName.isascii():
                if newUserName == session["userName"]:
                    flash("это ваш юзернейм", "error")
                else:
                    if userNameCheck == None:
                        cursor.execute(
                            f'update users set userName = "{newUserName}" where userName = "{session["userName"]}" '
                        )
                        connection.commit()
                        connection = sqlite3.connect("db/posts.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            f'update posts set Author = "{newUserName}" where author = "{session["userName"]}" '
                        )
                        connection.commit()
                        connection = sqlite3.connect("db/comments.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            f'update comments set user = "{newUserName}" where user = "{session["userName"]}" '
                        )
                        connection.commit()
                        message(
                            "2",
                            f'Пользователь: "{session["userName"]}" поменял юзернейм на "{newUserName}"',
                        )
                        session["userName"] = newUserName
                        flash("юзернейм изменен", "success")
                        return redirect(f"/user/{newUserName.lower()}")
                        flash(
                            "Этот юзернейм уже занят.", "error"
                        )
            else:
                flash("юзернейм содержит непонятные символы", "error")

        return render_template("changeUserName.html", form=form)
    else:
        return redirect("/")
