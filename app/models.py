from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from django.utils.text import slugify

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['name']
        
    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            
            while Category.objects.filter(slug=slug, parent=self.parent).exist():
                slug = f'{base_slug}-{num}'
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        ancestors = self.get_ancestors(include_self=True)
        return '/' + '/'.join(cat.slug for cat in ancestors)
        