from django.urls import path

from . import views

urlpatterns = [
    path('levels/', views.AuthorityLevelView.as_view(), name='authority-levels'),
    path('rules/', views.AuthorityRulesView.as_view(), name='authority-rules'),
    path('rules/<int:pk>/', views.AuthorityRuleView.as_view(), name='authority-rule'),

]
