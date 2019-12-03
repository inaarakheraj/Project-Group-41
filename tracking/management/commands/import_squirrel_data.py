from django.core.management.base import BaseCommand, CommandError
from tracking.models import Sighting
import datetime
import pandas as pd

class Command(BaseCommand):
    help = 'Syntax: python manage.py import_squirrel_data path/to/file.csv'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):

        path = options['path'][0]
        d = pd.read_csv(path)

        for i, row in d.iterrows():
            if i%100 == 0: print(i)

            s = Sighting()
            s.Latitude = row['X']
            s.Longitude = row['Y']
            s.Unique_Squirrel_ID = row['Unique Squirrel ID']
            s.Shift = row['Shift']
            s.Date = datetime.date(int(str(row['Date'])[4:]),int(str(row['Date'])[:2]),int(str(row['Date'])[2:4]))
            s.Age = row['Age']
            s.Primary_Fur_Color = row['Primary Fur Color']
            s.Location = row['Location']
            s.Specific_Location = row['Specific Location']
            s.Running = row['Running']
            s.Chasing = row['Chasing']
            s.Climbing = row['Climbing']
            s.Eating = row['Eating']
            s.Foraging = row['Foraging']
            s.Other_Activities = row['Other Activities']
            s.Kuks = row['Kuks']
            s.Quaas = row['Quaas']
            s.Moans = row['Moans']
            s.Tail_flags = row['Tail flags']
            s.Tail_twitches = row['Tail twitches']
            s.Approaches = row['Approaches']
            s.Indifferent = row['Indifferent']
            s.Runs_from = row['Runs from']

            s.save()