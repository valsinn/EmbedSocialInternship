import json
from django import forms

MIN_RATINGS = [(i, str(i)) for i in range(1, 6)]
RATING_CHOICES = [('highest', 'Highest First'), ('lowest', 'Lowest First')]
DATE_CHOICES = [('newest', 'Newest First'), ('oldest', 'Oldest First')]

class ReviewFilterForm(forms.Form):
    text_priority = forms.ChoiceField(
        label='Prioritize by text',
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
        required=False
    )
    minimum_rating = forms.ChoiceField(
        label='Minimum rating',
        choices=MIN_RATINGS,
        widget=forms.Select
    )
    rating_order = forms.ChoiceField(
        label='Rating',
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )
    date_order = forms.ChoiceField(
        label='Date',
        choices=DATE_CHOICES,
        widget=forms.RadioSelect
    )

    def filter_reviews(self):
        reviews = json.load(open('review_filter_app/reviews.json'))
        text_priority = self.cleaned_data['text_priority']
        minimum_rating = int(self.cleaned_data['minimum_rating'])
        rating_order = self.cleaned_data['rating_order']
        date_order = self.cleaned_data['date_order']
        filtered_reviews = []

        if text_priority == 'yes':
            # Prioritize reviews with text
            text_reviews = [r for r in reviews if r['reviewText']]
            text_reviews.sort(key=lambda r: r['reviewText'])
            filtered_reviews += text_reviews
            reviews = [r for r in reviews if not r['reviewText']]

        reviews = [r for r in reviews if r['rating'] >= minimum_rating]
        if rating_order == 'highest':
            reviews.sort(key=lambda r: (-r['rating'], r['reviewCreatedOnDate']))
        else:
            reviews.sort(key=lambda r: (r['rating'], r['reviewCreatedOnDate']))
        if date_order == 'newest':
            reviews.sort(key=lambda r: r['reviewCreatedOnDate'], reverse=True)

        filtered_reviews += reviews
        return filtered_reviews
