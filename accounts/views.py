from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, LoginSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated



# Register View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
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


# Common login logic
def generate_login_response(user):
    token, created = Token.objects.get_or_create(user=user)
    return Response(
        {
            "message": "Login successful",
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        },
        status=status.HTTP_200_OK,
    )


# Patient Login View
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
        return generate_login_response(user)


# Caretaker Login View
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
        return generate_login_response(user)
    
    
class PatientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "caretaker":
            return Response({"error": "Only caretaker allowed"}, status=403)

        patients = User.objects.filter(role="patient")

        data = []
        for p in patients:
            data.append({
                "id": p.id,
                "username": p.username,
                "fcm_token": p.fcm_token,
            })

        return Response(data)

    
    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class CaretakerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != "caretaker":
            return Response({"error": "Not a caretaker"}, status=403)

        return Response({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "fcm_token": user.fcm_token,
        })

