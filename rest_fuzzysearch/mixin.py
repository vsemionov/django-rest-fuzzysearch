from collections import OrderedDict


class ViewSetMixin(object):

    def decorated_list(self, cls, context, request, *args, **kwargs):
        response = super(cls, self).list(request, *args, **kwargs)

        if isinstance(response.data, dict):
            base_data = response.data
        else:
            base_data = OrderedDict(results=response.data)

        data = context.copy()
        data.update(base_data)

        response.data = data

        return response
