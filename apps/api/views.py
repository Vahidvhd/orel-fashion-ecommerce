from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import DiscountSerializer, ProductDetailSerializer, ProductListSerializer
from apps.cart.services import get_cart_count
from apps.catalog.filters import filter_products
from apps.catalog.models import Discount, Product


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        params = self.request.query_params
        return filter_products(
            Product.objects.prefetch_related("images", "variants"),
            section=params.get("section"),
            category_slug=params.get("category"),
            min_price=params.get("min_price"),
            max_price=params.get("max_price"),
            color_slugs=params.getlist("color"),
            size_slugs=params.getlist("size"),
            on_sale=params.get("sale") == "true",
            sort=params.get("sort", "newest"),
        )


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
    queryset = Product.objects.prefetch_related("images", "variants__color", "variants__size")


class CartCountAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"count": get_cart_count(request)})


class ActiveDiscountsAPIView(generics.ListAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        now = timezone.now()
        return Discount.objects.filter(
            is_active=True,
            starts_at__lte=now,
            ends_at__gte=now,
        ).select_related("product", "variant")[:50]
