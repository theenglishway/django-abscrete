.. image::  https://travis-ci.org/theenglishway/django-abscrete.svg?branch=master
    :target: http://travis-ci.org/theenglishway/django-abscrete
.. image:: https://img.shields.io/codecov/c/github/dtheenglishway/django-abscrete/master.svg
    :target: https://codecov.io/github/theenglishway/django-abscrete?branch=master


Abscrete Models
***************

Concept
=======

Abscrete models are models that are both abstract and concrete, hence their name.
They allow you to use Django's model inheritance in a transparent way and with a
minimal overhead.

Abscrete models are concrete because each model in your hierarchy will have its own
database table, just like any Django model.

... and they are abstract because you will never get access to a model in your
hierarchy that doesn't "mean" anything.

They are basically a version of the Polymorphic models from
`django-polymorphic <https://django-polymorphic.readthedocs.io/>`_ that uses
meta-programming instead of ContentTypes

A simple example
================

The only change you'll need in your app design is to derive your models from
``AbscreteModel`` instead of Django's ``models.Model``::

    from abscrete.models import AbscreteModel

    class CreativeWork(AbscreteModel):
        creator = models.ForeignKey(User)
        date_created = models.DateField()

    class Article(CreativeWork):
        text = models.TextField()

    class NewsArticle(Article):
        newspaper_name = models.CharField(max_number=100)
    class SocialMediaPosting(Article):
        url = models.URLField()

    class Movie(CreativeWork):
        duration_in_seconds = models.PositiveIntegerField()

(Using http://schema.org/docs/full.html as an inspiration)

Once you've designed such a hierarchy, the only objects you ever want to play
with are those that have a complete implementation (ie NewsArticle,
SocialMediaPosting, or Movie). So let's create a few of them :

>>> NewsArticle.objects.create(title='Abscrete Models are cool',
                               creator='theenglishway',
                               text='They really are',
                               newspaper_name='Django papers')
>>> SocialMediaPosting.objects.create(title='Abscrete Models are lame',
                                      creator='thefrenchway',
                                      text='Dont use them',
                                      url='http://anti-abscrete.org')
>>> Movie.objects.create(title='Why dont you try them ?',
                         creator='thebalancedway',
                         duration_in_minutes=10)

But still, you'd like to make queries on all creative works, or all articles.
Here's what Django would return in this case :

>>> CreativeWork.objects.all()
<AbscreteQuerySet [<CreativeWork: Abscrete Models are cool>,
                   <CreativeWork: Abscrete Models are lame>,
                   <CreativeWork: Why dont you try them ?>]>

Which one is of which type ?

Now here's what django-abscrete will return :

>>> CreativeWork.objects.all()
<AbscreteQuerySet [
    <NewsArticle: Abscrete Models are cool, published in Django papers>,
    <SocialMediaPosting: Abscrete Models are lame, published @ http://anti-abscrete.org>,
    <Movie: Why dont you try them ?, 10 minute-long>
]>

Querying any of the intermediate models also does the job :

>>> Article.objects.all()
<AbscreteQuerySet [
    <NewsArticle: Abscrete Models are cool, published in Django papers>,
    <SocialMediaPosting: Abscrete Models are lame, published @ http://anti-abscrete.org>
]>


Versions supported
==================

Python 2.7 / Django 1.5 up to 1.11.
Python 3.4-3.5-3.6 / Django 1.5 up to 1.11 and current master.
