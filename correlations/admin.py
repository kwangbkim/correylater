from django.contrib import admin
from correlations.models import Correlation

class CorrelationAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'title', 'coefficient', 'xlabel', 'xdata', 'ylabel', 'ydata']
    list_filter = ['pub_date']
    
admin.site.register(Correlation, CorrelationAdmin)