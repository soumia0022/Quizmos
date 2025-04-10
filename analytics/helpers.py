def apply_search_and_sort(queryset, search_query=None, sort_by=None, sort_options=None, default_sort='id'):
    """
    Apply search and sorting logic to a queryset.
    """
    if search_query:
        queryset = queryset.filter(question_text__icontains=search_query)

    if sort_by and sort_options:
        sort_expression = sort_options.get(sort_by, default_sort)
        queryset = queryset.order_by(sort_expression)

    return queryset
