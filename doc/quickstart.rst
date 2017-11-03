Quickstart
==========

Ever tried to deal with multi-table inheritance in Django ? Cumbersome isn't it ?

Derive your models from ``AbscreteModel`` instead of Django's ``models.Model``::

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

Let's create a few objects :

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

Now let's try to retrieve all creative works :

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

Django would have returned that :

>>> CreativeWork.objects.all()
<AbscreteQuerySet [<CreativeWork: Abscrete Models are cool>,
                   <CreativeWork: Abscrete Models are lame>,
                   <CreativeWork: Why dont you try them ?>]>

... leaving it up to you to figure out which models are from which concrete type.