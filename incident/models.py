from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# from ckeditor.fields import RichTextField, RichTextUploadingField
from ckeditor_uploader.fields import RichTextUploadingField
import nexmo


# Create your models here.
class TimeStampedModel(models.Model):
    """TimeStampedModel.
    An abstract base class model that provides self-managed "created" and
    "updated" fields.
    """

    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        get_latest_by = 'modified_on'
        ordering = ('-modified_on', '-created_on',)
        abstract = True


class Category(TimeStampedModel):
    """IncidentCategory model."""

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name =_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")

class Sector(TimeStampedModel):
    """Sector model."""

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name =_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")


class AffectedUnit(TimeStampedModel):
    """AffectedUnit model."""

    unit = models.CharField(max_length=30, null=True, blank=True, verbose_name =_("Unit"))
    sector = models.ForeignKey(Sector, related_name='unitsector', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("sector"))

    def __str__(self):
        return self.unit

    class Meta:
        verbose_name = _("AffectedUnit")
        verbose_name_plural = _("AffectedUnits")


class Incident(TimeStampedModel):
    """Incident model."""

    INCIDENT_STATUSES = (
        ('open', 'open'),
        ('pending', 'pending'),
        ('in_progress', 'in_progress'),
        ('closed', 'closed'),
    )

    subject = models.CharField(max_length=255, verbose_name=_("subject"))
    category = models.ForeignKey(Category, related_name='incidentcategory', on_delete=models.CASCADE, verbose_name=_("category"))
    timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_("timestamp"))
    sector = models.ForeignKey(Sector, related_name='incidentsector', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("sector"))
    affectedunit = models.ForeignKey(AffectedUnit, related_name='incidentunit', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("affectedunit"))
    description = models.TextField(null=True, blank=True, verbose_name=_("description"))
    status = models.CharField(max_length=100, choices=INCIDENT_STATUSES, null=True, blank=True,verbose_name=_("status"))
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incident_user', null=True, blank=True, verbose_name=_("assigned_user"))
    attachment = models.FileField(null=True, blank=True, verbose_name=_("attachment")) 

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        # if "ministries" in self.sector.name:
            # client = nexmo.Client(key='d7f80c7c', secret='VufAqNo9kXedsT3F')
            # to = '0096897135701'
            # from_txt = 'نظام مسبار'
            # subject = "Your incident with sector ministries has been created."
            # time = timestamp
            # affectedunit = affectedunit
            # category = category
            # message = "subject: {subject}\nTime: {time}\naffectedunit: {affectedunit}\nCategory: {category}"
            # client.send_message({'from': from_txt, 'to': to,
            # 'text': message,
            # })
        client = nexmo.Client(key='d7f80c7c', secret='VufAqNo9kXedsT3F')
        to = '+96897135701'
        from_txt = 'Misbar'
        subject = self.subject
        time = self.timestamp
        affectedunit = self.affectedunit if self.affectedunit else 0
        category = self.category.name
        status = self.status
        message = "{subject}\nTime: {time}\nAffected Unit: {affectedunit}\nCategory: {category}\nStatus:{status}\n".format(subject=subject, time=time, affectedunit=affectedunit, category=category, status=status)
        client.send_message({'from': from_txt, 'to': to,
        'text': message,
        })


        super(Incident, self).save(*args, **kwargs)


class Related_ip(TimeStampedModel):
    """Related_ip model."""

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("name"))
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("incident"))

    def __str__(self):
        return self.name


class Related_domain(TimeStampedModel):
    """Related_domain model."""

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("name"))
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("incident"))

    def __str__(self):
        return self.name


class Task(TimeStampedModel):
    """Task model."""

    TASK_STATUSES = (
        ('open', 'open'),
        ('in_progress', 'in_progress'),
        ('complete', 'complete'),
    )

    task_subject  = models.CharField(max_length=255, verbose_name=_("task_subject"))
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_user', null=True, blank=True, verbose_name=_("assigned_user"))
    due_date = models.DateField(null=True, blank=True, verbose_name=_("due_date"))
    attachment = models.FileField(null=True, blank=True, verbose_name=_("attachment"))
    status = models.CharField(max_length=100, choices=TASK_STATUSES, null=True, blank=True, verbose_name=_("status"))
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("incident"))


    def __str__(self):
        return self.task_subject


class Comment(TimeStampedModel):
    """Comments model."""

    comment = models.TextField(null=True, blank=True, verbose_name=_("comment"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user', null=True, blank=True, verbose_name=_("user"))
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='incident_comment', null=True, blank=True, verbose_name=_("incident"))

    def __str__(self):
        return self.comment


class Blog(TimeStampedModel):
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("title"))
    discription = RichTextUploadingField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_user', null=True, blank=True, verbose_name=_("user"))
    is_enable = models.NullBooleanField(blank=True, null=True, default=True, verbose_name=_("is_enable"))

    def __str__(self):
        return self.title
