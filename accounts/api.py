from ninja import Router, Schema
from ninja.errors import HttpError
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from typing import Optional
from datetime import timedelta
from django.utils.timezone import now

User = get_user_model()
router = Router()

# メール認証用の一時的なストレージ
email_verification_tokens = {}

# スキーマ定義
class SignupSchema(Schema):
    email: str
    username: str
    password: str

class TokenSchema(Schema):
    token: str

class PasswordResetRequestSchema(Schema):
    email: str

class PasswordResetSchema(Schema):
    token: str
    new_password: str

class PasswordChangeSchema(Schema):
    current_password: str
    new_password: str

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
    id: str
    email: str
    username: str
    avatar: Optional[str] = None  # Noneを許容
    introduction: Optional[str] = None  # Noneを許容

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
    if not request.user.is_authenticated:
        raise HttpError(403, "認証が必要です")
    logout(request)
    return {"message": "ログアウトしました"}

# トークンリフレッシュ
@router.post("/token/refresh", auth=None)
def refresh_token(request, payload: RefreshTokenSchema):
    try:
        refresh = RefreshToken(payload.refresh)
        return {"access_token": str(refresh.access_token)}
    except Exception:
        raise HttpError(401, "無効なリフレッシュトークンです")

# 現在のユーザー情報取得
@router.get("/me", response=UserSchema, auth=JWTAuth())
def me(request):
    user = request.user
    if not user.is_authenticated:
        raise HttpError(403, "認証が必要です")
    return {
        "id": str(user.id),
        "email": user.email,
        "username": user.username,
        "avatar": user.avatar.url if user.avatar else None,
        "introduction": user.introduction,
    }



# メール送信ヘルパー関数
def send_verification_email(email: str, token: str):
    subject = "メール認証リンク"
    message = f"次のリンクをクリックしてメールアドレスを確認してください: {settings.FRONTEND_URL}/verify-email/{token}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# ユーザー登録 (メール認証付き)
@router.post("/register", auth=None)
def register(request, payload: SignupSchema):
    if User.objects.filter(email=payload.email).exists():
        raise HttpError(400, "このメールアドレスは既に登録されています")
    
    # ユーザー作成 (is_active=Falseで無効化)
    user = User.objects.create(
        email=payload.email,
        username=payload.username,
        password=make_password(payload.password),
        is_active=False,
    )
    
    # メール認証トークン生成
    token = get_random_string(32)
    email_verification_tokens[token] = {
        "user_id": user.id,
        "expires_at": now() + timedelta(hours=24)
    }
    
    send_verification_email(user.email, token)
    
    if settings.DEBUG:
        return {"message": "仮登録が完了しました。メールをご確認ください"+token}

    return {"message": "仮登録が完了しました。メールをご確認ください"}

# メール認証を完了するエンドポイント
@router.post("/verify-email", auth=None)
def verify_email(request, payload: TokenSchema):
    # トークンを取得
    token_data = email_verification_tokens.get(payload.token)
    
    # トークンが無効または期限切れの場合
    if not token_data or token_data["expires_at"] < now():
        raise HttpError(400, "無効または期限切れのトークンです")
    
    # トークンに紐づくユーザーを取得
    user = User.objects.get(id=token_data["user_id"])
    
    # ユーザーを有効化
    user.is_active = True
    user.save()
    
    # トークン削除
    del email_verification_tokens[payload.token]
    
    return {"message": "メール認証が完了しました"}


# トークン検証
@router.post("/token/verify", auth=None)
def verify_token(request, payload: TokenSchema):
    try:
        RefreshToken(payload.token)
        return {"message": "トークンは有効です"}
    except Exception:
        raise HttpError(401, "無効なトークンです")

# パスワードリセットリクエスト
@router.post("/password/reset", auth=None)
def password_reset_request(request, payload: PasswordResetRequestSchema):
    user = User.objects.filter(email=payload.email).first()
    if not user:
        raise HttpError(400, "指定されたメールアドレスは登録されていません")
    
    token = get_random_string(32)
    email_verification_tokens[token] = {
        "user_id": user.id,
        "expires_at": now() + timedelta(hours=1)
    }
    
    send_mail(
        "パスワードリセット",
        f"以下のリンクでパスワードをリセットしてください: {settings.FRONTEND_URL}/reset-password/{token}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    
    return {"message": "パスワードリセットメールを送信しました"}

# パスワードリセット
@router.post("/password/reset/confirm", auth=None)
def password_reset_confirm(request, payload: PasswordResetSchema):
    token_data = email_verification_tokens.get(payload.token)
    
    if not token_data or token_data["expires_at"] < now():
        raise HttpError(400, "無効または期限切れのトークンです")
    
    user = User.objects.get(id=token_data["user_id"])
    user.password = make_password(payload.new_password)
    user.save()
    
    del email_verification_tokens[payload.token]
    
    return {"message": "パスワードがリセットされました"}

# パスワード変更
@router.post("/password/change", auth=JWTAuth())
def password_change(request, payload: PasswordChangeSchema):
    user = request.user
    if not check_password(payload.current_password, user.password):
        raise HttpError(400, "現在のパスワードが正しくありません")
    
    user.password = make_password(payload.new_password)
    user.save()
    
    return {"message": "パスワードが変更されました"}



