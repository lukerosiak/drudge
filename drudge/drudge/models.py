from django.db import models

class Story(models.Model):
    #a list of committees who can make independent expenditures, i.e. superpacs
    url = models.TextField()
    hed = models.CharField(max_length=255)
    time = models.DateTimeField()	
    location = models.CharField(max_length=25)
    outlet = models.CharField(max_length=255)
    
	
    def __unicode__(self):
        return self.hed

    def getoutlet(self):
        chunks = self.url.split('://')
        if len(chunks)==1: return 'Drudgereport.com'        
        url = chunks[1].split('/')[0]
        if url.startswith('www.'):
            url = url[4:]
        return url

    def save(self, *args, **kwargs):
        if not self.outlet:
            self.outlet = self.getoutlet()
        super(Story, self).save(*args, **kwargs)
