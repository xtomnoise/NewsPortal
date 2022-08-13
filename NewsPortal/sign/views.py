from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView
from .forms import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import os
import sys
sys.path.append(os.path.abspath('..'))
from news.models import Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class UserUpdate(LoginRequiredMixin,
                 UpdateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'user_update.html'
    context_object_name = 'user_update'

    def get_success_url(self):
        return '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('post_list')
