from django.contrib import admin
from dtg.eval.models import Url, Metrics

class UrlAdmin(admin.ModelAdmin):
	list_display = ('id', 'pop_tags', 'irf_tags', 'lda_tags', 'dlda_tags',\
									'pop_votes', 'irf_votes', 'lda_votes', 'dlda_votes',\
									'dtg_votes')
	search_fields = ('id',)

class MetricsAdmin(admin.ModelAdmin):
	list_display = ('url', 'pop_map', 'irf_map', 'lda_map', 'dlda_map',\
									'dtg_map')

admin.site.register(Url, UrlAdmin)
admin.site.register(Metrics, MetricsAdmin)

