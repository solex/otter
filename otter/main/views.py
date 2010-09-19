from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from annoying.decorators import render_to
from django_odesk.core.clients import RequestClient

from otter.main.models import User, Team, Message
from otter.main.forms import MessageForm


def get_timeline(request, team_id=None, user_id=None, private=None):
    timeline = Message.objects.all()

    if user_id:
        username = user_id+'@odesk.com' #TODO: FUUUUUUU. Should use something more generic 
        timeline = timeline.filter(sender__username = username, 
                                   to_user__isnull = True, 
                                   to_team__isnull=True)
    elif team_id:
        client = RequestClient(request)
        teamrooms = {}
        for item in client.team.get_teamrooms(): #TODO: Session or cache?
            teamrooms[item['id']] = item
        if team_id not in teamrooms:
            return HttpResponse('FORBIDDEN')
        team_data = teamrooms[team_id]
        title = "%(company_name)s > %(name)s" % team_data
        team, created = Team.objects.get_or_create(name = team_data['id'], 
                                        defaults = {'title': title})
        timeline = timeline.filter(to_team = team)
        return team, timeline
    return timeline



@login_required
@render_to('main/home.html')
def home(request):
    return HttpResponseRedirect(reverse('user_timeline',
                                        args=[request.user.odesk_id])) 

@login_required
@render_to('main/home.html')
def timeline(request, user_id=None, team_id=None):
    
    
    timeline = get_timeline(request, user_id, team_id)        
    
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
def post(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            message = Message(sender=request.user, text=data['text'])
            if 'team_name' in data:
                #TODO: Check access
                message.to_team = Team.objects.get(name=data['team_name'])
            message.save()
            if request.is_ajax():
                return HttpResponse('OK')
            redirect = data.get('redirect', '/')
            return HttpResponseRedirect(redirect) 
    else:
        return HttpResponseRedirect('/') 


@login_required
@render_to('main/teams.html')
def teams(request):
    client = RequestClient(request)
    teamrooms = client.team.get_teamrooms()
    return {'teamrooms': teamrooms}


@login_required
@render_to('main/team.html')
def teamroom(request, team_id):
    team, timeline = get_timeline(request, team_id = team_id) 
    form = MessageForm()
    return {'team':team, 'timeline': timeline, 'form': form, 
            'url': request.get_full_path()}


@login_required
@render_to('main/colleagues.html')
def colleagues(request):
    client = RequestClient(request)
    #TODO: HR2 get_team_users doesn't seem to work
    teamrooms = client.team.get_teamrooms()
    clgs = []
    for team in teamrooms:
        for snapshot in client.team.get_snapshots(team['id'], online="all"):
            username = snapshot['user']['mail']
            data = {
                'first_name': snapshot['user']['first_name'],
                'last_name': snapshot['user']['last_name'],
                'email': snapshot['user']['last_name'],
            }
            col, created = User.objects.get_or_create(username = username, 
                                                      defaults = data)
            if not col in clgs:
                clgs.append(col)
            #if not snapshot['user_id'] in clgs:
            #    clgs[snapshot['user_id']] = snapshot
    return {'colleagues': clgs}


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
