from wtforms import validators, Form, StringField, PasswordField, TextAreaField


class commentForm(Form):
    comment = TextAreaField(
        "Комментарий",
        [validators.Length(min=20, max=500), validators.InputRequired()],
        render_kw={"placeholder": "Оставить комементарий"},
    )


class loginForm(Form):
    userName = StringField(
        "Юзернейм",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "юзернейм"},
    )
    password = PasswordField(
        "Пароль",
        [validators.Length(min=8), validators.InputRequired()],
        render_kw={"placeholder": "Пароль"},
    )


class createPostForm(Form):
    postTitle = StringField(
        "Загловок",
        [validators.Length(min=4, max=75), validators.InputRequired()],
        render_kw={"placeholder": "Заголовок"},
    )
    postTags = StringField(
        "Теги, через запятую", [validators.InputRequired()], render_kw={"placeholder": "Теги через запятую"}
    )
    postContent = TextAreaField(
        "Текст поста",
        [validators.Length(min=5)],
    )


class changePasswordForm(Form):
    oldPassword = PasswordField(
        "Старый Пароль",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "Старый пароль"},
    )
    password = PasswordField(
        "Новый Пароль",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "Новый пароль"},
    )
    passwordConfirm = PasswordField(
        "Подтверждение пароля",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "Подтверди пароль"},
    )


class changeUserNameForm(Form):
    newUserName = StringField(
        "Юзернейм",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "Юзернейм"},
    )


class signUpForm(Form):
    userName = StringField(
        "Юзернейм",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "Юзернейм"},
    )
    email = StringField(
        "Почта",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"placeholder": "Почта"},
    )
    password = PasswordField(
        "Пароль",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "пароль"},
    )
    passwordConfirm = PasswordField(
        "Подтверждение пароля",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "Подтверждение пароля"},
    )
