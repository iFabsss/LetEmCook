from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import uuid
import boto3
       
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='users/', blank=True, null=True, default='users/default_profile_img.png')
    friendship = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='friends')
    bio = models.TextField(blank=True, null=True, default='This user has not set a bio yet.')

    def __str__(self):
        return self.user.username
    

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.CharField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Recipe.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

        # Upload image to S3 if new image is provided
        if self.image and not self.image.name.startswith(f"{settings.MEDIA_URL}"):
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            image_content = self.image.read()
            s3_key = f'recipes/{self.image.name.split("/")[-1]}'

            s3.upload_fileobj(
                Fileobj=self.image.file,
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=s3_key,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': self.image.file.content_type
                }
            )

            # Set the image URL to the public S3 URL
            self.image.name = f'{settings.MEDIA_URL}/{s3_key}'
            super().save(update_fields=['image'])

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'recipe_id': self.id, 'slug': self.slug})
    
    

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='comments/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
     # Upload image to S3 if new image is provided
        if self.image and not self.image.name.startswith(f"{settings.MEDIA_URL}"):
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            image_content = self.image.read()
            s3_key = f'recipes/{self.image.name.split("/")[-1]}'

            s3.upload_fileobj(
                Fileobj=self.image.file,
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=s3_key,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': self.image.file.content_type
                }
            )

            # Set the image URL to the public S3 URL
            self.image.name = f'{settings.MEDIA_URL}/{s3_key}'
            super().save(update_fields=['image'])

    def __str__(self):
        return f'Comment by {self.user.username} on {self.recipe.title}'
    
def generate_code():
    return '{:06d}'.format(random.randint(0, 999999))

class EmailMFA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def regenerate(self):
        self.code = generate_code()
        self.created_at = timezone.now()
        self.save()
# Create your models here.

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)