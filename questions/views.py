from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect
from .models import Question, Profile, Answer, Tag, TagManager
from django.shortcuts import HttpResponseRedirect

from questions.forms import RegForm, SettingForm


# Create your views here.


def base_context(request):
    return {
        'most_popular_tags': Tag.objects.most_popular(),
        'best_members': Profile.objects.best_members(),
    }


def paginate(items, request):
    items_page = []

    paginator = Paginator(items, 3)
    page = request.GET.get('page')
    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        page = int(page)
        if page < 1:
            items_page = paginator.page(1)
        elif page > paginator.num_pages:
            items_page = paginator.page(paginator.num_pages)

    return items_page


def index(request):
    context = {
        'paginated_list': paginate(Question.objects.fresh(), request),
    }
    context.update(base_context(request))
    return render(request, "index.html", context)


def hot(request):
    context = {
        'paginated_list': paginate(Question.objects.hot(), request),
    }
    context.update(base_context(request))
    return render(request, "hot.html", context)


def current_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
        'paginated_list': paginate(question.answer_set.all(), request)
    }
    context.update(base_context(request))
    return render(request, 'current_question.html', context)


def current_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    context = {
        'cur_tag': tag,
        'paginated_list': paginate(tag.questions.all(), request),
    }
    context.update(base_context(request))
    return render(request, 'current_tag.html', context)


def ask(request):
    return render(request, 'ask.html', base_context(request))


def login_view(request):
    next_url = request.GET.get('next') or '/'
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if not user:
            return render(request, "login.html", {'error': 1, 'next': next_url, 'most_popular_tags': Tag.objects.most_popular(),
                                              'best_members': Profile.objects.best_members(), })
        else:
            login(request, user)
            return HttpResponseRedirect(next_url)
    else:
        return render(request, 'login.html', {'next': next_url, 'most_popular_tags': Tag.objects.most_popular(),
                                              'best_members': Profile.objects.best_members(), })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def settings(request):
    if request.method == "POST":
        f = SettingForm(request.POST, request.FILES)
        if f.is_valid():
            user = request.user
            user = f.change_user(user)
            user.save()
            login(request, user)
    else:
        f = SettingForm()
    return render(request, 'settings.html', {'form': f, 'most_popular_tags': Tag.objects.most_popular(),
                                             'best_members': Profile.objects.best_members(), })


def register(request):
    if request.method == "POST":
        f = RegForm(request.POST, request.FILES)
        if f.is_valid():
            profile = f.save()
            profile.save()
            login(request, profile.user)
            return HttpResponseRedirect("/")
    else:
        f = RegForm()
    return render(request, 'register.html', {'form': f, 'most_popular_tags': Tag.objects.most_popular(),
                                             'best_members': Profile.objects.best_members(), })
