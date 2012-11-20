from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse

from .models.abstract import APINotFound
from .models import Account, Hero, ToolTip
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
    values = {
        'form': form,
        }
    if request.POST and form.is_valid():
        try:
            account = form.save_or_none()
            if account:
                return HttpResponseRedirect(reverse("diablo_account_detail",args=(account.pk,)))
        except APINotFound:
            pass
        values['account_404'] = True
    return TemplateResponse(request,"diablo/add.html",values)

def edit_account(request,pk):
    account = Account.objects.get_or_404(pk=pk)
    account.can_edit_or_404(request.user)
    form = AccountForm(request.POST or None,instance=account)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("diablo_account_detail",args=(account.pk,)))
    return TemplateResponse(request,"diablo/edit.html",values)

def tooltip(request,model,model_pk):
    if model == 'rune':
        return HttpResponse(ToolTip.objects.get_rune_html(model_pk=model_pk))
    return HttpResponse(ToolTip.objects.get_lazy_html(model=model,model_pk=model_pk))
