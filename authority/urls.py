from django.urls import path

from . import views

urlpatterns = [
    path('levels/', views.AuthorityLevelView.as_view(), name='authority-levels'),
    path('rules/', views.AuthorityRulesView.as_view(), name='authority-rules'),
    path('options/', views.AuthorityRulesView.as_view(), name='authority-options'),
    path('requests/', views.AuthorityRulesView.as_view(), name='authority-requests'),
    path('requests/<int:pk>/', views.AuthorityRulesView.as_view(), name='authority-request-detail'),
    path('rules/<int:pk>/', views.AuthorityRuleView.as_view(), name='authority-rule'),

]
