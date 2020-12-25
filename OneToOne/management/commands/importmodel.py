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
                print (row['customercode_id'])
                print (row['invitationcode'])
                if row['contactname']:
                    try:
                        customer, created = _model.objects.get_or_create(
                            contactname=row['contactname'] , customercode_id=row['customercode_id'] , invitationcode = row['invitationcode'])

                        if created:
                            customer.companyname = row['companyname']

                            customer.billingaddress = row['billingaddress']
                            customer.installaddress = row['installaddress']
                            customer.contactno = row['contactno']
                            customer.mobile = row['mobile']
                            customer.email = row['email']

                            customer.joindate = row['joindate']
                            customer.source = row['source']
                            customer.isconfirm = row['isconfirm']
                            customer.save()

                            created_users += 1
                        else:
                            existing_users += 1

                        print('{0} - {1}'.format(row['contactname'], 'Created' if created else 'Exist'))

                    except Exception as e:
                        errors += 1
                        print(e)




