from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Job


class Command(BaseCommand):
    help = "This command creates all Job instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            jobs = [
                {
                    "company_name": "Cocoonr Hosting Power and Book&Pay",
                    "position": "Apprenticeship as Python Developer",
                    "start_date": "2022-11-21",
                    "until_present": True,
                    "address": "Rennes (FRANCE)",
                    "description": """I have effectively utilized Notion as an integral tool for 
                    managing project workflows. My expertise includes working on tasks within 
                    Notion, where I have seamlessly created, tracked, and completed independently 
                    various project assignments, ensuring timely delivery and adherence to 
                    project goals. Proficient in handling database requests and exporting data 
                    into CSV files. Responsible for managing the internal Slack chat 
                    "Assistance Technique," where colleagues report bugs, problems, and server 
                    errors. Skilled in checking Sentry for errors and identifying issues promptly. 
                    Experienced in verifying bugs, resolving them, or creating development 
                    requests as necessary. Capable of analyzing code to provide explanations for 
                    issues and propose solutions. Enhanced understanding of website operations 
                    and management through problem-solving activities. Proficient in generating 
                    scripts with templates for inserting new data, such as new cities, into the 
                    database. Skilled in implementing new dashboard modules and assembling custom 
                    code modules to create innovative dashboard features.
                    """,
                    "job_type": Job.APPRENTICESHIP,
                },
                {
                    "company_name": "",
                    "position": "Parental Leave",
                    "start_date": "2020-09-01",
                    "end_date": "2022-11-21",
                    "description": """Dedication to my family's needs and being present during 
                    key developmental stages of my child's life. Grow personally and develop 
                    important skills such as patience, time management, and multitasking. 
                    Maintain a healthy work-life balance by taking time off to prioritize family
                    while also recognizing the significance of personal and professional 
                    development.
                    """,
                    "job_type": Job.PARENTAL_LEAVE,
                },
                {
                    "company_name": "Comdata (Nissan)",
                    "position": "Customer Support Agent (Helpdesk)",
                    "start_date": "2016-06-01",
                    "end_date": "2020-09-01",
                    "address": "Gennevilliers (FRANCE)",
                    "description": """Proficiently managed multilingual communication channels 
                    in both German and English, handling calls, chats, and emails with customers. 
                    Demonstrated efficiency in problem resolution by escalating technical issues
                    to relevant third-party providers, ensuring timely and effective solutions. 
                    Specialized expertise as a Telematics Agent (Helpdesk Agent), tasked with 
                    resolving inquiries and addressing issues pertaining to the onboard 
                    infotainment system and associated services within automotive environments. 
                    Utilized Salesforce CRM proficiently as a comprehensive recording and 
                    management system, facilitating streamlined documentation and tracking of 
                    customer interactions and resolutions.
                    """,
                    "job_type": Job.EMPLOYED,
                },
                {
                    "company_name": "",
                    "position": "Time of integration in France",
                    "start_date": "2015-05-01",
                    "end_date": "2016-06-01",
                    "description": """Proactively relocated to France, demonstrating adaptability
                    and a readiness to embrace new experiences. Engaged in the vibrant community 
                    of Paris as a dog walker, providing attentive care and companionship to pets 
                    while exploring the city's diverse neighborhoods.
                    """,
                    "job_type": Job.SABBATICAL,
                },
                {
                    "company_name": "Research Clinical Center of Freiburg im Breisgau",
                    "position": "Chemical Technical Assistant",
                    "start_date": "2008-06-01",
                    "end_date": "2015-02-01",
                    "address": "Freiburg im Breisgau (Germany)",
                    "description": """Autonomously managed projects under the supervision of 
                    senior leadership, demonstrating initiative and self-reliance in project 
                    execution. Proficiently analyzed project-generated data, translating findings
                    into visually informative graphs and reports to facilitate data-driven 
                    decision-making processes. Collaborated effectively with post-doctoral 
                    researchers, fostering teamwork and knowledge exchange to achieve project 
                    objectives efficiently.
                """,
                    "job_type": Job.EMPLOYED,
                },
                {
                    "company_name": "OpenClassrooms",
                    "position": "Path: Developer Python",
                    "start_date": "2022-11-21",
                    "until_present": True,
                    "address": "Home Office (FRANCE)",
                    "description": """Online training with OpenClassrooms, demonstrating 
                    dedication to self-improvement and professional development through distance 
                    learning. Successfully completed coursework and assignments from a home 
                    office environment, showcasing adaptability and self-discipline in remote 
                    work settings. Bachelor's-level diploma program, underscoring academic 
                    achievement and commitment to continuous learning and skill enhancement. 
                    BookScrape (Python): Data management via ETL, Git/GitHub version control, 
                    Python basics. 
                    Learn@Home: UML use case diagram, user stories, functional models, 
                    macro project breakdown with Kanban. 
                    ChessTournament (Python): Python code structuring with design patterns, 
                    PEP 8 adherence, object-oriented programming. 
                    JustStreamIt (JS): Interacting with REST APIs, front-end development with 
                    HTML/CSS/JS. 
                    AlgoInvest_trade (Python): Problem deconstruction, algorithm development. 
                    LITRevue (Django): Agile project management, functional requirement definition,
                    prototyping with domain models/mock-ups. 
                    SoftDesk (DRF): API security (OWASP/RGPD), Django REST API creation, Postman.
                    Gudlft (Flask): Python test suite implementation, error handling, environment
                    configuration, debugging. 
                    EpicEvents (Django): Secure database implementation with Python/SQL. 
                    OrangeCountryLettings (Django): Application documentation, technical debt 
                    reduction, Sentry code control, deployment, CI/CD methodology, modular 
                    Python architecture.
                    """,
                    "job_type": Job.FORMATION,
                },
                {
                    "company_name": "",
                    "position": "weekly mentor sessions with Django and OpenClassrooms Mentor",
                    "start_date": "2022-11-21",
                    "until_present": True,
                    "address": "Home Office (FRANCE)",
                    "description": """Engaged in distance learning mentor sessions with an 
                    OpenClassrooms mentor as part of my coursework. Utilizing the sessions to 
                    seek guidance and clarification on OpenClassrooms projects, ensuring 
                    comprehension and successful completion of assignments. Received 
                    personalized support and mentorship to navigate through the projects, 
                    benefiting from expert guidance and practical insights to enhance project 
                    understanding and execution.
                    """,
                    "job_type": Job.MENTORING,
                },
                {
                    "company_name": "",
                    "position": "weekly mentor sessions with Django Mentor",
                    "start_date": "2023-09-01",
                    "until_present": True,
                    "address": "Home Office (FRANCE)",
                    "description": """Comprehensive understanding of Django's core principles, 
                    including its processes, functionalities, and best practices. Received 
                    personalized guidance and support in effectively utilizing Django for 
                    project development, including practical insights into implementation 
                    strategies and optimization techniques. Additionally, received assistance 
                    with OpenClassrooms projects to deepen comprehension and refine project 
                    execution, enhancing overall learning outcomes and skill proficiency.
                    """,
                    "job_type": Job.MENTORING,
                },
                {
                    "company_name": "Ironhack Paris",
                    "position": "Web development bootcamp",
                    "start_date": "2019-08-01",
                    "end_date": "2019-10-01",
                    "address": "Paris (FRANCE)",
                    "description": """Completed a rigorous 3-month intensive bootcamp focused 
                    on becoming a proficient Full Stack Web Developer. Comprehensive instruction 
                    covering fundamental concepts and tools essential for full stack web 
                    development. Actively engaged in hands-on learning, culminating in the 
                    creation of personalized projects to solidify understanding and apply newly 
                    acquired skills.
                    """,
                    "job_type": Job.FORMATION,
                },
            ]

            if Job.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Job exists already!")
                )
                return

            with transaction.atomic():
                for job in jobs:
                    Job.objects.create(
                        **job,
                    )

            self.stdout.write(
                self.style.SUCCESS("Instances of Job successfully created!")
            )

        except IntegrityError:
            self.stdout.write(self.style.WARNING("These Job instances exists already!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
