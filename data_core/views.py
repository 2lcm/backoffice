from typing import Any
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from rest_framework import viewsets
from .serializers import ProductSerializer, ProductImageSerializer, TagSerializer
from .models import Product, ProductImage
from taggit.models import Tag


def index(request:HttpRequest) -> HttpResponse:
    return render(request, "data_core/index.html")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ProductImageDetailView(DetailView):
    model = ProductImage
    context_object_name = "image"
    template_name = "data_core/image_detail.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "data_core/product_detail.html"


class TagDetailView(DetailView):
    model = Tag
    context_object_name = "tag"
    template_name = "data_core/tag_detail.html"


class ProductListView(ListView):
    model = Product
    template_name = "data_core/product_list.html"
    paginate_by = 10
    extra_context = {"title" : "Product List"}

    def get_queryset(self):
        qs = super().get_queryset()
        if "keyword" in self.request.GET:
            keyword = self.request.GET["keyword"]
            qs = qs.filter(
                Q(pid__icontains=keyword) |
                Q(name__icontains=keyword) | 
                Q(tags__name__icontains=keyword)
            ).distinct()

        qs = qs.prefetch_related("productimage_set")

        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)
        context['pagelist'] = pagelist
        context["ref_url"] = ""
        if "keyword" in self.request.GET:
            kw = self.request.GET["keyword"]
            # context['keyword'] = kw
            context["ref_url"] += f"&keyword={kw}"
        
        return context