from ..register import views as register_view
from .views import ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView, CardDetailPageView, CampaignPageView, AboutPageForFoodie, AboutPageForCreator, test_ajax_response, like_ajax_response
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .models import Item


# アプリケーションのルーティング設定

urlpatterns = [
    path('about/foodie/', AboutPageForFoodie.as_view(), name='about_foodie'),
    path('about/creator/', AboutPageForCreator.as_view(), name='about_creator'),
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    path('', ItemFilterView.as_view(), name='index'),
    path('register/', register_view.register, name='register'),
    path('login/', register_view.Login.as_view(), name='login'),
    path('logout/', register_view.Logout.as_view(), name='logout'),
    path('profile/', register_view.profile, name='profile'),
    path('update_profile/', register_view.update_profile, name='update_profile'),
    path('card_detail/<int:pk>/', CardDetailPageView.as_view(), name='card_detail'),
    path('campaign/', CampaignPageView.as_view(), name='campaign'),
    path("ajax/", test_ajax_response),
    path("ajax-like/", like_ajax_response),
    url(r'user_portfolio/(?P<id>\d+)', register_view.user_portfolio, name='user_portfolio'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
