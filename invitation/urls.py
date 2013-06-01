from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app_settings import INVITE_ONLY


class LoginRequired(object):
    """
    Mixin for requiring login to a generic view.

    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs)


class LoginRequiredTemplateView(TemplateView, LoginRequired):
    pass

login_required_direct_to_template = login_required(direct_to_template)


urlpatterns = patterns('',
    url(r'^invitation/$',
        LoginRequiredTemplateView.as_view(template_name="invitation/invitation_home.html"),
        name='invitation_home'),
    url(r'^invitation/invite/$',
        'invitation.views.invite',
        name='invitation_invite'),
    url(r'^invitation/invite/complete/$',
        LoginRequiredTemplateView.as_view(template_name="invitation/invitation_complete.html"),
        name='invitation_complete'),
    url(r'^invitation/invite/unavailable/$',
        LoginRequiredTemplateView.as_view(template_name="invitation/invitation_unavailable.html"),
        name='invitation_unavailable'),
    url(r'^invitation/accept/complete/$',
        TemplateView.as_view(template_name="invitation/invitation_registered.html"),
        name='invitation_registered'),
    url(r'^invitation/accept/(?P<invitation_key>\w+)/$',
        'invitation.views.register',
        name='invitation_register'),
)


if INVITE_ONLY:
    urlpatterns += patterns('',
        url(r'^register/$',
            RedirectView.as_view(url='../invitation/invite_only/', permanent=False),
            name='registration_register'),
        url(r'^invitation/invite_only/$',
            TemplateView.as_view(template_name="invitation/invite_only.html"),
            name='invitation_invite_only'),
        url(r'^invitation/reward/$',
            'invitation.views.reward',
            name='invitation_reward'),
    )
