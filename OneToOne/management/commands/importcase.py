from django.core.management.base import BaseCommand
from django.apps import apps
import csv


class Command(BaseCommand):
    help = 'Creating model objects according the file path specified'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="file path")
        parser.add_argument('--model_name', type=str, help="model name")
        parser.add_argument('--app_name', type=str, help="django app name that the model is connected to")

    def handle(self, *args, **options):
        file_path = options['path']
        _model = apps.get_model(options['app_name'], options['model_name'])

        with open(file_path, mode="r", encoding="utf-8-sig") as csv_file:
            # reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            reader = csv.DictReader(csv_file)
            created_users = existing_users = errors = 0
            users_with_errors = []
            for row in reader:
                print (row['id'])

                if row['id']:
                    try:
                        case, created = _model.objects.get_or_create(
                            case_id=row['id'],handledby_id=row['handledby_id'] ,customer_id=row['customer_id'])

                        if created:
                            case.casetype = row['casetype']
                            case.scheduledate = row['scheduledate']
                            case.time = row['time']
                            case.action = row['action']
                            case.suggest = row['suggest']
                            case.comment = row['comment']
                            case.iscompleted = row['iscompleted']



                            case.save()

                            created_users += 1
                        else:
                            existing_users += 1

                        print('{0} - {1}'.format(row['case_id'], 'Created' if created else 'Exist'))

                    except Exception as e:
                        errors += 1
                        print(e)




