from django.http import HttpResponse
from django.shortcuts import redirect


# this closure will check that that user is_authenticated (or) not
# so that register and  login pages won't be displayed for those who are already authorized
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admindashboard')
            else:
                return redirect('userdashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


# we have linked the user account to admin and groups using group table.
# So,that we can restrict accessing views through urls
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator