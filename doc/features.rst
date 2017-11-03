Features
========


Getting an object
-----------------

Getting an object always returns a concrete instance :

>>> CreativeWork.objects.get(pk=2)
<SocialMediaPosting: Abscrete Models are lame, published @ http://anti-abscrete.org>


Filtering
---------

Filtering can be done on any field of the root model :

>>> CreativeWork.objects.filter(title='Why dont you try them ?')
<AbscreteQuerySet [
    <Movie: Why dont you try them ?, 10 minute-long>
]>

... or on any field of the children objects, using Django's natural syntax (
AbscreteQuerySet work just like any Django's queryset on OneToOneField
relations) :

>>> Article.objects.filter(newsarticle__newspaper_name='Django papers')
<AbscreteQuerySet [
    <NewsArticle: Abscrete Models are cool, published in Django papers>
]>
