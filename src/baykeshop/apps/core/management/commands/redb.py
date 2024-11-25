from django.core import management
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "重建数据库"

    def handle(self, *args, **options):
        for app in (settings.BASE_DIR.parent / "src/baykeshop/apps").iterdir():
            if not app.is_dir() and ("__pycache__" in str(app)):
                continue
            if (app / 'migrations').is_dir():
                for m in (app / 'migrations').iterdir():
                    if m.name == "__pycache__" and m.is_dir():
                        for pycache in m.iterdir():
                            pycache.unlink()
                            self.stdout.write(self.style.SUCCESS('删除 "%s"成功' % str(pycache)))
                        m.rmdir()
                        self.stdout.write(self.style.SUCCESS('删除 "%s"成功' % str(m)))
                    if m.is_file() and m.name != "__init__.py":
                        m.unlink()
                        self.stdout.write(self.style.SUCCESS('删除 "%s"成功' % str(m)))

        # management.call_command("makemigrations", verbosity=0, interactive=False)
        # management.call_command("migrate", verbosity=0, interactive=False)
        self.stdout.write(self.style.SUCCESS('数据重建成功！'))