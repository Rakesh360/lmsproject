from django.db import models
from base_rest.models import BaseModel
from courses.models import Course

class Coupoun(BaseModel):
    coupon_code = models.CharField(max_length=100 , unique=True)
    coupon_type = models.ManyToManyField(choices=(
        ('One time' , 'One time'),
        ('Validity' , 'Validity'),
        ('Specific Course','Specific Course')))

    courses = models.ManyToManyField(Course)
    start_date = models.DateField(null=True , blank=True)
    expiry_date = models.DateField(null=True , blank=True)

    coupon_discount_type = models.CharField(max_length=100 , choices=(('Percentage' ,'Percentage') , ('Amount' , 'Amount')))
    discount =  models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.coupon_code

    class Meta:
        db_table = "coupons"
        verbose_name_plural = "Coupon "
        ordering = ['-created_at']


    
    
