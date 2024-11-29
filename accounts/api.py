from ninja import Router, Schema
from ninja.errors import HttpError
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from typing import Optional

User = get_user_model()
router = Router()

# スキーマ定義
class SignupSchema(Schema):
    email: str
    username: str
    password: str

class LoginSchema(Schema):
    email: str
    password: str

class LoginResponseSchema(Schema):
    access_token: str
    refresh_token: str
    username: str
    email: str

class RefreshTokenSchema(Schema):
    refresh: str

class UserSchema(Schema):
    uid: str
    email: str
    username: str
    avatar: Optional[str] = None  # Noneを許容
    introduction: Optional[str] = None  # Noneを許容

# サインアップ
@router.post("/signup", auth=None)
def signup(request, payload: SignupSchema):
    if User.objects.filter(email=payload.email).exists():
        raise HttpError(400, "このメールアドレスは既に登録されています")
    user = User.objects.create(
        email=payload.email,
        username=payload.username,
        password=make_password(payload.password),
    )
    return {"message": "ユーザー登録が完了しました", "user_id": user.id}

# ログイン
@router.post("/login", auth=None, response=LoginResponseSchema)
def login_user(request, payload: LoginSchema):
    user = authenticate(email=payload.email, password=payload.password)
    if not user:
        raise HttpError(401, "メールアドレスまたはパスワードが間違っています")
    if not user.is_active:
        raise HttpError(403, "このアカウントは無効化されています")
    
    # トークン生成
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "username": user.username,
        "email": user.email,
    }

# ログアウト
@router.post("/logout")
def logout_user(request):
    logout(request)
    return {"message": "ログアウトしました"}

# トークンリフレッシュ
@router.post("/token/refresh", auth=None)
def refresh_token(request, payload: RefreshTokenSchema):
    try:
        refresh = RefreshToken(payload.refresh)
        return {"access_token": str(refresh.access_token)}
    except Exception as e:
        raise HttpError(401, "無効なリフレッシュトークンです")

# 現在のユーザー情報取得
@router.get("/me", response=UserSchema)
def me(request):
    user = request.user
    if not user.is_authenticated:
        raise HttpError(403, "認証が必要です")
    return {
        "uid": user.uid,
        "email": user.email,
        "username": user.username,
        "avatar": user.avatar.url if user.avatar else None,
        "introduction": user.introduction,
    }

# class HelloSchema(Schema):
#     name: str = "world"

# @router.post('/hello', auth=None)
# def hello(request, data: HelloSchema):
#     return f"Hello {data.name}"

# @router.get('/math')
# def math(request, a: int, b: int):
#     return {"add": a + b, "multiply": a * b}


# class UserSchema(Schema):
#     username: str
#     is_authenticated: bool
#     # Unauthenticated users don't have the following fields, so provide defaults.
#     email: str = None
#     # first_name: str = None
#     # last_name: str = None

# class Error(Schema):
#     message: str

# @router.get("/me", response={200: UserSchema, 403: Error})
# def me(request):
#     if not request.user.is_authenticated:
#         return 403, {"message": "Please sign in first"}
#     return request.user 

