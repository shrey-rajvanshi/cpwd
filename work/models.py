__author__ = "shrey"
from django.db import models

status_choices= (
    ('1','REQ. FROM CLIENT RECEIVED - UNSANCTIONED WORK'),
    ('2','PE SENT TO CLIENT - UNSANCTIONED WORK'),
    ('3','PE SENT TO CLIENT - UNSANCTIONED WORK'),
    ('4','SANCTIONED BUT NOT YET STARTED'),
    ('4','SANCTIONED AND WORK IS IN PROGRESS'),
    ('6','WORK COMPLETED'),
)

class Work(models.Model):
	name= models.CharField(max_length=1000)
	project_code= models.CharField(max_length=200,default='',blank=True)
	requisition= models.CharField(max_length=200,blank=True)
	pe_det= models.CharField(max_length=20,blank=True)
	pe_letter_no = models.CharField(max_length=200,blank=True)
	pe_date= models.DateField(blank=True)
	pe_amt= models.FloatField(blank=True)
	pe_sent_to= models.CharField(max_length=100,blank=True)
	fe_sent_to_client= models.CharField(max_length=100,blank=True)
	client= models.CharField(max_length=100,blank=True)
	aa_es_detail= models.CharField(max_length=50,blank=True)
	head_acc= models.CharField(max_length=7,blank=True)
	final_amt= models.FloatField(blank=True)
	ts_auth= models.CharField(max_length=50,blank=True)
	no_sub= models.IntegerField(default=0)
	ts_detail= models.CharField(max_length=20,default='',blank=True)
	ts_date= models.DateField(blank=True)
	ts_amt= models.FloatField(blank=True)
	time_allowd= models.IntegerField(blank=True,help_text='in months')
	nit= models.CharField(max_length=20,blank=True)
	nit_date= models.DateField(blank=True)
	nit_amt= models.FloatField(blank=True)
	agency= models.CharField(max_length=200,default = '',blank=True)
	agency_add= models.CharField(max_length=200,default = '',blank=True)
	agmnt_no= models.CharField(max_length=20,default = '',blank=True)
	tender_amt= models.FloatField(blank=True)
	date_start= models.DateField(blank=True)
	stipulated_date= models.DateField(blank=True)
	actual_date= models.DateField(blank=True)
	status= models.CharField(max_length=20,blank=True,choices=status_choices)
	expense= models.IntegerField(blank=True)
	remarks= models.TextField(max_length=200,blank=True)
	progress = models.CharField(max_length=20,blank=True)

	def __unicode__(self):
		return self.name

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Work._meta.fields]

class sub_work(models.Model):
	work= models.ForeignKey(Work,blank=True)
	name_subwork = models.CharField(max_length=1000)
	agency=models.CharField(max_length=200)


class agency(models.Model):
	name = models.CharField(max_length=200)
	add_1=models.CharField(max_length=500)
	add_2=models.CharField(max_length=500)
	#pan_no = models.CharField(max_length=200)


class TimeStamp(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	class Meta:
		abstract = True

class Document(TimeStamp):
	docfile = models.ImageField(upload_to='documents/%Y/%m/%d')
	relwork = models.ForeignKey(Work)


class Prog(TimeStamp):
	progressno = models.FloatField(blank=True)
	relatedwork = models.ForeignKey(Work)


'''
class Billing(models.Model):
	ra_bill= models.CharField(max_length=200,'R/A Bill No')
	expense_work_done= models.IntegerField(default=0,'Gross amount of work done')
	adv_paym= models.IntegerField(default=0,'Advance Payment')
	sec_adv= models.IntegerField(default=0,'Secured Advance')
	withheld= models.IntegerField(default=0,'Withheld if Any')
	sec_depst= models.IntegerField(default=0,'Secured Deposit')
	inc_tax= models.IntegerField(default=0,'Income Tax')
	ed_cess= models.IntegerField(default=0,'Education Cess')
	othr_cess= models.IntegerField(default=0,'Other Cess')
	sals_tax= models.IntegerField(default=0,'Sales Tax')
	worker_cess= models.IntegerField(default=0,'Worker Cess')
	withheld_dev= models.IntegerField(default=0,'Withheld for Deviation')
	withheld_eisi= models.IntegerField(default=0,'Withheld for EI/SI')
	withheld_eot= models.IntegerField(default=0,'Withheld for EOT')
	withheld_complete= models.CharField(blank=True,max_length=200,'Withheld for complete')
	withheld= models.IntegerField(default=0,'Withheld')

'''
