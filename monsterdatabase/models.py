from django.db import models


class Monster(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        "auth.user", related_name="entries", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} - {self.author.username}"
