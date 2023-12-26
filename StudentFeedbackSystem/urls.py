from django.contrib import admin
from django.urls import path
from feedback.views import feedback_form

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feedback/', feedback_form, name='feedback_form'),
    path('', feedback_form, name='default_feedback_form'),  # Add this line
]
