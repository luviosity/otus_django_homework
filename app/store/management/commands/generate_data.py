import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import IntegrityError, OperationalError
from django.db.models import Max

from store.models import Category, Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--products", type=int, help="Количество продуктов для генерации")
        parser.add_argument("--categories", type=int, help="Количество категорий для генерации")

    def handle(self, *args, **options):
        categories_count = options["categories"]
        products_count = options["products"]

        if (categories_count or 0) > 10000 or (products_count or 0) > 10000:
            self.stdout.write(self.style.WARNING("Максимальное количество строк для добавления - 10000"))
            return

        if categories_count:
            self._create_categories(categories_count)

        if products_count:
            self._create_products(products_count)

        if not categories_count and not products_count:
            self.stdout.write(self.style.WARNING("Укажите --products и/или --categories"))

    def _create_categories(self, count):
        offset = Category.objects.aggregate(max_id=Max("id"))["max_id"] or 0
        objects = [
            Category(name=f"Категория {offset + i + 1}", description=f"Описание категории {offset + i + 1}")
            for i in range(count)
        ]
        self._bulk_create("категорий", objects)

    def _create_products(self, count):
        category_ids = list(Category.objects.values_list("id", flat=True))
        if not category_ids:
            self.stdout.write(self.style.ERROR("Нет категорий. Сначала создайте категории."))
            return

        offset = Product.objects.aggregate(max_id=Max("id"))["max_id"] or 0
        objects = [
            Product(
                name=f"Продукт {offset + i + 1}",
                description=f"Описание продукта {offset + i + 1}",
                price=Decimal(random.uniform(100, 1000)).quantize(Decimal("0.01")),
                category_id=random.choice(category_ids),
            )
            for i in range(count)
        ]
        self._bulk_create("продуктов", objects)

    def _bulk_create(self, label, objects):
        try:
            result = type(objects[0]).objects.bulk_create(objects, batch_size=1000)
            self.stdout.write(self.style.SUCCESS(f"Успешно добавлено {label}: {len(result)}"))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка целостности при добавлении {label}: {e}"))
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка БД при добавлении {label}: {e}"))