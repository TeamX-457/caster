from django.urls import path

from . import views

app_name = 'assessments'

urlpatterns = [
    path('guides/<int:pk>/assessments/new/', views.AssessmentCreateView.as_view(), name='assessment_create'),
    path('assessments/<int:pk>/', views.AssessmentDetailView.as_view(), name='assessment_detail'),
    path('assessments/<int:pk>/questions/new/', views.add_question, name='question_create'),
    path('assessments/<int:pk>/take/', views.AssessmentTakeView.as_view(), name='assessment_take'),
    path('attempts/<int:pk>/', views.AttemptResultView.as_view(), name='attempt_result'),
]
