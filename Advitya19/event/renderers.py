import json
from rest_framework.renderers import JSONRenderer


class EventJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)
        details = data.get('detail', None)

        if errors is not None:
            return super(EventJSONRenderer, self).render(data)
        if details is not None:
            return super(EventJSONRenderer, self).render(data)
        return json.dumps({
            'event': data
        })