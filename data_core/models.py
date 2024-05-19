from django.db import models

from django.urls import reverse
from taggit.managers import TaggableManager


class BaseModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Product(BaseModel):
    pid = models.IntegerField(unique=True)
    name = models.CharField(max_length=60)
    tags = TaggableManager()

    class Meta:
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("data_core:product_detail", kwargs={"pk": self.pk})


class ProductImage(BaseModel):
    pid = models.ForeignKey("Product", to_field="pid", on_delete=models.CASCADE)
    image_id = models.IntegerField(null=True)
    height = models.IntegerField()
    width = models.IntegerField()
    valid = models.BooleanField(default=True)   

    class Meta:
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("data_core:image_detail", kwargs={"pk": self.pk})

    @property
    def path(self):
        return f"{self.pid.pid}/{self.image_id}.jpg"
    
    
        