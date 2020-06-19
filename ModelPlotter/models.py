from django.db import models

# Create your models here.

class Types(models.Model):
    type_text = models.CharField(max_length = 2)

    def __str__(self):
        return self.type_text

class Stages(models.Model):
    type = models.ForeignKey(Types, on_delete=models.PROTECT)
    stage_text = models.CharField(max_length=3)

    def __str__(self):
        return self.stage_text

class DOFs(models.Model):
    stage = models.ForeignKey(Stages, on_delete=models.PROTECT)
    dof_text = models.CharField(max_length=3)

    def __str__(self):
        return self.dof_text


class Optics(models.Model):
    type = models.ForeignKey(Types, on_delete=models.PROTECT)
    optic_text = models.CharField(max_length=4)

    def __str__(self):
        return self.optic_text

class XMLfile(models.Model):
    t_file = models.FileField()
    def __str__(self):
        return self.filename.url