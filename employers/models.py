from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from recruit.choices import (TIMEZONE_CHOICES, COUNTRY_CHOICES, GENDER_CHOICES,
	EDUCATION_CHOICES, EMPLOYER_TYPE_CHOICES, POSITION_TYPE_CHOICES, 
	DESIRED_MONTHLY_SALARY_CHOICES)

class Employer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)	
	phone_number = PhoneNumberField(blank=False)
	name_english = models.CharField(blank=False, max_length=200)
	name_local = models.CharField(blank=False, max_length=200)
	address_english = models.CharField(blank=False, max_length=200)
	address_local = models.CharField(blank=False, max_length=200)
	business_license = models.ImageField(upload_to='employer/%Y/%m/%d')
	business_license_thumb = models.ImageField(upload_to='employer/%Y/%m/%d', blank=True)

	def __str__(self):
		return self.name_english

	def save(self, *args, **kwargs):
		from recruit.utils import generate_thumbnail
		thumb = generate_thumbnail(self.business_license)
		self.business_license_thumb=thumb
		super(Employer, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		from recruit.utils import delete_from_s3
		delete_from_s3(self.business_license)
		delete_from_s3(self.business_license_thumb)
		if self.images.count() > 0:
			for image in self.images.all():
				delete_from_s3(image.image)
				delete_from_s3(image.thumb)
		super(Employer, self).delete(*args, **kwargs)

class EmployerRequirements(models.Model):
	employer = models.OneToOneField(Employer, on_delete=models.CASCADE)
	education = models.CharField(
			max_length=25,
			blank=True,
			choices=EDUCATION_CHOICES,
		)
	education_major = models.CharField(max_length=50, blank=True)
	age_range_low = models.IntegerField(blank=True)
	age_range_high = models.IntegerField(blank=True)
	years_of_experience = models.IntegerField(blank=True)
	citizenship = CountryField(blank=True)

class EmployerImages(models.Model):
	employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='images')
	cover_image = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	image = models.ImageField(upload_to='employer/%Y/%m/%d')
	thumb = models.ImageField(upload_to='employer/%Y/%m/%d', blank=True)

	def save(self, *args, **kwargs):
		from recruit.utils import generate_thumbnail
		thumb = generate_thumbnail(self.image)
		self.thumb=thumb
		super(EmployerImages, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		from recruit.utils import delete_from_s3
		delete_from_s3(self.image)
		delete_from_s3(self.thumb)
		super(EmployerImages, self).delete(*args, **kwargs)	