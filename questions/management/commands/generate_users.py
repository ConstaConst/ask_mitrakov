from django.core.management.base import BaseCommand
from questions.models import ProfileManager, Profile
from questions.management.commands.generating_utils import generate_word


class Command(BaseCommand):
    help = "Generate some users Profiles"

    def handle(self, *args, **options):
        if len(args) > 0:
            n = args[0]
        else:
            n = 10
        for i in range(n):
            name = generate_word(10)
            profile = ProfileManager()
            profile = profile.create_user(
                username=name, email=name + "@pochta.qw", password=name + "password",
                nickname=name + "Nickname", avatar="static/img/default_avatar.png")
            profile.save()
            self.stdout.write(self.style.SUCCESS("Successfully created profile: "
                                                 + profile.nickname + " | " + profile.user.password))
