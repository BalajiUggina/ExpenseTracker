from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('add-category/',views.add_category,name='add-category'),
    path('add-expense/',views.add_expense,name='add-expense'),
    path('expenses/',views.expense_list,name='expense-list'),
    path('expense/delete/<int:id>/', views.delete_expense, name='delete-expense'),
    path('logout/',views.logout,name='logout'),
]