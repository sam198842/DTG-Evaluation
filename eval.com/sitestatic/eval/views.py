from django.shortcuts import render_to_response
from django.http import HttpResponse
from dtg.eval.models import Url
from django.db.models import F
import random

def evaluate(request):
	if request.POST:
		idx =int(request.POST.get('id'))
		print 'POST id:%d'	% idx
		u = Url.objects.get(id=int(request.POST.get('id')))
		if request.POST.get('pop', False):
			Url.objects.filter(id=idx).update(pop_votes=F('pop_votes') + 1)
			print 'pop'
		if request.POST.get('irf', False):
			Url.objects.filter(id=idx).update(irf_votes=F('irf_votes') + 1)
			print 'irf'
		if request.POST.get('lda', False):
			Url.objects.filter(id=idx).update(lda_votes=F('lda_votes') + 1)
			print 'lda'
		if request.POST.get('dlda', False):
			Url.objects.filter(id=idx).update(dlda_votes=F('dlda_votes') + 1)
			print 'dlda'

	else:
		print 'NO POST'

	random.seed()
	idx = random.randint(1, 2400)

	u = Url.objects.get(id=idx)
	all_tags = set()
	for tag in u.pop_tags.split():
		all_tags.add(tag)
	for tag in u.irf_tags.split():
		all_tags.add(tag)
	for tag in u.lda_tags.split():
		all_tags.add(tag)
	for tag in u.dlda_tags.split():
		all_tags.add(tag)
	all_tags = list(all_tags)

	response_dict = dict()
	response_dict['id'] = idx
	response_dict['url'] = u.url
	response_dict['uuu'] = u
	response_dict['ori_tags'] = u.ori_tags
	response_dict['pop_tags'] = u.pop_tags.split()
	response_dict['irf_tags'] = u.irf_tags.split()
	response_dict['lda_tags'] = u.lda_tags.split()
	response_dict['dlda_tags'] = u.dlda_tags.split()
	response_dict['all_tags'] = all_tags

	return render_to_response('evaluate.html', response_dict)

