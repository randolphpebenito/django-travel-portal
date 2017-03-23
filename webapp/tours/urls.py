from django.conf.urls import url

from .views import (
    employee,
    employee_tour_create,
    employee_tour_details,
    employee_tour_draft_submit,
    employee_tour_edit,
    employee_tour_list,
    employee_tour_list_status,
    finance_manager,
    finance_manager_list,
    finance_manager_list_status,
    finance_manager_tour_details,
    finance_manager_tour_details_edit,
    manager,
    manager_list,
    manager_list_status,
    manager_tour_details,
    manager_tour_details_edit,
    manager_tour_details_submit,
    route,

)
urlpatterns = [
    url(r'^$', route, name='route'),
    url(r'^employee/(?P<account_id>\d+)/$', employee, name='emp'),
    url(r'^employee/(?P<account_id>\d+)/(?P<tour_id>\d+)/$', employee_tour_details, name='emp-detail'),
    url(r'^employee/(?P<account_id>\d+)/(?P<tour_id>\d+)/edit/$', employee_tour_edit, name='emp-detail-edit'),
    url(r'^employee/(?P<account_id>\d+)/create/$', employee_tour_create, name='emp-create'),
    url(r'^employee/(?P<account_id>\d+)/list/$', employee_tour_list, name='emp-list'),
    url(r'^employee/(?P<account_id>\d+)/list/(?P<status>[\w\-]+)/$', employee_tour_list_status, name='emp-list-status'),
    url(r'^employee/(?P<account_id>\d+)/(?P<tour_id>\d+)/draft/submit/$', employee_tour_draft_submit, name='emp-draft-submit'),

    url(r'^manager/(?P<account_id>\d+)/$', manager, name='man'),
    url(r'^manager/(?P<account_id>\d+)/emp-tour-list/$', manager_list, name='man-list'),
    url(r'^manager/(?P<account_id>\d+)/emp-tour-list/(?P<status>[\w\-]+)/$', manager_list_status, name='man-list-status'),
    url(
        r'^manager/(?P<account_id>\d+)/emp-tour-detail/(?P<tour_id>\d+)/(?P<status>[\w\-]+)/$', 
        manager_tour_details, 
        name='man-tour-details'
    ),
    url(
        r'^manager/(?P<account_id>\d+)/emp-tour-detail/(?P<tour_id>\d+)/pending/change-to/(?P<status>[\w\-]+)/$', 
        manager_tour_details_edit, 
        name='man-tour-details-edit'
    ),
    url(
        r'^manager/(?P<account_id>\d+)/emp-tour-detail/(?P<tour_id>\d+)/approved/submit/$', 
        manager_tour_details_submit, 
        name='man-tour-details-submit'
    ),

    url(r'^finance-manager/(?P<account_id>\d+)/$', finance_manager, name='fin-man'),
    url(r'^finance-manager/(?P<account_id>\d+)/emp-tour-list/$', finance_manager_list, name='fin-man-list'),
    url(r'^finance-manager/(?P<account_id>\d+)/emp-tour-list/(?P<status>[\w\-]+)/$', finance_manager_list_status, name='fin-man-list-status'),
    url(
        r'^finance-manager/(?P<account_id>\d+)/emp-tour-detail/(?P<tour_id>\d+)/(?P<status>[\w\-]+)/$', 
        finance_manager_tour_details, 
        name='fin-man-tour-details'
    ),
    url(
        r'^finance-manager/(?P<account_id>\d+)/emp-tour-detail/(?P<tour_id>\d+)/pending/change-to/(?P<status>[\w\-]+)/$', 
        finance_manager_tour_details_edit, 
        name='fin-man-tour-details-edit'
    ),
]
