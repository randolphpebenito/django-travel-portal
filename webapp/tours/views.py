from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from employee_accounts.models import EmployeeAccount
from .forms import EmployeeTourRequestForm 
from .models import EmployeeRequestStatus, EmployeeTourRequest, EmployeeTourRequestStatus  

REDIRECT_ACCOUNT = {
    1: 'tour:emp',
    2: 'tour:man',
    3: 'tour:fin-man',

}

REQUEST_STATUS = {
    'pending': {
        'id': 1,
        'status': 'Pending'
    },
    'approved': { 
        'id': 2,
        'status': 'Approved'
    },
    'rejected': { 
        'id': 3,
        'status': 'Rejected'
    },
    'request-for-info': {
        'id': 4,
        'status': 'Request For Information'
    },
    'draft': {
        'id': 5,
        'status': 'Draft'
    },
}

#Utility Functions
def get_employee_account_or_redirect_to_admin(**kwargs):
    try:
        e = EmployeeAccount.objects.get(**kwargs)
    except EmployeeAccount.DoesNotExist:
        return redirect('/admin/')
    return e

def account_position_page_validate_or_redirect(account_id, expected_account_id):
    ea = get_employee_account_or_redirect_to_admin(pk=account_id)
    if ea.account_position.id != expected_account_id:
        return redirect(REDIRECT_ACCOUNT[ea.account_position.pk], account_id=ea.pk)
    return ea

def paginate_list(list_obj, page_req_var):
    paginator = Paginator(list_obj, 10)
    try:
        pl = paginator.page(page_req_var)
    except PageNotAnInteger:
        pl = paginator.page(1)
    except EmptyPage:
        pl = paginator.page(paginator.num_pages)
    return pl


