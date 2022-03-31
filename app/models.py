from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class User(db.Model):
  __tablename__= 'users'
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(25), nullable=False)
  last_name = db.Column(db.String(25), nullable=False)
  username = db.Column(db.String(30), nullable=False, unique=True)
  profile_image = db.Column(db.String)
  bio = db.Column(db.String(150))
  email = db.Column(db.String(255), nullable=False, unique=True)
  hashedpassword = db.Column(db.String(50), nullable=False)
  created_at = db.Column(db.DateTime)
  updated_at = db.Column(db.DateTime)

  posts = db.relationship("Post", back_populates="users")
  likes = db.relationship("Like", back_populates="users")
  comments = db.relationship("Comment", back_populates="users")

  followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

  def follow(self, user):
    if not self.is_following(user):
        self.followed.append(user)

  def unfollow(self, user):
    if self.is_following(user):
        self.followed.remove(user)

  def is_following(self, user):
    return self.followed.filter(
        followers.c.followed_id == user.id).count() > 0

# Followed posts query
# class User(UserMixin, db.Model):
#   #...
#   def followed_posts(self):
#       return Post.query.join(
#           followers, (followers.c.followed_id == Post.user_id)).filter(
#               followers.c.follower_id == self.id).order_by(
#                   Post.timestamp.desc())

class Post(db.Model):
  __tablename__= 'posts'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
  caption = db.Column(db.String(2000))
  image = db.Column(db.ARRAY(db.String), nullable=False)
  created_at = db.Column(db.DateTime)
  updated_at = db.Column(db.DateTime)

  users = db.relationship("User", back_populates="posts")
  comments = db.relationship("Comment", back_populates="posts")
  likes = db.relationship("Like", back_populates="posts")

class Comment(db.Model):
  __tablename__= 'comments'
  id = db.Column(db.Integer, primary_key=True)
  post_id = db.Column(db.Integer, ForeignKey("posts.id"), nullable=False)
  user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
  content = db.Column(db.String(2000), nullable=False)
  created_at = db.Column(db.DateTime)
  updated_at = db.Column(db.DateTime)

  posts = db.relationship("Post", back_populates="comments")
  users = db.relationship("User", back_populates="comments")

class Like(db.Model):
  __tablename__= 'likes'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
  post_id = db.Column(db.Integer, ForeignKey("posts.id"), nullable=False)
  created_at = db.Column(db.DateTime)
  updated_at = db.Column(db.DateTime)

  users = db.relationship("User", back_populates="likes")
  posts = db.relationship("Post", back_populates="likes")
