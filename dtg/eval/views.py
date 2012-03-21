from django.shortcuts import render_to_response
from django.http import HttpResponse
from dtg.eval.models import Url
from dtg.eval.models import Metrics
from django.db.models import F
from decimal import *
import sys
import random
import math

def evaluate(request):
	if request.POST:
		doEvaluate(request.POST)
		"""
		for k, v in request.POST.iteritems():
			print k + ':' + v
		
		idx =int(request.POST['id'])
		print 'POST id:%d'	% idx
		u = Url.objects.get(id=int(request.POST['id']))
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
		"""
		return render_to_response('evaluate.html', {})

	else:
		print 'NO POST'
		random.seed()
		idx = random.randint(1, 1239)

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
		for tag in u.dtg_tags.split():
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
		response_dict['dtg_tags'] = u.dtg_tags.split()
		response_dict['all_tags'] = all_tags

		return render_to_response('evaluate.html', response_dict)

def doEvaluate(post):
	for k, v in post.iteritems():
		print k + ':' + v
		
	idx =int(post['id'])
	print 'POST id:%d'	% idx
	u = Url.objects.get(id=int(post['id']))
	if post.get('pop', False):
		Url.objects.filter(id=idx).update(pop_votes=F('pop_votes') + 1)
		print 'pop++'
	if post.get('irf', False):
		Url.objects.filter(id=idx).update(irf_votes=F('irf_votes') + 1)
		print 'irf++'
	if post.get('lda', False):
		Url.objects.filter(id=idx).update(lda_votes=F('lda_votes') + 1)
		print 'lda++'
	if post.get('dlda', False):
		Url.objects.filter(id=idx).update(dlda_votes=F('dlda_votes') + 1)
		print 'dlda++'
	if post.get('dtg', False):
		Url.objects.filter(id=idx).update(dtg_votes=F('dtg_votes') + 1)
		print 'dtg++'

	pop_tl = u.pop_tags.split()
	irf_tl = u.irf_tags.split()
	lda_tl = u.lda_tags.split()
	dlda_tl = u.dlda_tags.split()
	dtg_tl = u.dtg_tags.split()
	
	u = Url.objects.get(id=idx)
	all_tags = set()
	for tag in pop_tl:
		all_tags.add(tag)
	for tag in irf_tl:
		all_tags.add(tag)
	for tag in lda_tl:
		all_tags.add(tag)
	for tag in dlda_tl:
		all_tags.add(tag)
	for tag in dtg_tl:
		all_tags.add(tag)
	all_tags = list(all_tags)

	topic2tags = dict()
	groups = ''
	for tag in all_tags:
		topic = post[tag]
		groups += tag + ':' + topic + ' '
		if topic not in topic2tags:
			topic2tags[topic] = list()
		topic2tags[topic].append(tag)
	groups = groups.strip()

	# print topic2tags
	# print groups

	pop_map = str(computeMAP(topic2tags, pop_tl))
	irf_map = str(computeMAP(topic2tags, irf_tl))
	lda_map = str(computeMAP(topic2tags, lda_tl))
	dlda_map = str(computeMAP(topic2tags, dlda_tl))
	dtg_map = str(computeMAP(topic2tags, dtg_tl))

	# print pop_map
	# print irf_map
	# print lda_map
	# print dlda_map
	# print dtg_map

	try:
		m = Metrics(url=u, tag_groups=groups, pop_map=Decimal(pop_map), irf_map=Decimal(irf_map),\
			lda_map=Decimal(lda_map), dlda_map=Decimal(dlda_map),\
			dtg_map=Decimal(dtg_map))
		m.save()
		print 'Metrics saved'
	except Exception as e:
		print 'Unexpected Error: ', e


def computeMAP(topic2tags, taglist):
	MAP = list()
	for topic in topic2tags.iterkeys():
		rel_cnt = 0.0
		tag_cnt = 0.0
		precisions = list()
		for tag in taglist:
			tag_cnt += 1.0
			if tag in topic2tags[topic]:
				rel_cnt += 1.0
				precisions.append(rel_cnt / tag_cnt)
		if rel_cnt != 0:
			MAP.append(math.fsum(precisions) / rel_cnt)
	return math.fsum(MAP) / len(MAP)
				

