from django.db.models import Q, F, Case, When, IntegerField
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class AdvancedSearchView(APIView):
    
    def get(self, request):
        query = request.GET.get('query', '').strip()
        
        if not query:
            return Response([])
        
        try:
            search_results = self.basic_search(query)
            filtered_results = self.apply_filters(search_results, request)
            serializer = ProductSerializer(filtered_results[:50], many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def basic_search(self, query):
        return Product.objects.select_related('store_id').filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(store_id__name__icontains=query)
        ).annotate(
            name_match=Case(
                When(name__icontains=query, then=4),
                default=0,
                output_field=IntegerField()
            ),
            store_match=Case(
                When(store_id__name__icontains=query, then=3),
                default=0,
                output_field=IntegerField()
            ),
            category_match=Case(
                When(category__icontains=query, then=2),
                default=0,
                output_field=IntegerField()
            ),
            desc_match=Case(
                When(description__icontains=query, then=1),
                default=0,
                output_field=IntegerField()
            ),
            availability_score=Case(
                When(availability=True, then=1),
                default=0,
                output_field=IntegerField()
            ),
            total_score=F('name_match') + F('store_match') + F('category_match') + F('desc_match') + F('availability_score') + F('views') * 0.001
        ).order_by('-total_score', '-created_at')
    
    def apply_filters(self, queryset, request):
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass
        
        availability = request.GET.get('availability')
        if availability:
            queryset = queryset.filter(availability=availability.lower() == 'true')
        
        return queryset

class AutocompleteView(APIView):
    
    def get(self, request):
        query = request.GET.get('query', '').strip()
        
        if len(query) < 2:
            return Response([])
        
        product_suggestions = Product.objects.filter(
            name__istartswith=query
        ).values_list('name', flat=True).distinct()[:5]

        from .models import Storefront
        storefront_suggestions = Storefront.objects.filter(
            name__istartswith=query
        ).values_list('name', flat=True).distinct()[:5]

        suggestions = list(product_suggestions) + list(storefront_suggestions)

        if len(suggestions) < 8:
            additional_products = Product.objects.filter(
                name__icontains=query
            ).exclude(
                name__istartswith=query
            ).values_list('name', flat=True).distinct()[:3]
            
            suggestions.extend(list(additional_products))
        
        return Response(suggestions[:10])

class SearchSuggestionsView(APIView):
    
    def get(self, request):
        query = request.GET.get('query', '').strip()
        
        if not query:
            return Response([])
        
        suggestions = self.get_spell_corrections(query)
        
        return Response(suggestions)
    
    def get_spell_corrections(self, query):
        all_names = Product.objects.values_list('name', flat=True).distinct()
        
        suggestions = []
        for name in all_names:
            distance = self.levenshtein_distance(query.lower(), name.lower())
            if distance <= 2 and distance > 0:
                suggestions.append({
                    'original': query,
                    'suggestion': name,
                    'distance': distance
                })
        
        suggestions.sort(key=lambda x: x['distance'])
        return [s['suggestion'] for s in suggestions[:5]]
    
    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
