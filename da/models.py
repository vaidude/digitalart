from django.db import models

from django.utils import timezone
class Artist(models.Model):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    gender_choices=(
        ('MALE','male'),
        ('FEMALE','female'),
        ('OTHERS','others'),
        )
    gender=models.CharField(choices=gender_choices,max_length=100,null=True,blank=True)
    image=models.ImageField(upload_to='userimg/',null=True,blank=True)
    dob=models.DateField(null=True)
    phonenumber=models.IntegerField(null=True)

    def __str__(self):
        return self.username   

    
class Buyer(models.Model):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    gender_choices=(
        ('MALE','male'),
        ('FEMALE','female'),
        ('OTHERS','others'),
        )
    gender=models.CharField(choices=gender_choices,max_length=100,null=True,blank=True)
    image=models.ImageField(upload_to='userimg/',null=True,blank=True)
    dob=models.DateField(null=True)
    phonenumber=models.IntegerField(null=True)
    address=models.CharField(max_length=50,null=True,blank=True)
    

    def __str__(self):
        return self.username

from django.db import models


class Logo(models.Model):
    user = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    logo_data = models.TextField(null=True, blank=True)  # To store JSON (editable canvas data)
    logo_image = models.ImageField(upload_to='logos/', null=True, blank=True)  # Optional image field
    
    def __str__(self):
        return self.name

class Portraits(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='artworks/%Y/%m/', null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title
    

class Payment(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    portrait = models.ForeignKey(Portraits, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for {self.portrait.title}'
    


class Room(models.Model):
    room_name = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{str(self.room)} - {self.sender}"

class Feedback(models.Model):
   RATING_CHOICES = [
      (1, '1'),
      (2, '2'),
      (3, '3'),
      (4, '4'),
      (5, '5'),
      ]
   feedback_text = models.TextField() 
   rating = models.IntegerField(choices=RATING_CHOICES) 
   created_at = models.DateTimeField(auto_now_add=True)
   email = models.EmailField()
   def str(self):
      return f"Rating: {self.rating}, feedback: {self.feedback_text[:50]}..."
  
  
class ProductFeedback(models.Model):
   RATING_CHOICES = [
      (1, '1'),
      (2, '2'),
      (3, '3'),
      (4, '4'),
      (5, '5'),
      ]
   product = models.ForeignKey(Portraits, on_delete=models.CASCADE)
   feedback_text = models.TextField() 
   rating = models.IntegerField(choices=RATING_CHOICES) 
   created_at = models.DateTimeField(auto_now_add=True)
   email = models.EmailField()
   def str(self):
      return f"Rating: {self.rating}, feedback: {self.feedback_text[:50]}..."
  
# class Notification(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  # Assuming the artist is a User
#     message = models.TextField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Notification for {self.artist.username}: {self.message}"
    
class PostModel(models.Model):
    user = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='posts')
    post_pic = models.ImageField(upload_to='posts/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    liked_users = models.ManyToManyField(Buyer, related_name='liked_posts', blank=True)  # Fixed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.email} - {self.description[:20]}"

    
class CommentSectionModel(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"





        
from django.db import models

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(Buyer, on_delete=models.CASCADE)  # Adjust based on your auth system
    portrait=models.ForeignKey(Portraits, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Other fields like order_total, items, etc.

from django.utils.timezone import now

class ChatMessage(models.Model):
    sender = models.CharField(max_length=100)  # Artist or Buyer username
    receiver = models.CharField(max_length=100)  # Receiver's username
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    media=models.FileField(upload_to='chat_media/',null=True,blank=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"
    
from django.db import models


class Spam(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  # Artist being reported
    reports = models.IntegerField(default=0)  # Track number of reports

    def increment_report(self):
        self.reports += 1
        if self.reports > 3:
            self.artist.is_active = False  # Ban the artist
            self.artist.save()
        self.save()
