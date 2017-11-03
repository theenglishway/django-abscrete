from django.db import models
from abscrete.models import AbscreteModel


class CreativeWork(AbscreteModel):
    title = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Article(CreativeWork):
    text = models.TextField()


class NewsArticle(Article):
    newspaper_name = models.CharField(max_length=100)

    def __str__(self):
        return '%s, published in %s' % (self.title, self.newspaper_name)


class SocialMediaPosting(Article):
    url = models.URLField()

    def __str__(self):
        return '%s, published @ %s' % (self.title, self.url)


class Movie(CreativeWork):
    duration_in_minutes = models.PositiveIntegerField()

    def __str__(self):
        return '%s, %i minute-long' % (self.title, self.duration_in_minutes)
