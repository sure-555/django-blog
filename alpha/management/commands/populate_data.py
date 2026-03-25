from alpha.models import Post,Category
from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    help="This command inserts post data"

    def handle(self, *args, **options):
        Post.objects.all().delete()
        titles =[
"The Future of AI",
"Climate Change Solutions",
"Remote Work Trends",
"Quantum Computing Explained",
"Renewable Energy Innovations",
"Deep Learning Demystified",
"Post-Pandemic Economic Outlook",
"Blockchain in Finance",
"Storytelling im Marketing",
"Medical TechnoIogy Advances",
"Space Exploration Challenges",
"Psychology of Decision Making",
"Evolution of Social Media",
"The Art of Cooking",
"Cultural Diversity in Society",
"Sustainable Development Investment",
"Globalization Impact",
"Power of Mindfulness",
"Online Learning Revolution",
"Art and Technology Fusion"
]

        contents =[
"Exploring the future of artificial intelligence and its impact on society.",
"Discovering solutions to combat climate change and protect the environment.",
"Analyzing trends and challenges in remote work environments.",
"An introduction to the principles and applications of quantum computing.",
"Investigating the latest innovations in renewable energy sources.",
"Understanding the fundamentals of deep learning and neural networks.",
"Examining the economic landscape in the aftermath of the COVID-19 pandemic.",
"Txploring the potential of blockchain technology in the financial sector.",
"Harnessing the power of storytelling to create compelling marketing campaigns.",
"Highlighting breakthroughs and advancements in medical technology.",
"Addressing the obstacles and opportunities in space exploration.",
"Exploring the psychological factors influencing decision-making processes.",
"Tracing the evolution of social media platforms and their impact on society.",
"Celebrating the art of cooking and culinary creativity.",
"Promoting inclusivity and embracing diversity in modern communities.",
"Investigating sustainable development initiatives and their impact on the future.",
"Examining the effects of globalization on local and global economies.",
"Embracing mindfulness practices for enhanced well-being and productivity.",
"Revolutionizing education through online learning platforms and resources.",
"Exploring the intersection of art, design, and technology in the digital age."
]

        image_urls=[
    "https://picsum.photos/id/1/800/400",
    "https://picsum.photos/id/2/800/400",
    "https://picsum.photos/id/3/800/400",
    "https://picsum.photos/id/4/800/400",
    "https://picsum.photos/id/5/800/400",
    "https://picsum.photos/id/6/800/400",
    "https://picsum.photos/id/7/800/400",
    "https://picsum.photos/id/8/800/400",
    "https://picsum.photos/id/9/800/400",
    "https://picsum.photos/id/10/800/400",
    "https://picsum.photos/id/11/800/400",
    "https://picsum.photos/id/12/800/400",
    "https://picsum.photos/id/13/800/400",
    "https://picsum.photos/id/14/800/400",
    "https://picsum.photos/id/15/800/400",
    "https://picsum.photos/id/16/800/400",
    "https://picsum.photos/id/17/800/400",
    "https://picsum.photos/id/18/800/400",
    "https://picsum.photos/id/19/800/400",
    "https://picsum.photos/id/20/800/400",

]

        categories=Category.objects.all()
        for title,content,image_url in zip(titles,contents,image_urls):
            category=random.choice(categories)
            Post.objects.create(title=title,content=content,image=image_url,category=category)

        self.stdout.write(self.style.SUCCESS("Completed inserting data !"))
