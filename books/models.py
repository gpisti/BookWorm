from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name="Szerző neve")
    bio = models.TextField(blank=True, null=True, verbose_name="Életrajz")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Cím")
    
    authors = models.ManyToManyField(
        Author, 
        related_name="books", 
        verbose_name="Szerző(k)"
    )
    
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True, verbose_name="ISBN szám")
    publication_year = models.IntegerField(blank=True, null=True, verbose_name="Kiadás éve")
    cover_image_url = models.URLField(blank=True, null=True, verbose_name="Borítókép URL")

    def __str__(self):
        return self.title

class UserBook(models.Model):
    
    class Status(models.TextChoices):
        TO_READ = 'TR', 'Olvasni fogom'
        READING = 'RG', 'Éppen olvasom'
        READ = 'RD', 'Elolvasva'

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="user_books",
        verbose_name="Felhasználó"
    )
    
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE,
        related_name="user_entries",
        verbose_name="Könyv"
    )

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.TO_READ,
        verbose_name="Státusz"
    )
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True, null=True,
        verbose_name="Értékelés (1-5)"
    )
    
    private_notes = models.TextField(
        blank=True, null=True, 
        verbose_name="Személyes jegyzetek"
    )

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"