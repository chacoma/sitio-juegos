from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.inicio),
    url(r'^intercambio/$', views.intercambio_index, name='intercambio'),
    url(r'^intercambio/registro/$', views.registro, name='registro'),
    url(r'^intercambio/preguntas/1/$', views.preguntas, name='preguntas'),
    url(r'^intercambio/preguntas/2/$', views.preguntas2, name='preguntas2'),
    url(r'^intercambio/puntaje/$', views.final, name='final'),
    url(r'^intercambio/prueba/$', views.probar, name='probar'),
    url(r'^intercambio/reglamento/$', views.reglamento, name='reglamento'),
    ]
