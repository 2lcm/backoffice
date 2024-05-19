import json
from django.conf import settings
import tqdm
from pathlib import Path
from django.core.management import BaseCommand

from data_core.models import Product


class Command(BaseCommand):
    help = "Load data from file system"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_dir_path", nargs="?", default=settings.DEFAULT_JSON_DIR_PATH
        )

    def handle(self, *args, **options):
        json_dir_path = Path(options["json_dir_path"])

        fnames = list(json_dir_path.glob("*.json"))

        for fname in tqdm.tqdm(fnames):
            pid = fname.stem
            with open(fname, "rt") as f:
                json_val = json.load(f)
            name = json_val["name"]
            product, _ = Product.objects.get_or_create(pid=pid, name=name)
            for tag in json_val["tag"]:
                product.tags.add(tag)
            attr_dict = json_val["attribute"]
            for attr_key in attr_dict:
                attr_val = attr_dict[attr_key]
                product.tags.add(f"{attr_key} : {attr_val}")
