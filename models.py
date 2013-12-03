from django.db import models
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField


class MediaItem(models.Model):
    image = FilerImageField(
        null=True, blank=True,
        default=None, verbose_name='image',
        related_name='image item')
    video = FilerFileField(
        verbose_name='movie file',
        help_text='use .flv file or h264 encoded video file',
        blank=True, null=True)
    video_url = models.CharField(
        'movie url',
        max_length=255,
        help_text='vimeo or youtube video url. \
        Example: http://www.youtube.com/watch?v=YFa59lK-kpo',
        blank=True, null=True)
    image_url = models.CharField(
        'image url',
        max_length=255,
        help_text='vimeo or youtube video url. \
        Example: http://www.youtube.com/watch?v=YFa59lK-kpo',
        blank=True, null=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if (self.image and (self.video or self.video_url or self.image_url)) \
           or (self.video and (self.image or self.video_url or self.image_url)) \
           or (self.image_url and (self.image or self.video_url or self.video)) \
           or (self.video_url and (self.video or self.image or self.image_url)):
            raise ValidationError(
                'you must choose only an image or a video or a video_url')

        if not (self.image or self.video_url or self.video):
            raise ValidationError(
                'You must provide at least one media')

        if self.video:
            raise ValidationError(
                'Video Files is not yet implemented')

    class Meta:
        verbose_name = "Media Item"

    def __unicode__(self):
        if self.image:
            return u'Media Item: image > %s' % self.image
        elif self.video_url:
            return u'Media Item: video > %s' % self.video_url
        elif self.video:
            return u'Media Item: video > %s' % self.video
        else:
            return u'Media Item: Empty!'


class MediaViewer(CMSPlugin):

    SLIDE_TYPE = (
        ('carousel', 'carousel'),
        ('shadowbox', 'shadowbox'),
    )

    title = models.CharField('Title', max_length=255, blank=True, null=True)
    slide_type = models.CharField(
        max_length=5, choices=SLIDE_TYPE, default='carousel')
    medias = models.ManyToManyField(MediaItem)

    def clean(self):
        #import pudb
        #pudb.set_trace()
        #from django.core.exceptions import ValidationError
        #if not self.medias:
        #    raise ValidationError(
        #        'You must provide medias')
        pass

    class Meta:
        verbose_name = "Media Viewer"

    def copy_relations(self, oldinstance):
        self.medias = oldinstance.medias.all()

    def __unicode__(self):
        return u'Media Viewer'
