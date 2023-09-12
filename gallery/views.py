from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from gallery.forms import SignUpForm, ImageUploadForm, PhotoSearchForm
from gallery.models import Image


def home(request):
    contents = Image.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been successfully logged in..")
            return redirect('home')
    else:
        contents = Image.objects.all()
        return render(request, 'gallery/home.html', {'contents': contents})
    return render(request, 'gallery/home.html', {'contents': contents})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully..")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been successfully logged in..")
                return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'gallery/register.html', {'form': form})
    return render(request, 'gallery/register.html', {'form': form})


def photoview(request, pk):
    if request.user.is_authenticated:
        photo_detail = Image.objects.get(id=pk)
        return render(request, 'gallery/photoview.html', {'photo_detail': photo_detail})
    else:
        messages.success(request, "you must have an account")
        return redirect('home')


def add_photo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Your photo has been uploaded successfully..")
                return redirect('home')
        else:
            form = ImageUploadForm()
        return render(request, 'gallery/add_photo.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to add a photo.')
        return redirect('home')


def delete_photo(request, pk):
    delete_photo = Image.objects.get(id=pk)
    delete_photo.delete()
    return redirect('home')


class UpdatePhoto(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Image
    template_name = 'gallery/update_photo.html'
    fields = ['title', 'description', 'image_file']
    success_url = '/'

    def test_func(self):
        return True


def search_photos(request):
    if request.method == 'GET':
        form = PhotoSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Image.objects.filter(title__icontains=query)
            return render(request, 'gallery/search_results.html', {'form': form, 'results': results})
        else:
            results = []
    else:
        form = PhotoSearchForm()
        results = []

    return render(request, 'gallery/search_results.html', {'form': form, 'results': results})

