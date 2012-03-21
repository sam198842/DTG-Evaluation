from django.db import models

class Url(models.Model):
	url = models.URLField(max_length=300)
	ori_tags = models.TextField()
	pop_tags = models.CharField(max_length=200)
	irf_tags = models.CharField(max_length=200)
	lda_tags = models.CharField(max_length=200)
	dlda_tags = models.CharField(max_length=200)
	pop_votes = models.PositiveIntegerField(default=0)
	irf_votes = models.PositiveIntegerField(default=0)
	lda_votes = models.PositiveIntegerField(default=0)
	dlda_votes = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return u'%d %s %d %d %d %d' % (self.id, self.url, self.pop_votes,\
			self.irf_votes, self.lda_votes, self.dlda_votes)
	
