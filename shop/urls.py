from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="shopApp"),
     path('aboutus/',views.aboutus,name="aboutus"),
    path('contactus/',views.contactus,name="contactus"),
    path('tracker/',views.tracker,name="tracker"),
     path('search/',views.search,name="search"),
    path('checkout/',views.checkout,name="checkout"),
    path('products/<int:myid>',views.productview,name="productview"),
]
