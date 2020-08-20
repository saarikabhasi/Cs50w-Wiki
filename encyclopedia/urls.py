from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>",views.get_page, name="title"),
    path("search/",views.get_search_query, name="search_results"),
    path("new/",views.new_page, name="create"),
    path("random/",views.random_page, name ="random"),
    path("edit/",views.edit_page, name="edit"),
    path("save/",views.save_page, name="save")

]
