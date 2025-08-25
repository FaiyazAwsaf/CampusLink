from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Storefront(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default = "IUTian's Waffle")
    image = models.URLField(default='https://images.pexels.com/photos/789327/pexels-photo-789327.jpeg', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Storefront'
        verbose_name_plural = 'Storefronts'
        ordering = ['store_id']


class Product(models.Model):

    product_id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey(Storefront, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.URLField(default='https://images.pexels.com/photos/789327/pexels-photo-789327.jpeg', blank=True, null=True)
    category = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    
    search_vector = SearchVectorField(null=True, blank=True)
    popularity_score = models.FloatField(default=0.0)

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return round(sum(rating.rating for rating in ratings) / len(ratings), 1)
        return 0.0

    def get_rating_count(self):
        return self.ratings.count()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['category']),
            models.Index(fields=['price']),
            models.Index(fields=['availability']),
            models.Index(fields=['popularity_score']),
        ]


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    review = models.TextField(blank=True, null=True, help_text="Optional review text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating} stars"
