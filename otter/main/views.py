from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to
from otter.main.models import Message
from otter.main.forms import MessageForm

@login_required
@render_to('main/home.html')
def home(request):
    user = request.user
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return HttpResponseRedirect(request.get_full_path()) 
    else:
        form = MessageForm()
    return {'form': form, 'user': user}

