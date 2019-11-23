from django.core.management.base import BaseCommand, CommandError
from tracking.models import Sighting
import datetime

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    @staticmethod
    def to_bool(s):
        if s == 'TRUE':
            return True
        if s == 'FALSE':
            return False

    def handle(self, *args, **options):

        path = options['path'][0]
        f = open(path, 'r')
        for row in f.readlines()[1:]:
            row = row.split(',')
            s = Sighting()
            s.Latitude = row[0]
            s.Longitude = row[1]
            s.Unique_Squirrel_ID = row[2]
            s.Shift = row[4]
            s.Date = datetime.date(int(row[5][4:]),int(row[5][:2]),int(row[5][2:4]))
            s.Age = row[7]
            s.Primary_Fur_Color = row[8]
            s.Location = row[12]
            s.Specific_Location = row[14]
            s.Running = Command.to_bool(row[15])
            s.Chasing = Command.to_bool(row[16])
            s.Climbing = Command.to_bool(row[17])
            s.Eating = Command.to_bool(row[18])
            s.Foraging = Command.to_bool(row[19])
            s.Other_Activities = row[20]
            s.Kuks = Command.to_bool(row[21])
            s.Quaas = Command.to_bool(row[22])
            s.Moans = Command.to_bool(row[23])
            s.Tail_flags = Command.to_bool(row[24])
            s.Tail_twitches = Command.to_bool(row[25])
            s.Approaches = Command.to_bool(row[26])
            s.Indifferent = Command.to_bool(row[27])
            s.Runs_from = Command.to_bool(row[28])

            s.save()
            break

        # for poll_id in options['path']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()

        self.stdout.write(self.style.SUCCESS(path))