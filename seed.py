from models import User, Post, db, DEFAULT_IMG_URL
from app import app

db.drop_all()
db.create_all()

robin = User(first_name='Robin', last_name='Williams', image_url='https://upload.wikimedia.org/wikipedia/commons/5/59/Robin_Williams_Happy_Feet_premiere.jpg')
ted = User(first_name='Ted', last_name='Mosby', image_url='https://home.adelphi.edu/~br21822/Ted.jpg')
maisy = User(first_name='Maisy', last_name='Sidekick', image_url=DEFAULT_IMG_URL)

robin_post = Post(title='I was Mrs. Doubtfire', content='It was filmed in San Francisco', user=robin)
ted_post = Post(title='How I met your mother', content='It was not Robin', user=ted)

db.session.add(robin)
db.session.add(ted)
db.session.add(maisy)
db.session.commit()

db.session.add(robin_post)
db.session.commit