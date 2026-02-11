from django.urls import path
from .views import (
    RegisterView,
    SellerLoginView,
    PatientLoginView,
    CaretakerLoginView,
    PatientListView,
    CaretakerDetailView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('seller/login/', SellerLoginView.as_view(), name='seller-login'),
    path('patient/login/', PatientLoginView.as_view(), name='patient-login'),
    path('caretaker/login/', CaretakerLoginView.as_view(), name='caretaker-login'),

    path('caretaker/patients/', PatientListView.as_view(), name='caretaker-patients'),
    path('caretaker/me/', CaretakerDetailView.as_view(), name='caretaker-detail'),
]
