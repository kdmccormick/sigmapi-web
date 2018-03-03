"""
URLs for PartyList app.
"""
from django.conf.urls import url
from django.views.generic import RedirectView

from . import views, api


urlpatterns = [
    url(
        regex=r'^$',
        view=RedirectView.as_view(pattern_name='partylist-index'),
        name='partylist-index-old',
    ),
    url(
        regex=r'^all/$',
        view=views.index,
        name='partylist-index',
    ),
    url(
        regex=r'^add/$',
        view=views.add_party,
        name='partylist-add_party',
    ),
    url(
        regex=r'^blacklist/$',
        view=views.view_blacklist,
        name='partylist-view_blacklist',
    ),
    url(
        regex=r'^blacklist/match/(?P<query_str>.+)/$',
        view=api.query_blacklist,
        name='partylist-query_blacklist',
    ),
    url(
        regex=r'^blacklist/manage/$',
        view=views.manage_blacklist,
        name='partylist-manage_blacklist',
    ),
    url(
        regex=r'^blacklist/manage/remove/(?P<bl_id>[\d]+)/$',
        view=views.remove_blacklisting,
        name='partylist-remove_blacklisting',
    ),
    url(
        regex=r'^greylist/$',
        view=views.view_greylist,
        name='partylist-view_greylist',
    ),
    url(
        regex=r'^greylist/match/(?P<query_str>.+)/$',
        view=api.query_greylist,
        name='partylist-query_greylist',
    ),
    url(
        regex=r'^greylist/manage/$',
        view=views.manage_greylist,
        name='partylist-manage_greylist',
    ),
    url(
        regex=r'^greylist/manage/remove/(?P<gl_id>[\d]+)/$',
        view=views.remove_greylisting,
        name='partylist-remove_greylisting',
    ),
    url(
        regex=r'^manage/$',
        view=views.manage_parties,
        name='partylist-manage_parties',
    ),
    url(
        regex=r'^edit/(?P<party_id>[\d]+)/$',
        view=views.edit_party,
        name='partylist-edit_party',
    ),
    url(
        regex=r'^delete/(?P<party_id>[\d]+)/$',
        view=views.delete_party,
        name='partylist-delete_party',
    ),
    url(
        regex=r'^view/(?P<party_id>[\d]+)/guests/$',
        view=views.guests,
        name='partylist-guests',
    ),
    url(
        regex=r'^view/(?P<party_id>[\d]+)/guests/create/$',
        view=api.create,
        name='partylist-api-create',
    ),
    url(
        regex=(
            r'^view/(?P<party_id>[\d]+)/guests/destroy/'
            r'(?P<party_guest_id>[\d]+)/$'
        ),
        view=api.destroy,
        name='partlist-api-destroy',
    ),
    url(
        regex=(
            r'^view/(?P<party_id>[\d]+)/guests/signIn/'
            r'(?P<party_guest_id>[\d]+)/$'
        ),
        view=api.sign_in,
        name='partylist-api-signin',
    ),
    url(
        regex=(
            r'^view/(?P<party_id>[\d]+)/guests/signOut/'
            r'(?P<party_guest_id>[\d]+)/$'
        ),
        view=api.sign_out,
        name='partylist-api-signout',
    ),
    url(
        regex=r'^view/(?P<party_id>[\d]+)/guests/poll/$',
        view=api.poll,
        name='partylist-api-poll',
    ),
    url(
        regex=r'^view/(?P<party_id>[\d]+)/guests/export/$',
        view=api.export_list,
        name='partylist-api-export_list',
    ),
    url(
        regex=r'^view/(?P<party_id>[\d]+)/guests/count/delta/$',
        view=api.update_manual_delta,
        name='partylist-api-updateManualDelta',
    ),
    url(
        regex=r'^view/(?P<party_id>[\d]+)/guests/count/poll/$',
        view=api.poll_count,
        name='partylist-api-pollCount',
    ),
    url(
        regex=r'^view/(?P<party_id>[\d]+)/guests/init/$',
        view=api.init_pulse,
        name='partylist-api-initPulse',
    ),
]
