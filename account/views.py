import django
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request, *args, **kwargs):
    return render(
        request,
        "base.html"
    )


def register_view(request, *args, **kwargs):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password2 = form.cleaned_data.get("password2")
            # Don't print out the password as a decent dev

            try:

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password2
                )
            except:
                user = None

            if user:
                login(request, user)
                return redirect("account:dashboard")
            else:
                request.session["register_error "] = 1  # True

    return render(request,
                  "registration.html", dict(
                      form=form
                  )
                  )


def login_view(request, *args, **kwargs):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # Don't print out the password as a decent dev

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                # also check if user is_active...
                login(request, user)
                return redirect("account:dashboard")
            else:
                request.session["invalid_user"] = 1  # True

    return render(request,
                  "login_view.html", dict(
                      form=form
                    )
                )

@login_required
def dashboard(request, *args, **kwargs):
    name = request.user
    return render(
        request, "dashboard.html", dict(
        name=name
        )
    )

@login_required
def logout_view(request):
    logout(request)
    # request.user == AnonymousUser
    return redirect("account:index")
