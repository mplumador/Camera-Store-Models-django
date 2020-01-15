from django.db import models

# Create your models here.
class Stores(models.Model):
    #This is not needed, as django should automatically create an ID field as the primary key
    #However making the ID field have a recognizeable name could improve readability
    location_id = models.IntegerField(primary_key=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Inventory(models.Model):
    manufacturer = models.CharField(max_length = 25)
    model_num = models.CharField(max_length=20)
    quantity = models.IntegerField()
    store = models.ForeignKey(Stores, on_delete=models.CASCADE)
    price_per_item = models.DecimalField(max_digits=None,decimal_places=2)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['manufacturer','model_num','store'],name = 'unique item')]   

class Address(models.Model):
    street_address = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

class Transactions(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    model_num = models.CharField(max_length=20)
    store = models.ForeignKey(Stores, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=None,decimal_places=2)
    requires_shipping = models.BooleanField()
    shipping_Address = models.ForeignKey(Address,on_delete=models.CASCADE, blank=True)
    date_time_purchased = models.DateTimeField()
    class Meta:
        constraints = [models.UniqueConstraint(fields=['transaction_id','model_num'],name = 'unique transaction')]

class salesTax(models.Model):
    tax = models.DecimalField(max_digits=5,decimal_places=5)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class State(models.Model):
    abbrev = models.CharField(max_length=2)
    full_name = models.CharField(max_length=50)
    
#Stores may only have one address (foreign key)
#Inventory should have a primary key based on the uniqueness of three criteria:
    #Manufacturer, model_num, and Store location.
    #A specific item can have differing quantities and prices based on Store location
    #Items may have the same model number but not the same manufacturer
    #Manufacturers may have more than one model_number

#An address needs to have a street address, a postal code, a city, and a country.
    #Not all countries have states, therefore that option is not required
    #I do not know how the foreign_key and blank option work together
    #It could be that a default value should be set and then needs to be checked elsewhere.

#Transactions require a unique transaction ID and model_number combo. This allows us to tie transaction ids to multiple items
    #Transactions also require a store, quantity, cost,whether shipping is required or not, and a date/time purchased.
    #A shipping address is left optional, but is also a foreign key of the list of addresses. It is optional for the case shipping is not required

#SalesTax requires a decimal and a State
#State requires a two letter Abbreviation and a full_name

#We may want to collect "User" information as well. Perhaps link addresses to names of people as well as their transaction ids. This would require a model for
    #users that could also contain email information, something along the lines of a saved-account set-up.
