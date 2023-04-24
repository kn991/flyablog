from helpers import (
    session,
    sqlite3,
    message,
    redirect,
    Blueprint,
)

deletePostBlueprint = Blueprint("deletePost", __name__)


@deletePostBlueprint.route("/deletepost/<int:postID>/redirect=<direct>")
def deletePost(postID, direct):
    direct = direct.replace("&", "/")
    if "userName" in session:
        connection = sqlite3.connect("db/posts.db")
        cursor = connection.cursor()
        cursor.execute(f"select author from posts where id = {postID}")
        author = cursor.fetchone()
        match author[0] == session["userName"]:
            case True:
                cursor.execute(f"delete from posts where id = {postID}")
                cursor.execute(f"update sqlite_sequence set seq = seq-1")
                connection.commit()
                message("2", f'ПОСТ: "{postID}" УДАЛЕН')
                return redirect(f"/")
            case False:
                message(
                    "1",
                    f'ПОСТ: "{postID}" НЕ УДАЛЕН "{postID}" НЕ ПРИНАДЛЕЖИТ: {session["userName"]}',
                )
                return redirect(f"/")
        return redirect(f"/{direct}")
    else:
        message("1", f'ПОЛЬЗОВАТЕЛЬ ДОЛЖЕН ЗАРЕГИСТРИРОВАТЬСЯ ЧТОБЫ УДАЛЯТЬ ПОСТ: "{postID}"')
        return redirect(f"/login/redirect=&post&{postID}")
