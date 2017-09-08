#! -*- coding: UTF-8 -*-
from django.views import generic
from django.core import paginator
from django.contrib.admin.utils import NestedObjects

from . import conf as base_conf

# Create your views here.


class BaseCreateView(generic.CreateView):
    """
    View based on CreateView from django.views.generic.
    Use a custom template for a form display
    """
    template_name = "base/%s/create.html" % base_conf.style

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data(**kwargs)

        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()

        return context


class BaseUpdateView(generic.UpdateView):
    """
    View based on Update from django.views.generic.
    Use a custom template for a form display
    """
    template_name = "base/%s/update.html" % base_conf.style
    context_object_name = "element"

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data(**kwargs)

        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()

        return context


class BaseListView(generic.ListView):
    """
    View based on ListView from django.views.generic.
    Use a custom template for iterate a list
    """
    template_name = "base/%s/list.html" % base_conf.style
    context_object_name = "list"

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)

        if len(self.get_queryset()) > 0:
            context['model_name'] = self.get_queryset()[0]._meta.verbose_name.title()
            context['model_name_plural'] = self.get_queryset()[0]._meta.verbose_name_plural.title()

        return context


class BasePaginationListView(generic.ListView):
    """
    View based on ListView from django.views.generic.
    Use a custom template for iterate a list.
    Uses django.core.paginator to slice the result in pages
    """
    template_name = "base/%s/pagination_list.html" % base_conf.style
    context_object_name = "list"

    def get_context_data(self, **kwargs):
        context = super(BasePaginationListView, self).get_context_data(**kwargs)

        queryset = self.get_queryset()

        recordings_by_page = base_conf.ITEMS_BY_PAGE
        pager = paginator.Paginator(queryset, recordings_by_page)
        page = self.request.GET.get('page', 1)
        try:
            recordings = pager.page(page)

            start_index = max(1, recordings.number-3)
            end_index = min(recordings.number+3, (len(queryset)/recordings_by_page)+1)
            context['range'] = range(start_index, end_index+1)
            context[self.context_object_name] = recordings
        except paginator.PageNotAnInteger:
            context[self.context_object_name] = pager.page(1)
        except paginator.EmptyPage:
            context[self.context_object_name] = pager.page(pager.num_pages)

        if len(self.get_queryset()) > 0:
            context['model_name'] = self.get_queryset()[0]._meta.verbose_name.title()
            context['model_name_plural'] = self.get_queryset()[0]._meta.verbose_name_plural.title()

        return context


class BaseGridView(BaseListView):
    """
    View based on ListView from django.views.generic.
    Use a custom template for iterate a list in a grid
    """
    template_name = "base/%s/grid.html" % base_conf.style


class BasePaginationGridView(BasePaginationListView):
    """
    View based on ListView from django.views.generic.
    Use a custom template for iterate a list in a grid
    Uses django.core.paginator to slice the result in pages
    """
    template_name = "base/%s/pagination_grid.html" % base_conf.style


class BaseDetailView(generic.DetailView):
    """
    View based on DetailView from django.views.generic.
    Shows all attributes and values of an object
    """
    template_name = "base/%s/detail.html" % base_conf.style
    context_object_name = "element"

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)

        context[self.context_object_name].get_fields = [
            (field.name, field.value_to_string(self.get_object())) for field in self.model._meta.fields
        ]

        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()

        return context


class BaseDeleteView(generic.DeleteView):
    """
    View based on Delete view from django.views.generic
    Show a list with all elements to be delete and delete it on post
    """
    template_name = "base/%s/delete.html" % base_conf.style
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super(BaseDeleteView, self).get_context_data(**kwargs)

        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()

        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()

        return context
