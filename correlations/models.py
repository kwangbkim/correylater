from django import forms
from django.db import models
from datetime import datetime
from scipy.stats.stats import pearsonr

import decimal
import StringIO
import csv
import string
import re
    
# Create your models here.
class Correlation(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    coefficient = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    xdata = models.CharField(max_length=5000)
    xlabel = models.CharField(max_length=200)
    
    ydata = models.CharField(max_length=5000)
    ylabel = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.title
    
    def calculate_coefficient(self):
        x = self.get_xdata_list()
        y = self.get_ydata_list()
        z = pearsonr(x, y)
        self.coefficient = z[0]
        
    def get_xdata_list(self):
        l = CommaDelimitedParser.numbers_to_list(self.xdata)
        return l
            
    def get_ydata_list(self):
        l = CommaDelimitedParser.numbers_to_list(self.ydata)
        return l
        
class CorrelationForm(forms.Form):
    title = forms.CharField(max_length=200)
    xlabel = forms.CharField(max_length=200)
    xdata = forms.CharField(max_length=5000, widget=forms.Textarea)
    ylabel = forms.CharField(max_length=200)
    ydata = forms.CharField(max_length=5000, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(CorrelationForm, self).clean()
        x = cleaned_data.get("xdata")
        y = cleaned_data.get("ydata")
        
        xcheck = CommaDelimitedParser.validate_number_array(x)
        if xcheck != "":
            self._errors["xdata"] = self.error_class([xcheck])
            del cleaned_data["xdata"]
        
        ycheck = CommaDelimitedParser.validate_number_array(y)
        if ycheck != "":
            self._errors["ydata"] = self.error_class([ycheck])
            del cleaned_data["ydata"]
                    
        if xcheck != "" or ycheck != "":
            return cleaned_data
        
        xl = CommaDelimitedParser.numbers_to_list(x)
        yl = CommaDelimitedParser.numbers_to_list(y)
        
        if len(xl) != len(yl):
            self._errors["xdata"] = self.error_class(["X and Y data sets should have same number of elements.  X: " + str(len(xl))])
            self._errors["ydata"] = self.error_class(["Y: " + str(len(yl))])
            
            del cleaned_data["xdata"]
            del cleaned_data["ydata"]
            
        return cleaned_data
        
class CommaDelimitedParser:
    
    @staticmethod
    def numbers_to_list(value):
        s = StringIO.StringIO(value)
        reader = csv.reader(s, delimiter=',')
        l = list(map(float, row) for row in reader)
        return l[0]
        
    @staticmethod
    def validate_number_array(value):
        if not "," in value: 
            return "Data should be comma delimited (1.1, 2.2, 3.3 ...)"
        
        letter_search = re.findall('[A-Za-z]', value)
        if len(letter_search) > 0:
            return "Are you crazy?!  Data should be numbers only."

        return ""