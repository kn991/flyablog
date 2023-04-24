from helpers import (
    session,
    redirect,
    render_template,
    Blueprint,
)

accountSettingsBlueprint = Blueprint("accountSettings", __name__)


@accountSettingsBlueprint.route("/accountsettings")
def accountSettings():
    if "userName" in session:
        return render_template("accountSettings.html")
    else:
        return redirect("/login/redirect=&accountsettings")
