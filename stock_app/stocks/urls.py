from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
	path("get-quote", views.get_quote),
    path("add-portfolio", views.add_portfolio),
    path("remove-saved", views.remove_saved),
    path("game/<room>",views.game_lobby, name="game-lobby"),
    path("game/<room>/<user>",views.game_portfolio, name="game-portfolio"),
    path("game/<room>/<user>/<bs>",views.buy_sell, name="buy-sell"),
    path("create-newgame", views.create_newgame),
    path("user-join", views.user_join),
	path("create-game", views.create_game, name="create-game"),
	path("join-game", views.join_game, name="join-game"),
	path("portfolio", views.portfolio, name="portfolio"),
    path("new-transaction", views.new_transaction, name="transaction"),	
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	