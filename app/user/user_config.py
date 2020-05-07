from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from app.views import *
from app.tokens import *
from django.contrib.sites.shortcuts import get_current_site


class SignUp(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = SignUpForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktywacja konta w TwojaŚwinka.pl'
            message = render_to_string('user/confirm_register_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'user/confirm_registration.html')

        return render(request, 'user/register.html', {'form': form})


class ActiveUser(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('login')
        else:
            return render(request, 'user/confirm_register_error.html')


class UserDetails(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'user/details.html')


class PasswordReset(PasswordResetView):

    def post(self, request, *args, **kwargs):
        for user in User.objects.all():
            if request.POST.get('email') == user.email:
                return super().post(request, *args, **kwargs)

        return render(request, 'user/password_reset_form.html')


class DeleteUser(LoginRequiredMixin, DeleteView):
    login_url = '/login/'

    model = User
    success_url = reverse_lazy('/login/')

    def get(self, request, *args, **kwargs):
        if User.objects.get(id=kwargs['pk']).pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')
