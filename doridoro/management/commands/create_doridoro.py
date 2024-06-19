from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import DoriDoro

UserModel = get_user_model()


class Command(BaseCommand):
    help = "This command creates one DoriDoro instance."

    # for later...
    # client = models.ForeignKey()
    # review = models.ForeignKey()

    def handle(self, *args, **options):
        if (
            not DoriDoro.objects.exists()
            and not UserModel.objects.filter(username="doridoro").exists()
        ):
            try:
                raw_password = input("Please enter the password for DoriDoro: ")

                profile_description = """
                I am a composed and well-balanced individual who thrives on activity and continuous 
                learning. Diligence characterizes my approach, as I am quick to grasp new concepts 
                and adapt to new challenges. My reliability and sensitivity make me a trusted 
                team member, and I prioritize effective communication and organization in all 
                endeavors.
    
                Driven by high personal standards, I exhibit a penchant for perfectionism in 
                specific areas, particularly in programming. I am committed to elevating my skills 
                and expectations in this field, aspiring to become a dependable and esteemed asset 
                within my future organization.
    
                Throughout my career, I have cultivated a collaborative mindset, recognizing the 
                importance of teamwork in achieving collective goals. I derive satisfaction from 
                working alongside others and contributing to a supportive and cohesive team 
                environment. While valuing teamwork, I also relish opportunities for independent 
                work and initiative.
                """
                dream_job_description = """
                I possess a keen curiosity to understand the entirety of processes, striving to 
                grasp the 'big picture' to comprehend the why, how, and what of tasks. I 
                prioritize comprehension over rote learning, seeking to fully understand the task 
                at hand to effectively prioritize my focus. A culture of feedback and open 
                communication is indispensable to me, as I value insights into areas where I can 
                improve and grow.
    
                With a preference for home office work, I leverage my organizational prowess and 
                ability to prioritize tasks efficiently, ensuring timely completion of assignments.
                My quick comprehension allows me to grasp concepts rapidly when presented clearly, 
                contributing to my independence and personal responsibility in task execution. 
                Driven by determination and conscientiousness, I consistently deliver reliable and 
                high-quality work, refusing to give up until tasks are completed to satisfaction.
    
                I acknowledge my weaknesses, including introversion and shyness, yet I actively 
                work to overcome these barriers through continuous learning and self-improvement. 
                While small talk may not come naturally to me, I excel in problem-solving and 
                effective communication when tackling substantive challenges. Furthermore, I 
                confront perfectionism by striving for improvement rather than flawlessness, 
                recognizing the importance of progress over perfection.
    
                My soft skills, including effective communication, attention to detail, and 
                adaptability, complement my technical proficiency in programming. Proficient in 
                Python, Django, Django REST Framework, Flask, and related tools such as Unittest, 
                Pytest, and CLI applications, I excel in software development. Additionally, my 
                expertise extends to version control with Git and GitHub, deployment with Heroku, 
                Vercel, and Render, and database management with SQLite, PostgreSQL, and SQL.
    
                Furthermore, I am well-versed in UML, wireframing, user stories, and 
                entity-relationship diagrams, enhancing my ability to conceptualize and 
                develop robust software solutions. Leveraging tools like Sentry, Docker, Celery, 
                and PyCharm, I ensure the reliability, scalability, and efficiency of my projects, 
                consistently adhering to best practices and industry standards.
                """
                free_time_description = """
                I would like to have time for a dog again. I really miss the morning walks with my 
                dog to start the day with positive energy. My aim is to find a better balance 
                between my life and my needs, those of my son and the demands of my future job. In 
                the morning, I need time for myself, to find the strength and energy I need for the
                hole day, to concentrate and to do something good for my body. I like sitting in 
                front of the computer, but you also need time to exercise and channel your energy. 
                Organizing my energy in the evening does not work as well as it does in the 
                morning. 
    
                In the evening, I like to watch films and take a break from my day. I like 
                spending time with animals, especially dogs and horses. Some time ago, I have 
                bought a little pony for my son and me. I love spending time with animals. This 
                pony is so adorable and it gives me so much strength back. Once a week I am able 
                to take riding lessens. This horse is amazing, the bond I feel to him is really 
                fascinating. 
    
                I like to talk with my family and my best friend. I really enjoy exchanging 
                information on specific subjects, small-talk is difficult for me. I like to share 
                my knowledge, I like to teach others and I'm a good listener. For some time now, 
                I've been reading articles on Medium or Dev.io to refine my knowledge. I've also 
                written articles on Dev.io.
                """

                with transaction.atomic():
                    user = UserModel.objects.create_user(
                        username="doridoro",
                        password=raw_password,
                        email="dorothea.reher@gmail.com",
                        first_name="Dorothea",
                        last_name="Reher",
                    )
                    DoriDoro.objects.create(
                        user=user,
                        phone="0033768132147",
                        address="35710 Bruz in France",
                        profession="Python/Django Developer",
                        introduction=profile_description,
                        dream_job=dream_job_description,
                        free_time=free_time_description,
                    )

            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING("An instance of DoriDoro exists already!")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"An unexpected error occurred: {e}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("DoriDoro instance successfully created!")
                )
        else:
            self.stdout.write(self.style.WARNING("A DoriDoro instance exists already!"))
