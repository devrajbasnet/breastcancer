
from django.contrib import admin
from django.urls import path
from core import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict_diagnosis/<int:id>/', views.predict_diagnosis, name='predict_diagnosis'),
    path('data/', views.data_input, name='data'),
    path('all/',views.check_status,name="check_status")
]
