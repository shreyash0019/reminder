from django.urls import path
from .views import (
    RegisterView,
    PatientLoginView,
    CaretakerLoginView,
    CaretakerDetailView,
    PatientListView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/patient/", PatientLoginView.as_view()),
    path("login/caretaker/", CaretakerLoginView.as_view()),
    path("caretaker/me/", CaretakerDetailView.as_view()),
    path("caretaker/patients/", PatientListView.as_view()),
]
