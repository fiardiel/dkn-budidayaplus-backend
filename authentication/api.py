from authentication.schema import LoginSchema, RegisterSchema
from ninja import Router
from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.errors import HttpError
from django.contrib.auth.models import User

router = Router()

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            return RefreshToken(token).check_blacklist()
        except Exception:
            raise HttpError(401, "Invalid token")

@router.post("/login")
def login(request, data: LoginSchema):
    try:
        user = User.objects.get(username=data.phone_number)
        if not user.check_password(data.password):
            raise HttpError(404, "User not found")
        
        refresh = RefreshToken.for_user(user)
        return {
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
    except User.DoesNotExist:
        raise HttpError(404, "User not found")
    

@router.post("/register")
def register(request, data: RegisterSchema):
    try:
        if User.objects.filter(username=data.phone_number).exists():
            raise HttpError(400, "User already exists")
        
        user = User.objects.create_user(
            username=data.phone_number,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name
        )
        refresh = RefreshToken.for_user(user)
        return {
            "message": "User created successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
    except Exception as e:
        raise HttpError(400, str(e))


@router.post("/protected", auth=JWTAuth())
def protected(request):
    return {"message": "This is a protected route"}