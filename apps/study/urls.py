from django.urls import path

from . import views

app_name = 'study'

urlpatterns = [
    path('guides/new/', views.StudyGuideCreateView.as_view(), name='studyguide_create'),
    path('guides/<int:pk>/', views.StudyGuideDetailView.as_view(), name='studyguide_detail'),
    path('guides/<int:pk>/activities/new/', views.AddActivityView.as_view(), name='activity_create'),
    path('guides/<int:pk>/assign/', views.AssignStudyGuideView.as_view(), name='studyguide_assign'),
    path('guides/<int:pk>/complete/', views.MarkCompleteView.as_view(), name='studyguide_complete'),
]
