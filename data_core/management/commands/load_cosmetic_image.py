from PIL import Image
from django.conf import settings
import tqdm
from pathlib import Path
from django.core.management import BaseCommand

from data_core.models import Product, ProductImage


class Command(BaseCommand):
    help = "Load image from file system"

    def add_arguments(self, parser):
        parser.add_argument(
            "image_root_dir_path", nargs="?", default=settings.DEFAULT_IMAGE_ROOT_DIR_PATH
        )

    def handle(self, *args, **options):
        image_root_dir_path = Path(options["image_root_dir_path"])

        products = Product.objects.all().only('pid')

        product_image_list = []

        for product in tqdm.tqdm(products):
            pid = product.pid
            image_dir = image_root_dir_path / str(pid)
            images = image_dir.glob("*")
            for image_fname in images:
                image = Image.open(image_fname)
                h, w = image.size[:2]
                imid = image_fname.stem
                product_image = ProductImage(pid=product, image_id = imid, height=h, width=w)
                product_image_list.append(product_image)

        ProductImage.objects.bulk_create(product_image_list, batch_size=999)

            
