from django.shortcuts import render
from .forms import ProfileForm

# Create your views here.
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    form = ProfileForm(instance=request.user.profile)
    return render(request, "registration/profile.html", {"profile": form})