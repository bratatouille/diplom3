from django.urls import path
from .views import index, about, support, payments, delivery, computer_catalog, get_computers_by_category

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('support/', support, name='support'),
    path('payments/', payments, name='payments'),
    path('delivery/', delivery, name='delivery'),
    path('pc/', computer_catalog, name='computer_catalog'),
    path('pc/<str:category_name>/', get_computers_by_category, name='get_computers_by_category'),
]
