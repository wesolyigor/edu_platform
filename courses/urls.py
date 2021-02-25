from django.urls import path

from courses import views

app_name = 'courses'

urlpatterns = [
    path('create', views.CreateCourse.as_view(), name='create-course'),
    path('<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
]

