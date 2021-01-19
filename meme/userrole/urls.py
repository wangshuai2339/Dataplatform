from django.conf.urls import include, url
from userrole.views import *
urlpatterns = [
    # Examples:
    # url(r'^$', 'meme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', admin.site.urls),
    url(r'^auth', AuthView.as_view()),
    url(r'^userinfo', UserInfo.as_view()),
    url(r'^register', Register.as_view()),
    url(r'^path/user', UserUpdate.as_view()),
    url(r'^udel', UserDelete.as_view()),
    url(r'^query', UsersInfo.as_view()),
    url(r'^roleadd', RoleAdd.as_view()),
    url(r'^rolesinfo', RolesInfo.as_view()),
    url(r'^path/role', RoleUpdate.as_view()),
    url(r'^rdel', RoleDelete.as_view()),
    url(r'^roleredact', Roleredact.as_view()),
    url(r'^loginout', LoginOut.as_view()),
    url(r'^pasupdate', PasswordUpdate.as_view()),
    url(r'^rolesearch', Rolesearch.as_view()),

]