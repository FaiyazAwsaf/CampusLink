from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Owner'
        verbose_name_plural = 'Owners'
        ordering = ['name']

class Storefront(models.Model):
    store_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='stores', blank=True, null=True)
    name = models.CharField(max_length=100, default = "IUTian's Waffle", blank=True, null=True)
    image = models.URLField(default='https://images.pexels.com/photos/789327/pexels-photo-789327.jpeg', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    return_policy = models.TextField(blank=True, null=True)
    shipping_info = models.TextField(blank=True, null=True)
    store_hours = models.CharField(max_length=200, blank=True, null=True)
    total_sales = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def get_average_rating(self):
        products = self.product_set.all()
        if not products:
            return 0.0
        
        total_ratings = 0
        total_count = 0
        
        for product in products:
            ratings = product.ratings.all()
            if ratings:
                total_ratings += sum(rating.rating for rating in ratings)
                total_count += len(ratings)
        
        return round(total_ratings / total_count, 1) if total_count > 0 else 0.0

    def get_total_products(self):
        return self.product_set.count()

    def get_total_reviews(self):
        return sum(product.get_rating_count() for product in self.product_set.all())

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
