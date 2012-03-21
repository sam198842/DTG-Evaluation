from django.core.management.base import BaseCommand, CommandError
from dtg.eval.models import Url
from itertools import izip

class Command(BaseCommand):
	args = 'eval_file, baseline_file'
	help = 'Loading Database.'

	def handle(self, *args, **options):
		if len(args) != 2:
			raise CommandError('Usage: python manage.py loaddb eval_file baseline_file')

		print "Loading URLs: ('.' means 10 entries)"
		eval_fn, baseline_fn = args
		with open(eval_fn, 'r') as feval:
			with open(baseline_fn, 'r') as fbase:
				cnt = 0
				for leval, lbase in izip(feval, fbase):
					if cnt % 10 == 0:
						print '.',
					cnt += 1
					tokens = leval.split()
					tags = ' '.join(tokens[2:])
					bases = lbase.splitlines()[0].split(',')
					u = Url(url=tokens[1], ori_tags=tags, pop_tags=bases[0],\
									irf_tags=bases[1], lda_tags=bases[2],\
									dlda_tags=bases[3], dtg_tags=bases[4])
					u.save()

		print '\nFinish loading %d URLs into MySQL.' % cnt
	

