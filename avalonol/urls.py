from django.conf.urls import url
from . import views

app_name = 'test2'
urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^hall/$',views.hall,name='hall'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^players/$',views.players,name='players'),
    url(r'^instance/$',views.instance,name='instance'),
    url(r'^game/$',views.game,name='game'),
    url(r'^message/$',views.message,name='message'),
    url(r'^stage/$',views.stage,name='stage'),
    url(r'^board/$',views.board,name='board'),
    url(r'^notice/$',views.notice,name='notice'),
    url(r'^chooseopen/$',views.chooseopen,name='chooseopen'),
    url(r'^choose/$',views.choose,name='choose'),
    url(r'^voteopen/$',views.voteopen,name='voteopen'),
    url(r'^vote/$',views.vote,name='vote'),
    url(r'^backtohall/$',views.backtohall,name='backtohall'),
    url(r'^test/$',views.test,name='test'),
    # url(r'^$', views.index, name = 'index'),
    # url(r'^(?P<grade_id>[0-9])/$',views.detail,name = 'detail'),
]
