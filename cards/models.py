from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Categories to group flashcard sets (e.g., Science, History)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class FlashcardSet(models.Model):
    """A set of flashcards created by a user"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name="sets", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="sets", on_delete=models.CASCADE)  # User who created the set
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Flashcard(models.Model):
    """Individual flashcards in a set"""
    set = models.ForeignKey(FlashcardSet, related_name="flashcards", on_delete=models.CASCADE)
    term = models.CharField(max_length=255)
    definition = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.term}: {self.definition[:30]}..."  # Preview the term and part of definition

    class Meta:
        ordering = ['created_at']  # Order flashcards by creation time


class FlashcardReview(models.Model):
    """User interactions with flashcards (for reviews or quizzes)"""
    flashcard = models.ForeignKey(Flashcard, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, "Hard"), (2, "Medium"), (3, "Easy")])  # Rating the difficulty of the flashcard
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.flashcard.term}"
