from django.db import models

# Create your models here.
from django.db import models



class Worker(models.Model):

    WORK_CHOICES = (
        ('designer', 'Designer'),
        ('tailor', 'Tailor'),
        ('embroidery', 'Embroidery'),
        ('packing', 'Packing'),
    )

    name = models.CharField(max_length=100)

    personal_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    phone = models.CharField(max_length=15)

    address = models.CharField(max_length=100)

    work_type = models.CharField(
        max_length=100,
        choices=WORK_CHOICES,
        default='tailor'
    )

    salary = models.CharField(max_length=100)


class Saree(models.Model):
    saree_name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    design = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)



class customer(models.Model):

    PRIORITY_CHOICES = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    saree = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    quantity = models.IntegerField()

    delivery_date = models.DateField()

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    def __str__(self):
        return self.name
    
class Assigned_Work(models.Model):

     STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ) 

     worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name='assigned_work'
    )

     preorder = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE
    )

     worker_name = models.CharField(max_length=100)

     def save(self, *args, **kwargs):
        self.worker_name = self.worker.name
        super().save(*args, **kwargs)

     def __str__(self):
        return self.worker_name
     
     work_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )