from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
import time
import models


class MediaViewerPlugIn(CMSPluginBase):
    model = models.MediaViewer
    name = 'Media Viewer'
    render_template = 'media_viewer.html'
    # raw_id_fields = ('medias',)
    filter_horizontal = ('medias',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slide_type', 'medias'),
        }),
        ('More', {
            'classes': ('collapse',),
            'fields': ('width', 'height'),
        }),
    )

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'time': '-'.join([
                str(instance.id),
                repr(time.time()).replace('.', '_')]),
        })
        return context

plugin_pool.register_plugin(MediaViewerPlugIn)
