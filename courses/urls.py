from django.urls import path

from courses import views

app_name = 'courses'

urlpatterns = [
    path('create', views.CreateCourse.as_view(), name='create-course'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('edit/<slug:slug>/', views.CourseUpdateView.as_view(), name='course-edit'),
    path('delete/<slug:slug>/', views.CourseDeleteView.as_view(), name='course-delete'),
    path('<int:pk>/module/', views.CourseModuleUpdateView.as_view(), name='course-modules-update'),
    path('module/<int:module_id>/content/<model_name>/create', views.ContentCreateUpdateView.as_view(),
         name='module-content-create'),
]
