from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from annoying.decorators import render_to
from django_odesk.core.clients import RequestClient

from otter.main.models import Team, Message
from otter.main.forms import MessageForm

@login_required
@render_to('main/home.html')
def home(request):
    return HttpResponseRedirect(reverse('user_timeline',
                                        args=[request.user.odesk_id])) 

@login_required
@render_to('main/home.html')
def timeline(request, user_id=None, team_id=None):
    
    timeline = Message.objects.all()

    if user_id:
        username = user_id+'@odesk.com' #TODO: FUUUUUUU. Should use something more generic 
        timeline = timeline.filter(sender__username = username, 
                                   to_user__isnull = True, 
                                   to_team__isnull=True)
    elif team_id:
        pass
        
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return HttpResponseRedirect(request.get_full_path()) 
    else:
        form = MessageForm()

    return {'form': form, 'timeline': timeline}


@login_required
def sync(request):
    client = RequestClient(request)
    teamrooms = client.team.get_teamrooms()
    print teamrooms
    db_teams = set([team.name for team in request.user.team_set.all()])
    odesk_teams = set([team['id'] for team in teamrooms])
    if db_teams == odesk_teams:
        return HttpResponse('OK')
    for name in db_teams - odesk_teams:
        team = Team.objects.get(name = name)
        request.user.team_set.remove(team)
    for name in odesk_teams - db_teams:
        team = Team.objects.create(name = name, title=name) #TODO: Get real title
        request.user.team_set.add(team)
    return HttpResponse('SYNC')
