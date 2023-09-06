
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from menu_service import customer_controller
from menu_service import restaurant_controller
from menu_service import auth_controller


urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view()),

    path('register/', auth_controller.register_user),

    path('restaurant/create/', restaurant_controller.create_restaurant),
    path('add/menu/', restaurant_controller.add_menu),

    path('menus/', customer_controller.menus_list),
    path('choose/menu/', customer_controller.choose_menu),
    path('menu/winning', customer_controller.winning_menu),
]
