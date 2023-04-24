from helpers import session, redirect, message, Blueprint


logoutBlueprint = Blueprint("logout", __name__)


@logoutBlueprint.route("/logout")
def logout():
    match "userName" in session:
        case True:
            message("2", f'ПОЛЬЗОВАТЕЛЬ: "{session["userName"]}" ВЫШЕЛ')
            session.clear()
            return redirect("/")
        case False:
            message("1", f"ПОЛЬЗОВАТЕЛЬ НЕ ВОШЕЛ")
            return redirect("/")
