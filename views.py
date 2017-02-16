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
    template_name = "base/create.html"

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
    template_name = "base/update.html"

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
    template_name = "base/list.html"
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
    template_name = "base/pagination_list.html"
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
            print(start_index, end_index, len(queryset))
            context['range'] = range(start_index, end_index+1)
            context[self.context_object_name] = recordings
        except paginator.PageNotAnInteger:
            context[self.context_object_name] = pager.page(1)
        except paginator.EmptyPage:
            context[self.context_object_name] = pager.page(pager.num_pages)

        if len(self.get_queryset()) > 0:
            context['model_name'] = self.get_queryset()[0]._meta.verbose_name.title()
            context['model_name_plural'] = self.get_queryset()[0]._meta.verbose_name_plural.title()

        print context

        return context


class BaseGridView(BaseListView):
    """
    View based on ListView from django.views.generic.
    Use a custom template for iterate a list in a grid
    """
    template_name = "base/grid.html"


class BasePaginationGridView(BasePaginationListView):
    """
    View based on ListView from django.views.generic.
    Use a custom template for iterate a list in a grid
    Uses django.core.paginator to slice the result in pages
    """
    template_name = "base/pagination_grid.html"


class BaseDetailView(generic.DetailView):
    """
    View based on DetailView from django.views.generic.
    Shows all attributes and values of an object
    """
    template_name = "base/detail.html"
    context_object_name = "element"

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)

        if self.model:
            context['model_name'] = self.model._meta.verbose_name.title()
            context['model_name_plural'] = self.model._meta.verbose_name_plural.title()

        return context


class BaseDeleteView(generic.DeleteView):
    """
    View based on Delete view from django.views.generic
    Show a list with all elements to be delete and delete it on post
    """
    template_name = "base/delete.html"
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