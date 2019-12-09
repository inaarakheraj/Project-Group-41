from django.shortcuts import render
from tracking.models import Sighting
import json
import numpy as np
from django import forms


def list_sightings(request):

    context = {'object_list': Sighting.objects.values_list('pk', flat=True).order_by('pk')}

    return render(request, 'tracking/list_sightings.html', context)


def add_sighting(request):

    if request.method == "POST":
        form = SightingForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data

            s = Sighting()
            s.Latitude = data.get('Latitude')
            s.Longitude = data.get('Longitude')
            s.Unique_Squirrel_ID = data.get('Unique_Squirrel_ID')
            s.Shift = data.get('Shift')
            s.Date = data.get('Date')
            s.Age = data.get('Age')
            s.Primary_Fur_Color = data.get('Primary_Fur_Color')
            s.Location = data.get('Location')
            s.Specific_Location = data.get('Specific_Location')
            s.Running = data.get('Running')
            s.Chasing = data.get('Chasing')
            s.Climbing = data.get('Climbing')
            s.Eating = data.get('Eating')
            s.Foraging = data.get('Foraging')
            s.Other_Activities = data.get('Other_Activities')
            s.Kuks = data.get('Kuks')
            s.Quaas = data.get('Quaas')
            s.Moans = data.get('Moans')
            s.Tail_flags = data.get('Tail_flags')
            s.Tail_twitches = data.get('Tail_twitches')
            s.Approaches = data.get('Approaches')
            s.Indifferent = data.get('Indifferent')
            s.Runs_from = data.get('Runs_from')

            s.save()

    elif request.method == "GET":
        # fields = ['Unique Squirrel ID','Latitude', 'Longitude', 'Shift', 'Date', 'Age',
        #           'Primary Fur Color', 'Location', 'Specific Location',  'Other Activities']
        #
        # bool_fields = ['Running', 'Chasing', 'Climbing', 'Eating', 'Foraging', 'Kuks',
        #                'Quaas', 'Moans','Tail flags', 'Tail twitches', 'Indifferent', 'Runs from']

        return render(request, "tracking/add.html", {'form': SightingForm()})


def update_or_delete(request, pk):

    s = Sighting.objects.get(pk=pk)

    if request.method == "GET":
        form = SightingForm(s.__dict__)

        if form.is_valid():
            return render(request, "tracking/add.html", {'form': form})
        else:
            return render(request, "tracking/add.html", {'errors': form.errors})

    # update
    if request.method == "POST":

        data = json.loads(request.body.decode('utf-8'))
        s = Sighting.objects.get(pk=pk)
        
        s.Latitude = data.get('Lattitude') or s.Latitude
        s.Longitude = data.get('Longitude') or s.Longitude
        s.Unique_Squirrel_ID = data.get('Unique Squirrel ID') or s.Unique_Squirrel_ID
        s.Shift = data.get('Shift') or s.Shift
        s.Date = data.get('Date') or s.Date
        s.Age = data.get('Age') or s.Age
        s.Primary_Fur_Color = data.get('Primary Fur Color') or s.Primary_Fur_Color
        s.Location = data.get('Location') or s.Location
        s.Specific_Location = data.get('Specific Location') or s.Specific_Location
        s.Running = data.get('Running') or s.Running
        s.Chasing = data.get('Chasing') or s.Chasing
        s.Climbing = data.get('Climbing') or s.Climbing
        s.Eating = data.get('Eating') or s.Eating
        s.Foraging = data.get('Foraging') or s.Foraging
        s.Other_Activities = data.get('Other Activities') or s.Other_Activities
        s.Kuks = data.get('Kuks') or s.Kuks
        s.Quaas = data.get('Quaas') or s.Quaas
        s.Moans = data.get('Moans') or s.Moans
        s.Tail_flags = data.get('Tail flags') or s.Tail_flags
        s.Tail_twitches = data.get('Tail twitches') or s.Tail_twitches
        s.Approaches = data.get('Approaches') or s.Approaches
        s.Indifferent = data.get('Indifferent') or s.Indifferent
        s.Runs_from = data.get('Runs from') or s.Runs_from
        
        s.save()


def stats(request):

    s = Sighting.objects.all()

    lat_lon = np.array(s.values_list('Latitude', 'Longitude'))
    avg_coords = (np.mean(lat_lon[:,0]), np.mean(lat_lon[:,1]))

    activities = np.array(s.values_list('Running', 'Chasing', 'Climbing', 'Eating', 'Foraging'))
    act_freq = np.sum(activities,axis=0)
    most_common_act = ('Running', 'Chasing', 'Climbing', 'Eating', 'Foraging')[np.argmax(act_freq)]

    responses = np.array(s.values_list('Approaches', 'Runs_from', 'Indifferent'))
    resp_freq = np.sum(responses,axis=0)
    most_common_resp = ('Approaches', 'Runs_from', 'Indifferent')[np.argmax(resp_freq)]

    sounds = np.array(s.values_list('Kuks', 'Quaas', 'Moans'))
    sound_freq = np.sum(sounds,axis=0)
    most_common_sound = ('Kuks', 'Quaas', 'Moans')[np.argmax(sound_freq)]

    color = list(s.values_list('Primary_Fur_Color', flat=True))
    counter = dict()
    for c in color:
        if c != 'nan':
            if c in counter:
                counter[c] += 1
            else:
                counter[c] = 1
    max_c = 0
    most_common_color = None
    for k,v in counter.items():
        if v > max_c:
            max_c = v
            most_common_color = k

    context = {'avg_coords', avg_coords,
               'most_common_act', most_common_act,
               'most_common_resp', most_common_resp,
               'most_common_sound',most_common_sound,
               'most_common_color', most_common_color
    }

    return render(request,'stats.html',context)


class Point:

    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon


def map_view(request):

    s = Sighting.objects.values_list('Latitude', 'Longitude')

    sightings = []
    for sighting in s[:100]:
        sightings.append(Point(sighting[1], sighting[0]))

    return render(request, 'tracking/map.html', {'sightings': sightings})\



class SightingForm(forms.Form):

    Unique_Squirrel_ID = forms.CharField(max_length=20,required=False)
    Latitude = forms.FloatField(required=False)
    Longitude = forms.FloatField(required=False)
    Shift = forms.CharField(max_length=2,required=False)
    Date = forms.CharField(max_length=10,required=False)
    Age = forms.CharField(max_length=10, required=False)
    Primary_Fur_Color = forms.CharField(max_length=10,required=False)
    Location = forms.CharField(max_length=20,required=False)
    Specific_Location = forms.CharField(max_length=50,required=False)
    Other_Activities = forms.CharField(max_length=20,required=False)
    Running = forms.BooleanField(required=False)
    Chasing = forms.BooleanField(required=False)
    Climbing = forms.BooleanField(required=False)
    Eating = forms.BooleanField(required=False)
    Foraging = forms.BooleanField(required=False)
    Kuks = forms.BooleanField(required=False)
    Quaas = forms.BooleanField(required=False)
    Moans = forms.BooleanField(required=False)
    Tail_flags = forms.BooleanField(required=False)
    Tail_twitches = forms.BooleanField(required=False)
    Approaches = forms.BooleanField(required=False)
    Indifferent = forms.BooleanField(required=False)
    Runs_from = forms.BooleanField(required=False)