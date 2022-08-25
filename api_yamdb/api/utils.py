class CurrenTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        view = serializer_field.context['view']
        self.title = view.kwargs['title_id']
        return self.title

    def __repr__(self):
        return '%s()' % self.__class__.__name__
