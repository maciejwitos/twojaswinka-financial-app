from app.views import *


class SignUp(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/dashboard/')

        return render(request, 'user/register.html', {'form': form})


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
