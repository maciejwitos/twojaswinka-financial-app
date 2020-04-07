from app.views import *


class AddCategory(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = AddCategoryForm()
        return render(request, 'category/category_form.html', {'form': form})

    def post(self, request):
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            Category.objects.create(
                name=form.cleaned_data['name'],
                spending=0,
                user=request.user
            )
            return redirect('all-category')
        return redirect('all-category')


# Wyświetlanie wszystkich kategorii
class ReadCategories(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        categories = Category.objects.filter(user=request.user.pk).order_by('-spending')
        return render(request, 'category/category_all.html', {'categories': categories})


# Edytowanie kategorii
class EditCategory(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    fields = ('name', 'spending')
    model = Category
    success_url = '/category/all/'

    def get(self, request, *args, **kwargs):
        if Category.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')


class DetailsCategory(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        transactions = Transaction.objects.filter(category=category).order_by('date')
        if not request.user.pk == category.user.pk:
            return redirect('/404/')
        return render(request, 'category/category_details.html', {'category': category,
                                                                  'transactions': transactions})


# Usuwanie kategorii
class DeleteCategory(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Category
    template_name = 'confirm_delete.html'
    success_url = '/category/all/'

    def get(self, request, *args, **kwargs):
        if Category.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')



