from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Correlation, CorrelationForm


def index(request):
    latest_correlation_list = Correlation.objects.order_by('-pub_date')[:1]
    context = {'latest_correlation_list': latest_correlation_list, }

    if request.method == 'POST':
        input_form = CorrelationForm(request.POST)
        if input_form.is_valid():
            correy = Correlation()
            correy.title = input_form.cleaned_data['title']
            correy.xdata = input_form.cleaned_data['xdata']
            correy.xlabel = input_form.cleaned_data['xlabel']
            correy.ydata = input_form.cleaned_data['ydata']
            correy.ylabel = input_form.cleaned_data['ylabel']
            correy.calculate_coefficient()
            correy.save()

            return HttpResponseRedirect("/correlations/%s" % correy.id)
        else:
            context.update({'input_form': input_form})
    else:
        input_form = CorrelationForm()
        context.update({'input_form': input_form})

    return render(request, 'correlations/index.html', context)


def detail(request, correlation_id):
    correlation = Correlation.objects.get(pk=correlation_id)
    context = {'correlation': correlation}
    return render(request, 'correlations/detail.html', context)


# Plots are generated from the view to save space from
# storing images in a database.
def simple_plot(request, correlation_id):
    import django
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure

    fig = Figure()
    ax = fig.add_subplot(111)

    correlation = Correlation.objects.get(pk=correlation_id)
    x = []
    y = []

    for i in correlation.get_xdata_list():
        x.append(i)
    for i in correlation.get_ydata_list():
        y.append(i)

    ax.scatter(x, y)
    ax.set_xlabel(correlation.xlabel, size=15, backgroundcolor='w')
    ax.set_ylabel(correlation.ylabel, size=15)
    ax.set_title(correlation.title, size=20)

    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_figure(response, facecolor='w', dpi=80)
    return response
