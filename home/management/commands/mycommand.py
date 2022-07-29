# from django.core.management.base import BaseCommand, CommandError


# class Command(BaseCommand):

#     def add_arguments(self, parser):
#         parser.add_argument('first', type=str, help="a three letter string")
#         parser.add_argument('-A', default="default", help="option one value")

#     def handle(self, *args, **options):

#         if len(options['first']) < 4:
#             self.stdout.write(self.style.SUCCESS('write argument'))
#         else:
#             raise CommandError("wrong argument")

#         # print('command:mycommand')
#         # print(f'First:{options["first"]}')
#         # print(f'A:{options["A"]}')
