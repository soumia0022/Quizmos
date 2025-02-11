from django.shortcuts import redirect

def return_to_dashboard(request):
    return redirect('user_management:dashboard')
