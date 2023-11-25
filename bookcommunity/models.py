from django.db import models
from django.conf import settings

#-------------------------------------IMPORTANT!---------------------------------------------------
# ALWAYS USE 'settings.AUTH_USER_MODEL' INSTEAD OF THE USUAL 'User' WHEN CONNECTING MODELS TO USER!
# i.e. user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#                    OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#                    ManyToManyField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

# NOT THIS -> models.ForeignKey(User,on_delete=models.CASCADE)

# BECAUSE WE ARE USING CUSTOM USER
#--------------------------------------------------------------------------------------------------
# Create your models here.
class Forum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    book = models.CharField(max_length=100)
    subject = models.TextField(unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.subject)
    

class Discussion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    forum = models.ForeignKey(Forum,blank=True,on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
 
    def __str__(self):
        return str(self.forum)
    
