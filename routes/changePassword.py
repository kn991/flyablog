from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
    sha256_crypt,
    changePasswordForm,
)

changePasswordBlueprint = Blueprint("changePassword", __name__)


@changePasswordBlueprint.route("/changepassword", methods=["GET", "POST"])
def changePassword():
    if "userName" in session:
        form = changePasswordForm(request.form)
        if request.method == "POST":
            oldPassword = request.form["oldPassword"]
            password = request.form["password"]
            passwordConfirm = request.form["passwordConfirm"]
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select password from users where userName = "{session["userName"]}"'
            )
            if sha256_crypt.verify(oldPassword, cursor.fetchone()[0]):
                if oldPassword == password:
                    flash("новый пароль не может совпадать со старым", "error")
                    message("1", "НОВЫЙ ПАРОЛЬ НЕ МОЖЕТ СОВПАДАТЬ СО СТАРЫМ")
                elif password != passwordConfirm:
                    message("1", "ПАРОЛИ ДОЛЖНЫ СОВПАДАТЬ")
                    flash("пароли должны совпадать", "error")
                elif oldPassword != password and password == passwordConfirm:
                    newPassword = sha256_crypt.hash(password)
                    connection = sqlite3.connect("db/users.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        f'update users set password = "{newPassword}" where userName = "{session["userName"]}"'
                    )
                    connection.commit()
                    message(
                        "2", f'ПОЛЬЗОВАТЕЛЬ: "{session["userName"]}" ПОМЕНЯЛ СВОЙ ПАРОЛЬ'
                    )
                    session.clear()
                    flash("вы должны зайти с новым паролем", "success")
                    return redirect("/login")
            else:
                flash("старый пароль неверный", "error")
                message("1", "СТАРЫЙ ПАРОЛЬ НЕВЕРНЫЙ")

        return render_template("changePassword.html", form=form)
    else:
        message("1", "ПОЛЬЗОВАТЕЛЬ НЕ ВОШЕЛ")
        flash("вы должны зайти в аккаунт", "error")
        return redirect("/login")
