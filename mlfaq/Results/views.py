from django.shortcuts import render
from os import listdir
import os
import re, math
from collections import Counter
import urllib.request, json
from stop_words import get_stop_words

# Create your views here.

WORD = re.compile(r'\w+')
path = os.path.dirname(os.path.abspath(__file__))
sentlist = open(path + "/corpus.txt", "r").readlines()

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

def results(request):

    if request.method == "POST":
        stop_words = get_stop_words('en')
        spec_stop = ['opinion','thoughts']
        for i in spec_stop:
            stop_words.append(i)

        query = request.POST.get("search")   	
        text1 = query
        txtarr = text1.split(' ')
        textarr = [word for word in txtarr if word not in stop_words]
        text1 = ''
        for i in textarr:
            text1 += i + ' '

        finalstr=''

        vector1 = text_to_vector(text1)
        ans = []

        for i in sentlist:
            vector2 = text_to_vector(i)
            cosine = get_cosine(vector1, vector2)
            ans.append( (i,cosine) )

        ans = sorted(ans, key=lambda x: -1 * x[1])


        for i in ans:
            if i[1] > 0:
                finalstr += i[0]
            else:
                break

        return render(request, 'Results/index.html', {'best_hit': finalstr})
    else:
        return render(request, 'Results/index.html', {})
