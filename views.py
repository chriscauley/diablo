from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from .models import Account, Hero
from .forms import AccountForm

def account_detail(request,pk):
    account = Account.objects.get_or_404(pk=pk)
    values = {
        'account': account,
        'hero': account.hero_set.all()[0]
        }
    return TemplateResponse(request,"diablo/account_detail.html",values)

def hero_detail(request,hero_pk):
    hero = Hero.objects.get_or_404(pk=hero_pk)
    values = {
        'account': hero.account,
        'hero': hero,
        }
    m = '_hero' if request.is_ajax() else 'account_detail'
    return TemplateResponse(request,"diablo/%s.html"%m,values)

def add_account(request):
    form = AccountForm(request.POST or None)
    if request.POST and form.is_valid():
        account = form.save()
        return HttpResponseRedirect(reverse("diablo_account_detail",args=(account.pk,)))
    values = {
        'form': form,
        }
    return TemplateResponse(request,"diablo/add.html",values)

def edit_account(request,pk):
    account = Account.objects.get_or_404(pk=pk)
    account.can_edit_or_404(request.user)
    form = AccountForm(request.POST or None,instance=account)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("diablo_account_detail",args=(account.pk,)))
    return TemplateResponse(request,"diablo/edit.html",values)
