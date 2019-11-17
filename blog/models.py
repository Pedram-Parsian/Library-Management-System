from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone
from lms.utilities import convert_range, get_gravatar_url
from users.models import User, Member


class PostManager(models.Manager):
    def get_archive(self, year, month):
        return self.filter(status='published').filter(date_published__year=year, date_published__month=month)


class Post(models.Model):
    DRAFT = 10
    PUBLISHED = 20
    WITHDRAWN = 30
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (WITHDRAWN, 'Withdrawn'),
    )
    # todo `REGISTERED ONLY POSTS` + `SPECIAL MEMBERS POSTS`
    image = models.ImageField(upload_to='static_img/', null=True, blank=True)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    body = models.TextField(max_length=200000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)
    liked_by = models.ManyToManyField(User, blank=True)
    tags = models.ManyToManyField('PostTag', blank=True)
    categories = models.ManyToManyField('PostCategory', blank=True)

    objects = PostManager()

    def is_new(self):
        if self.date_published:
            return timezone.now() - \
                   timedelta(days=settings.DEFAULT_POST_NEW_DAYS) <= self.date_published <= timezone.now()
        else:
            return False

    def get_likes_count(self):
        return self.liked_by.count()

    def get_comments_count(self):
        return PostComment.objects.filter(status=PostComment.APPROVED).filter(post=self).count()

    @staticmethod
    def get_archives():
        archive = []
        for date in Post.objects.filter(status='published').values_list('date_published', flat=True):
            if (date.strftime('%B %Y'), date.strftime('%Y'), date.strftime('%m')) not in archive:
                archive.append((date.strftime('%B %Y'), date.strftime('%Y'), date.strftime('%m')))
        return archive

    def get_post_score(self):
        comments_count = self.get_comments_count()
        likes_count = self.get_likes_count()
        views_count = 5
        return (likes_count * 3) + (comments_count * 2) + views_count

    @staticmethod
    def get_popular_posts():
        return sorted(Post.objects.filter(status='published'), key=lambda t: t.get_post_score(), reverse=True)[:5]

    def get_related_posts(self):
        # get posts with same tags _or_ same categories
        # we are using sets to ensure that there is no duplication
        related_posts = set()
        for tag in self.tags.all():
            posts_with_tag = tag.post_set.all()
            # the if statement is to prevent adding 'current' post to the 'related' posts
            related_posts.update([_ for _ in posts_with_tag if _.pk != self.pk])
        for category in self.categories.all():
            posts_with_category = category.post_set.all()
            # the if statement is to prevent adding 'current' post to the 'related' posts
            related_posts.update([_ for _ in posts_with_category if _.pk != self.pk])
        # if these related posts were 3 or more, that's ok,
        # but if not, we will add some other posts to it based on score:
        if len(related_posts) < 3:
            related_posts.update([x for x in Post.get_popular_posts()])
        return sorted(related_posts, key=lambda t: t.get_post_score(), reverse=True)[:3]

    def get_tags(self):
        return ",".join([x.title for x in self.tags.all()])

    def __str__(self):
        return self.title


class PostTag(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    def get_post_count(self):
        return self.post_set.count()

    @staticmethod
    def get_all_with_size():
        TAG_MIN_SIZE = 8
        TAG_MAX_SIZE = 25
        result = {}
        for tag in PostTag.objects.all():
            tag_post_count = tag.get_post_count()
            if tag_post_count > 0:
                result[tag] = tag_post_count
        if result:
            min_repeat_tag = min(result.values())
            max_repeat_tag = max(result.values())
            if min_repeat_tag == max_repeat_tag:
                # handle the situation when there is only one tag, or 'n' tags with equal post_count
                # if not handled, we will get a DivisionByZero error while converting random_string_generator
                for tag, repeated_time in result.items():
                    result[tag] = (TAG_MAX_SIZE + TAG_MIN_SIZE) / 2
                return result.items()
            for tag, repeated_time in result.items():
                result[tag] = convert_range(min_repeat_tag, max_repeat_tag, TAG_MIN_SIZE, TAG_MAX_SIZE, repeated_time)
            return sorted(result.items(), key=lambda item: item[0].title)

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    def get_post_count(self):
        return self.post_set.count()

    def __str__(self):
        return self.title


class PostComment(models.Model):
    APPROVED = 10
    REFUSED = 20
    WAITING = 30
    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (REFUSED, 'Refused'),
        (WAITING, 'Waiting...')
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    text = models.TextField(max_length=600)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)

    def get_avatar(self):
        if not self.member_id:
            return get_gravatar_url(self.email)
        return self.member.user.get_avatar()

    def get_info(self):
        if self.member_id:
            return self.member.user.first_name, self.member.user.last_name
        else:
            return self.name, None

    def __str__(self):
        name, family = self.get_info()
        if self.parent:
            return f'"{name} {family}" on "{self.post.title}" (child comment)'
        return f'"{name} {family}" on post "{self.post.title}"'
