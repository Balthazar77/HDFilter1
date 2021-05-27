from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View
from account.forms import SignUpForm, ProfileForm
from django.urls import reverse, reverse_lazy
from account.models import User, Enrollment, DataUserOrganization
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class SigninView(View):
    form_class = SignUpForm

    def get(self, request, **kwargs):
        print()
        return self.render_form(self.form_class())

    def post(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self.render_form(form)

        user = form.save()
        user.refresh_from_db()
        user = authenticate(
            request=request,
            username=user.email,
            password=form.password,
        )
        login(request, user)
        return redirect(reverse('product'))

    def render_form(self, form):
        return render(self.request, 'registration/signup.html', {'form': form})


class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('product'))


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = SetPasswordForm


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = SetPasswordForm


class Profile(View):
    form_class = ProfileForm
    template_name = 'profile.html'

    def get(self, request, **kwargs):
        user = User.objects.filter(pk=self.request.user.pk).first()
        organizations = DataUserOrganization.objects.filter(account=self.request.user).first()
        initials = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'telephone': user.telephone,
            'name_org': organizations.name_org,
            'name_director': organizations.name_director,
            'ur_address': organizations.ur_address,
            'fk_address': organizations.fk_address,
            'inn': organizations.inn,
            'ogrn': organizations.ogrn,
            'kpp': organizations.kpp,
            'okpo': organizations.okpo,
            'okvid': organizations.okvid,
            'name_bank': organizations.name_bank,
            'bic': organizations.bic,
            'r_chet': organizations.r_chet,
            'k_chet': organizations.k_chet,
            'post_address': organizations.post_address,
        }
        form = self.form_class(initial=initials)
        return self.render_form(form)

    def get_context_data(self, **kwards):
        context = super(Profile, self).get_context_data(**kwards)
        context['Enrollments'] = Enrollment.objects.all()
        return context

    def render_form(self, form):
        enrollments = Enrollment.objects.filter(user=self.request.user)
        return render(self.request, self.template_name,
                      {'form': form, 'Enrollments': enrollments})

