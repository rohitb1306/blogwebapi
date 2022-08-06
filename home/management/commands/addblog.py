from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from blog.models import Blog
from faker import Faker

from account.models import MyUser


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "number",
            type=int,
            help="how many blogs to add maximum 15 at a time",
        )

    def handle(self, *args, **options):

        if options["number"] < 15:
            for i in range(options["number"]):
                f = Faker()
                user_object = MyUser.objects.filter(is_auther=True)
                blog_object = Blog(
                    blog_title=f.sentence(),
                    blog_content="\n".join(f.sentences(nb=4)),
                    blog_keywords='","'.join(f.sentences(nb=3)),
                    blog_description=f.paragraph(nb_sentences=1),
                    blog_new_request=False,
                    blog_is_approved=True,
                    blog_auther=get_object_or_404(
                        MyUser, id=user_object[0].id
                    ),
                )
                blog_object.save()
            self.stdout.write(self.style.SUCCESS("added blog"))
        else:
            raise CommandError("wrong argument")
