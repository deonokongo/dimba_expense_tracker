from django.urls import path
from . import views
app_name = 'dimba_app'

urlpatterns = [
    path('',views.home, name="home"),
    path('about/', views.about, name="about"),
    path('features/', views.features, name='features'),
    path('track_expenses/', views.track_expenses, name='track_expenses'),
    path('expenses/', views.expenses, name='expenses'),
    path('contact/', views.contact, name='contact'),
    path('reports/', views.reports, name='reports'),
    path('team/', views.team, name='team'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('savings/', views.savings, name='savings'),
    path('profile/', views.profile, name='profile'),
    path('loans/', views.loans, name='loans'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_saving/', views.add_saving, name='add_saving'),
    path('add_loan/', views.add_loan, name='add_loan'),
    path('finance_management/', views.finance_management, name='finance_managememnt'),
    path('finance_literacy/', views.finance_literacy, name='finance_literacy'),
    path('update_expense/<int:id>',views.update_expense, name='update_expense'),
    path('update_saving/<int:id>/',views.update_saving, name='update_saving'),
    path('update_loan/<int:id>/',views.update_loan, name='update_loan'),
    path('delete_expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('delete_saving/<int:id>/', views.delete_saving, name='delete_saving'),
    path('delete_loan/<int:id>/', views.delete_loan, name='delete_loan'),
    path('accounts/register', views.register, name='register'),
    path('accounts/login', views.login_page, name='login'),
    path('accounts/logout', views.logout_view, name='logout'),
    path('upload/', views.upload_image, name='upload'),
]
