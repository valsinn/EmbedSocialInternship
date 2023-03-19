from django.shortcuts import render
from .forms import ReviewFilterForm


def review_filter(request):
    form = ReviewFilterForm(request.GET or None)
    if form.is_valid():
        filtered_reviews = form.filter_reviews()
    else:
        filtered_reviews = []
    return render(request, 'review_filter.html', {'form': form, 'reviews': filtered_reviews})
