from django.db import models

# Create your models here.
class Product(models.Model):
  product_brand = models.CharField(max_length = 50, default='Unknown Brand')
  name = models.CharField(max_length=100)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  image = models.ImageField(upload_to='products/')

  def __str__(self):
    return self.name
  
class Auth(models.Model):
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=128)

  def __str__(self):
    return self.email
  
class CartItem(models.Model):
  user = models.ForeignKey(Auth, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)

  @property
  def sub_total(self):
    return self.product.price * self.quantity
  
  def __str__(self):
    return f"{self.quantity} of {self.product.name} for {self.user.email}"