#View Functions
@login_required
def route(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    ea = get_employee_account_or_redirect_to_admin(account=request.user)
    return redirect(REDIRECT_ACCOUNT[ea.account_position.pk], account_id=ea.pk)

#---EMPLOYEE VIEWS---#
@login_required
def employee(request, account_id):
    ea = account_position_page_validate_or_redirect(account_id, 1)
    et = EmployeeTourRequest.objects.filter(employee=ea)
    etr = et.values('request_status').annotate(total=Count('request_status'))
    
    tour_list = paginate_list(et.order_by('-date_modified'), request.GET.get('page'))
    context = {
            'user': ea.account.username,
            'employee_account': ea, 
            'emp_tours': tour_list,
            'pending_count': next((item for item in etr if item["request_status"] == 1), {'request_status': 1, 'total': 0})['total'],
            'approved_count': next((item for item in etr if item["request_status"] == 2), {'request_status': 2, 'total': 0})['total'],
            'rejected_count': next((item for item in etr if item["request_status"] == 3), {'request_status': 3, 'total': 0})['total'],
            'rfi_count': next((item for item in etr if item["request_status"] == 4), {'request_status': 4, 'total': 0})['total'],
            'tour_id': ea.pk,
        }

    return render(request, "tours/employee_dashboard.html", context)

@login_required
def employee_tour_create(request, account_id):
    ea = account_position_page_validate_or_redirect(account_id, 1)

    form = EmployeeTourRequestForm(request.POST or None, request.FILES or None)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = ea
            if not instance.draft:
                pending_obj = EmployeeRequestStatus.objects.get(status_name='Pending')
                instance.request_status = pending_obj
            instance.save()
            # message success
            messages.success(request, "Successfully Created!")
            return redirect('tour:emp-detail', account_id=ea.pk, tour_id=instance.pk)
    context = {
            'user': ea.account.username,
            'form': form,
            'tour_id': ea.pk,
    }

    return render(request, "tours/employee_tour_create.html", context)

@login_required
def employee_tour_edit(request, account_id, tour_id):
    ea = account_position_page_validate_or_redirect(account_id, 1)
    emp_tour = get_object_or_404(EmployeeTourRequest, employee=ea, pk=tour_id)

    form = EmployeeTourRequestForm(request.POST or None, request.FILES or None, instance=emp_tour)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = ea
            instance.save()
            # message success
            messages.success(request, "Successfully Updated!")
            return redirect('tour:emp-detail', account_id=ea.pk, tour_id=instance.pk)
    context = {
            'user': ea.account.username,
            "form": form,
    }

    return render(request, "tours/employee_tour_create.html", context)

@login_required
def employee_tour_list(request, account_id):
    ea = account_position_page_validate_or_redirect(account_id, 1)
    etr = EmployeeTourRequest.objects.filter(employee=ea)
    tour_list = paginate_list(etr.order_by('-date_modified'), request.GET.get('page'))
    etr_req = etr.values('request_status').annotate(total=Count('request_status'))
    etr_draft = etr.values('draft').annotate(total=Count('draft'))

    context = {
            'employee_account': ea, 
            'user': ea.account.username,
            'tours': tour_list,
            'tour_id': ea.pk,
	    'tour_count': etr.count(),
            'pending_count': next((item for item in etr_req if item["request_status"] == 1), {'request_status': 1, 'total': 0})['total'],
            'approved_count': next((item for item in etr_req if item["request_status"] == 2), {'request_status': 2, 'total': 0})['total'],
            'rejected_count': next((item for item in etr_req if item["request_status"] == 3), {'request_status': 3, 'total': 0})['total'],
            'rfi_count': next((item for item in etr_req if item["request_status"] == 4), {'request_status': 4, 'total': 0})['total'],
            'draft_count': next((item for item in etr_draft if item["draft"] == True), {'draft': True, 'total': 0})['total']	
        }

    return render(request, "tours/employee_tour_list.html", context)

def employee_tour_list_status(request, account_id, status):
    ea = account_position_page_validate_or_redirect(account_id, 1)
    status_id = None
    etr = None
    if status == 'draft':
        etr = EmployeeTourRequest.objects.filter(
                    employee=ea,
                    draft=True,
                )
        status_id = 5
    else:
        if status in REQUEST_STATUS:
            status_id = REQUEST_STATUS[status]['id']
        else:
            return render(request, "404.html", {})

        etr = EmployeeTourRequest.objects.filter(
                    employee=ea,
                    request_status__pk=status_id,
                )

    tour_list = paginate_list(etr.order_by('-date_modified'), request.GET.get('page'))
    context = {
            'employee_account': ea, 
            'user': ea.account.username,
            'tours': tour_list,
            'tour_id': ea.pk,
            'status': REQUEST_STATUS[status]['status'],
            'status_id': status_id,
            'status_link': status,
            'account_id': account_id,
        }

    return render(request, "tours/employee_tour_list_status.html", context)

@login_required
def employee_tour_details(request, account_id, tour_id):
    ea = account_position_page_validate_or_redirect(account_id, 1)
    etr = get_object_or_404(EmployeeTourRequest, pk=tour_id)

    context = {
            'user': ea.account.username,
            'tour_details': etr,
            'tour_id': ea.pk
        }

    return render(request, "tours/employee_tour_details.html", context)

def employee_tour_draft_submit(request, account_id, tour_id):
    ea = account_position_page_validate_or_redirect(account_id, 1)
    etr = get_object_or_404(EmployeeTourRequest, pk=tour_id, employee=ea)
    status_obj = EmployeeRequestStatus.objects.get(status_name='Pending')
    etr.draft = False
    etr.request_status = status_obj
    etr.save()

    return redirect('tour:emp-list-status', account_id=ea.pk, status='draft')

#---MANAGER VIEWS---#
def manager(request, account_id):
    ea = account_position_page_validate_or_redirect(account_id, 2)
    et = EmployeeTourRequest.objects.filter(approving_manager=ea, draft=False)
    etr = EmployeeTourRequestStatus.objects.filter(emp_tour_req__approving_manager=ea)
    etr_req = etr.values('approved_by_manager').annotate(total=Count('approved_by_manager'))
    x = etr.values('approved_by_manager', 'submitted_to_finance_manager').annotate(total=Count('approved_by_manager'))

    context = {
            'user': ea.account.username,
            'account_id': ea.pk,
            'employee_account': ea, 
            'tours': et,
            'tour_id': ea.pk,
            'pending_count': next(
                    (item for item in etr_req if item["approved_by_manager"] == 1), 
                    {'approved_by_manager': 1, 'total': 0}
                )['total'],
            'for_submission_count': next(
                        (item for item in x if item["approved_by_manager"] == 2 and not item["submitted_to_finance_manager"] ), 
                        {'approved_by_manager': 2, 'total': 0}
                    )['total'],
        }

    return render(request, "tours/manager_dashboard.html", context)

def manager_list(request, account_id):
    ea = account_position_page_validate_or_redirect(account_id, 2)
    etr = EmployeeTourRequestStatus.objects.filter(emp_tour_req__approving_manager=ea)
    tour_list = paginate_list(etr.order_by('-date_modified'), request.GET.get('page'))

    context = {
            'user': ea.account.username,
            'tours': tour_list,
            'account_id': account_id,
            'tour_id': ea.pk,
        }

    return render(request, "tours/manager_tour_list.html", context)

def manager_list_status(request, account_id, status):
    ea = account_position_page_validate_or_redirect(account_id, 2)
    if status in REQUEST_STATUS:
        status_id = REQUEST_STATUS[status]['id']
    else:
        return render(request, "404.html", {})

    etr = EmployeeTourRequestStatus.objects.filter(
                emp_tour_req__approving_manager=ea,
                approved_by_manager__pk=status_id,
            )

    tour_list = paginate_list(etr.order_by('-date_modified'), request.GET.get('page'))

    context = {
            'user': ea.account.username,
            'tours': tour_list,
            'status': REQUEST_STATUS[status]['status'],
            'status_id': status_id,
            'status_link': status,
            'tour_id': ea.pk,
            'account_id': account_id
        }

    return render(request, "tours/manager_tour_list_status.html", context)

def manager_tour_details(request, account_id, tour_id, status):
    ea = account_position_page_validate_or_redirect(account_id, 2)
    etr = get_object_or_404(EmployeeTourRequest, pk=tour_id, approving_manager=ea)
    if status in REQUEST_STATUS:
        status_id = REQUEST_STATUS[status]['id']
    else:
        return render(request, "404.html", {})
    
    etr_stat = get_object_or_404(EmployeeTourRequestStatus, emp_tour_req=etr)
    context = {
            'etr_stat': etr_stat,
            'user': ea.account.username,
            'manager_user': True,
            'tour_details': etr,
            'tour_id': ea.pk,
            'status_id': REQUEST_STATUS[status]['id']
        }

    return render(request, "tours/employee_tour_details.html", context)

def manager_tour_details_edit(request, account_id, tour_id, status):
    ea = account_position_page_validate_or_redirect(account_id, 2)
    etr = get_object_or_404(EmployeeTourRequest, pk=tour_id, approving_manager=ea)
    if status in REQUEST_STATUS:
        status_id = REQUEST_STATUS[status]['id']
    else:
        return render(request, "404.html", {})

    status_obj = EmployeeRequestStatus.objects.get(pk=status_id)
    emp_tour_stat = EmployeeTourRequestStatus.objects.get(emp_tour_req=etr) 
    emp_tour_stat.approved_by_manager = status_obj
    emp_tour_stat.save()

    if status == 'rejected' or status == 'request-for-info':
        etr.request_status = status_obj
        etr.save()

    return redirect('tour:man-list-status', account_id=ea.pk, status=status)

def manager_tour_details_submit(request, account_id, tour_id):
    ea = account_position_page_validate_or_redirect(account_id, 2)
    etr = get_object_or_404(EmployeeTourRequest, pk=tour_id, approving_manager=ea)
    status_obj = EmployeeRequestStatus.objects.get(pk=REQUEST_STATUS['approved']['id'])
    emp_tour_stat = EmployeeTourRequestStatus.objects.get(emp_tour_req=etr, approved_by_manager=status_obj) 
    emp_tour_stat.submitted_to_finance_manager = True
    emp_tour_stat.save()

    return redirect('tour:man-list-status', account_id=ea.pk, status='approved')
    
#---FINANCE MANAGER VIEWS---#
def finance_manager(request, account_id):
    ea = account_position_page_validate_or_redirect(account_id, 3)
    context = {
            'tour_id': ea.pk,
            'user': ea.account.username,
            'employee_account': ea    
        }
    return render(request, "tours/finance_manager_dashboard.html", context)

def finance_manager_list(request, account_id):
    ea = account_position_page_validate_or_redirect(account_id, 3)
    etr = EmployeeTourRequestStatus.objects.filter(submitted_to_finance_manager=True).order_by('-date_modified')

    context = {
            'user': ea.account.username,
            'tour_id': ea.pk,
            'tours': etr,
            'account_id': account_id,
            'finance_manager_id': ea.pk,
        }

    return render(request, "tours/finance_manager_tour_list.html", context)

def finance_manager_list_status(request, account_id, status):
    ea = account_position_page_validate_or_redirect(account_id, 3)
    if status in REQUEST_STATUS:
        status_id = REQUEST_STATUS[status]['id']
    else:
        return render(request, "404.html", {})

    stat_obj = EmployeeRequestStatus.objects.get(pk=REQUEST_STATUS[status]['id'])
    etr = EmployeeTourRequestStatus.objects.filter(
                submitted_to_finance_manager=True,
                approved_by_finance_manager=stat_obj,
            ).order_by('-date_modified')

    context = {
            'user': ea.account.username,
            'tours': etr,
            'status': REQUEST_STATUS[status]['status'],
            'status_id': status_id,
            'status_link': status,
            'account_id': account_id,
            'tour_id': ea.pk,
            'finance_manager_id': ea.pk,
        }

    return render(request, "tours/finance_manager_tour_list_status.html", context)

def finance_manager_tour_details(request, account_id, tour_id, status):
    ea = account_position_page_validate_or_redirect(account_id, 3)
    etr = get_object_or_404(EmployeeTourRequest, pk=tour_id)
    if status in REQUEST_STATUS:
        status_id = REQUEST_STATUS[status]['id']
    else:
        return render(request, "404.html", {})
    context = {
            'user': ea.account.username,
            'finance_manager_id': ea.pk,
            'tour_id': ea.pk,
            'finance_manager_user': True,
            'tour_details': etr,
            'status_id': REQUEST_STATUS[status]['id']
        }

    return render(request, "tours/employee_tour_details.html", context)

def finance_manager_tour_details_edit(request, account_id, tour_id, status):
    print "EDITING TOUR DETAILS FINANCE MANAGER!!!"
    ea = account_position_page_validate_or_redirect(account_id, 3)
    etr = get_object_or_404(EmployeeTourRequest, pk=tour_id)
    if status in REQUEST_STATUS:
        status_id = REQUEST_STATUS[status]['id']
    else:
        return render(request, "404.html", {})

    status_obj = EmployeeRequestStatus.objects.get(pk=status_id)
    emp_tour_stat = get_object_or_404(EmployeeTourRequestStatus, emp_tour_req=etr, submitted_to_finance_manager=True) 
    emp_tour_stat.approving_finance_manager = ea
    emp_tour_stat.approved_by_finance_manager = status_obj
    emp_tour_stat.save()
    print etr.request_status
    etr.request_status = status_obj
    etr.save()

    return redirect('tour:fin-man-list-status', account_id=ea.pk, status=status)



def logout_page(request):
    #if not request.user.is_authenticated():
    logout(request)
    return HttpResponseRedirect('/')

