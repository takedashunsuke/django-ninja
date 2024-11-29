# from .models import UserAccount
# from ninja import ModelSchema, Schema

# class CustomUserSchema(Schema):
#   class Meta:
#     model = UserAccount
#     fields = "__all__"
#     # exclude = ['password', 'last_login', 'birth_date']

# class UserIn(Schema):
#     username: str
#     password: str

# class UserOut(Schema):
#     id: int
#     username: str

# class CustomUserOut(ModelSchema):
#   class Meta:
#     model = UserAccount
#     fields = ['uid', 'name', 'email', 'avator']

# class CreateCustomUser(Schema):
#   username: str
#   email: str
#   password: str
#   first_name: Optional[str]
#   last_name: Optional[str]

# class UpdateUser(Schema):
#   username: Optional[str]
#   email: Optional[str]
#   first_name: Optional[str]
#   last_name: Optional[str]
#   is_active: Optional[bool]
#   is_staff: Optional[bool]
#   is_superuser: Optional[bool]

# # token
# class TokenSchema(Schema):
#   access_token: str
#   refresh_token: str
#   token_type: str