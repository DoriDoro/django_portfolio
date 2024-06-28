from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError

UserModel = get_user_model()


class Command(BaseCommand):
    """
    This command is designed to create a superuser with a specified email and password.
    If a superuser with the same email already exists, it will print a warning message.
    Otherwise, it will create the superuser and print a success message.

    Command:
        $ python manage.py create_superuser

    Attributes:
        help (str): Description of the command.

    Methods:
        handle(self, *args, **options): Executes the command to create a superuser.
            Args:
                *args: Variable length argument list.
                **options: Arbitrary keyword arguments.

            Returns:
                None

            Raises:
                IntegrityError: If a superuser with the same email already exists.
    """

    help = "This command creates a superuser."

    def handle(self, *args, **options):
        try:
            if not UserModel.objects.filter(username="Admin").exists():
                raw_password = input("Please enter the password for Admin: ")

                UserModel.objects.create_superuser(
                    username="Admin", email="admin@mail.com", password=raw_password
                )
        except IntegrityError:
            self.stdout.write(self.style.WARNING("This superuser exists already!"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser successfully created!"))
