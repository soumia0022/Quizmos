from django.db import models
import random
import qrcode
from io import BytesIO
from django.core.files import File

class Poll(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    number_code = models.IntegerField(unique=True, blank=True, null=True)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.number_code:
            self.number_code = self.generate_number_code()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.title)
        qr.make(fit=True)


        img = qr.make_image(fill_color="#003366", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)


        filename = f"qr_code_{self.title}.png"
        self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, ** kwargs)

    def generate_number_code(self):
        while True:
            number_code = random.randint(100000, 999999)
            if not Poll.objects.filter(number_code=number_code).exists():
                return number_code
