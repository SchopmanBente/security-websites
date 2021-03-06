import base64
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class BadToken(models.Model):
    """
    The default authorization token model.
    """

    def __init__(self, username):
        super().__init__()
        self.generate_key(username)
        self.save()

    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(BadToken, self).save(*args, **kwargs)

    def generate_key(self, username):
        user = User.objects.filter(username=username).first()
        standard = "userid="
        sentence = f"{standard}{str(user.pk)}"
        sutf8 = sentence.encode("utf-8")
        self.key = base64.b64encode(sutf8)
        self.user_id = user

    def __str__(self):
        return self.key
