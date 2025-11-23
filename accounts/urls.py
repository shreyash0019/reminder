from django.urls import path
from .views import RegisterView, PatientLoginView, CaretakerLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('patient/login/', PatientLoginView.as_view(), name='patient_login'),
    path('caretaker/login/', CaretakerLoginView.as_view(), name='caretaker_login'),
]
