from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .serializers import UserSerializer, LoginSerializer
from .models import User


# -------------------------------
# Register
# -------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "User registered successfully",
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "role": user.role,
            },
            status=status.HTTP_201_CREATED,
        )


# -------------------------------
# Common Login Response
# -------------------------------
def generate_login_response(user, request):
    fcm_token = request.data.get("fcm_token")

    if fcm_token:
        user.fcm_token = fcm_token
        user.save(update_fields=["fcm_token"])

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "message": "Login successful",
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "fcm_token": user.fcm_token,
        },
        status=status.HTTP_200_OK,
    )


# -------------------------------
# Seller Login
# -------------------------------
class SellerLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if user.role != "seller":
            return Response(
                {"error": "Invalid role for seller login"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return generate_login_response(user, request)


# -------------------------------
# Patient Login
# -------------------------------
class PatientLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if user.role != "patient":
            return Response(
                {"error": "Invalid role for patient login"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return generate_login_response(user, request)


# -------------------------------
# Caretaker Login
# -------------------------------
class CaretakerLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if user.role != "caretaker":
            return Response(
                {"error": "Invalid role for caretaker login"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return generate_login_response(user, request)


# -------------------------------
# Caretaker → Get All Patients
# -------------------------------
class PatientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "caretaker":
            return Response(
                {"error": "Only caretaker allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        patients = User.objects.filter(role="patient")

        data = [
            {
                "id": p.id,
                "username": p.username,
                "fcm_token": p.fcm_token,
            }
            for p in patients
        ]

        return Response(data, status=status.HTTP_200_OK)


# -------------------------------
# Caretaker → Own Details
# -------------------------------
class CaretakerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != "caretaker":
            return Response(
                {"error": "Not a caretaker"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "fcm_token": user.fcm_token,
            },
            status=status.HTTP_200_OK,
        )

