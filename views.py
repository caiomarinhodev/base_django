#! -*- coding: UTF-8 -*-
from django.views import generic
from django.core import paginator

from . import conf as base_conf

# Create your views here.


class BaseCreateView(generic.CreateView):
    """
    View based on CreateView from django.views.generic.
    Use a custom template for a form display
    """
    template_name = "base/create.html"

class BaseUpdateView(generic.UpdateView):
    """
    View based on Update from django.views.generic.
    Use a custom template for a form display
    """
    template_name = "base/update.html"

class BaseListView(generic.ListView):
    """
    View based on ListView from django.views.generic.
    Use a custom template for iterate a list
    """
    template_name = "base/list.html"
    context_object_name = "list"


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

        recordings_by_page = base_conf.ITEMS_BY_PAGE
        pager = paginator.Paginator(context['list'], recordings_by_page)
        page = self.request.GET.get('page', 1)
        try:
            recordings = pager.page(page)

            start_index = max(1, recordings.number-3)
            end_index = min(recordings.number+3, (len(context['list'])/recordings_by_page)+1)
            print(start_index, end_index, len(context['list']))
            context['range'] = range(start_index, end_index+1)
            context['list'] = recordings
        except paginator.PageNotAnInteger:
            context['list'] = pager.page(1)
        except paginator.EmptyPage:
            context['list'] = pager.page(pager.num_pages)

        return context


class BaseGridView(BaseListView):
    """
    View based on ListView from django.views.generic.
    Use a custom template for iterate a list in a grid
    """
    template_name = "base/grid.html"


class BaseDetailView(generic.DetailView):
    """
    View based on DetailView from django.views.generic.
    Shows all attributes and values of an object
    """
    template_name = "base/detail.html"
    context_object_name = "element"
