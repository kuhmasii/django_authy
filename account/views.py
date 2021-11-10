from django.shortcuts import redirect, render, get_object_or_404
from .forms import LoginForm, RegisterForm, searchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, get_user
from . models import Dictionary
from difflib import get_close_matches
import json

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

            # print(request.session.items())
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                # also check if user is_active...
                login(request, user)
                session = request.session
                session["name"] = request.user.username
                # print(session.items())

                return redirect("account:dashboard")
            else:
                request.session["invalid_user"] = 1

    return render(request,
                  "login_view.html", dict(
                      form=form
                  )
                  )


@login_required
def dashboard(request, *args, **kwargs):

    # dictionary = Dictionary.objects.get(pk=1)
    dictionary = get_object_or_404(Dictionary, pk=1)
    data = json.load(open(dictionary.file.path))
    name = request.user

    form_ser = searchForm()
    word_searched = None
    word_searched_list = None
    word_searched_str = 'What your search appears here'

    context = {"word_searched_list": word_searched_list,
               "word_searched_str": word_searched_str,
               "form_ser": form_ser, "name": name}

    if request.method == "POST":
        form_ser = searchForm(request.POST)

        if form_ser.is_valid():
            search = form_ser.cleaned_data.get("search")

            close_match = get_close_matches(
                search, data.keys(),
                n=5, cutoff=0.8
            )

            if search in data:
                word_searched = data[search]

            elif close_match:
                word_searched = f'Do you mean {close_match[0]} instead?'

            else:
                word_searched = "What you searched does not exist"

            if isinstance(word_searched, list):
                word_searched_list = word_searched
            else:
                word_searched_str = word_searched

            context = {"word_searched_list": word_searched_list,
                       "word_searched_str": word_searched_str,
                       "form_ser": form_ser, "name": name}

            return render(request, "dashboard.html", context)

    return render(request, "dashboard.html", context)


@ login_required
def logout_view(request):
    logout(request)
    # print(request.session.items())
    # request.user == AnonymousUser
    return redirect("account:index")
