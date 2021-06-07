from django.http import HttpResponse
import json
import urllib.request
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
import re
import time
from django.views.generic.base import TemplateView
from django.shortcuts import render
import base64
import io
import mpld3

#class HomeView(TemplateView):
    #template_name = 'dashboard.html'
WWWW=1

def home(request):
# Data for plotting
    #while WWWW==1:

        #time.sleep(1)
        #ax.clear
        
        #Lim = GetLim()
        #xlimHigh=int(Lim[1])
        #xlimLow=int(Lim[0])

        #xlimHigh=1230
        #xlimLow=1780
    
        Q = GetData()
        #number = len(Q["ydata"])
        #increment = (xlimHigh-xlimLow)/number

        #x = np.arange(xlimLow, xlimHigh, increment)
        x = [element * 100000 for element in Q["xdata"]]
        s = Q["ydata"]


        fig, ax = plt.subplots()
        fig.set_size_inches(19, 10)
        ax.plot(x, s, linewidth=0.2, color= 'xkcd:black')

    #Lim = GetLim()
    #LimNum = int(Lim[0])
    
    
        ax.set(xlabel=Q["xlabel"]+' [um]', ylabel=Q["ylabel"]+ ' [DBM]',
           title='Time: '+ Q["timestamp"])
        ax.set_facecolor('xkcd:white')
        fig.patch.set_facecolor('xkcd:white')
        
        ax.title.set_color('black')
        ax.xaxis.label.set_color('black')        #setting up X-axis label color to yellow
        ax.yaxis.label.set_color('black')          #setting up Y-axis label color to blue

        ax.tick_params(axis='x', colors='black')    #setting up X-axis tick color to red
        ax.tick_params(axis='y', colors='black')  #setting up Y-axis tick color to black


        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.spines['left'].set_color('white')

        ax.grid(color='white', alpha=0.7)

    #number = len(Q["ydata"])

        

        response = HttpResponse(content_type = 'image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)
        #return response

        

        #encodedPNG = base64.b64encode(open(response, "rb").read())

        #s = io.BytesIO()

        #plt.plot(list(range(100)))

        #plt.savefig(s, format='png', bbox_inches="tight")
        #plt.close()
        #s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")

        #return '<img align="left" src="data:image/png;base64,%s">' % s

        html_graph = mpld3.fig_to_html(fig)

        
        #testvar = '<img align="left" src="data:image/png;base64,%s">' % s
        Sta = GetState()
        
        return render(request, 'dashboard.html', {'testvar': html_graph, 'STA': Sta})
        #return render(request, 'dashboard.html', {'testvar': html_graph})
        

    #Q = GetData()
    #return HttpResponse(LimNum)

def GetData():
    urlData = "http://flaskosa.herokuapp.com/cmd/TRACE"
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))
    return JSON_object

def GetLim():
    urlData2 = "http://flaskosa.herokuapp.com/cmd/LIM"
    webURL2 = urllib.request.urlopen(urlData2)
    data2 = webURL2.read().decode("utf-8")
    data2S = str(data2)
    data2L = re.findall(r'[\d.]+', data2S)
    #data2Num = str(data2L)
    return data2L  

def GetState():
    urlData3 = "http://flaskosa.herokuapp.com/cmd/STATE"
    webURL3 = urllib.request.urlopen(urlData3)
    data3 = webURL3.read().decode("utf-8")
    data3S = str(data3)
    if data3S == '+READY>"RUN"':
        Condition = 'Running Data Acquisition'
    elif data3S == '+READY>"IDLE"':
        Condition = 'Data Acquisition Stopped'
    else:
        Condition = 'ERROR/ Device Timed Out'
    return Condition

    
