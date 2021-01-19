from django.conf.urls import include, url
from memetest.views import *
urlpatterns = [
    # Examples:
    # url(r'^$', 'meme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', admin.site.urls),
    url(r'^testuser', TuserView.as_view()),
    url(r'^teststar', TstarView.as_view()),
    url(r'^user', UserView.as_view()),
    url(r'^star', StarView.as_view()),
    url(r'^createuser', CreateUser.as_view()),
    url(r'^testpay', TestPay.as_view()),
    url(r'^multipk', MultiPk.as_view()),
    url(r'^ladderpk', LadderPk.as_view()),

]