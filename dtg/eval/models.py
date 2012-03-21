from django.db import models

class Url(models.Model):
	url = models.URLField(max_length=300)
	ori_tags = models.TextField()
	pop_tags = models.CharField(max_length=200)
	irf_tags = models.CharField(max_length=200)
	lda_tags = models.CharField(max_length=200)
	dlda_tags = models.CharField(max_length=200)
	dtg_tags = models.CharField(max_length=200)
	pop_votes = models.PositiveIntegerField(default=0)
	irf_votes = models.PositiveIntegerField(default=0)
	lda_votes = models.PositiveIntegerField(default=0)
	dlda_votes = models.PositiveIntegerField(default=0)
	dtg_votes = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return u'%d %s %d %d %d %d %d' % (self.id, self.url, self.pop_votes,\
			self.irf_votes, self.lda_votes, self.dlda_votes, self.dtg_votes)
	

class Metrics(models.Model):
	url = models.ForeignKey(Url)
	tag_groups = models.TextField()
	pop_map = models.DecimalField(max_digits=12, decimal_places=10)
	irf_map = models.DecimalField(max_digits=12, decimal_places=10)
	lda_map = models.DecimalField(max_digits=12, decimal_places=10)
	dlda_map = models.DecimalField(max_digits=12, decimal_places=10)
	dtg_map = models.DecimalField(max_digits=12, decimal_places=10)
	
	def __unicode__(self):
		return u'%d %.4f %.4f %.4f %.4f %.4f' % (self.url.id, self.pop_map,\
			self.irf_map, self.lda_map, self.dlda_map, self.dtg_map)

