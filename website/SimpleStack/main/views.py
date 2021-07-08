'''
SimpleStack views.py by clarence yang 07/01/2021

this script handles the views: kinda like a library of httpresponses we can get and output
it is like a directory, it will output a response based on requests.

it will interact with templates


'''

from django.shortcuts import render 
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import RequestContext
import random
from . import Main
import html
import time
import sys
import threading
import urllib.parse


# random searh bar text
randomText = ["What's your question?", "What is your issue?", "Search for a solution!", "What are you having trouble with?", "What's the problem?"]
resultBody = []
resultTitle = []
resultLink = []
resultTags = []


resultContent = []

pageLength = 5

scoreTag = 0


def home(request): #happens on home load
    #return HttpResponse('Hello world!')
    context = {
        #'result': Post.objects.all(), #database content
        'title': 'Home', #how we pass the title
        'textSearch': randomText[random.randint(0, len(randomText)-1)] #send a random search bar text
    }
    return render(request, 'main/home.html', context) #renders entire html

def about(request): #about webpage
    #return HttpResponse('about')
    return render(request, 'main/about.html', {'title': 'About'}) #sends the title parameter

def guide(request):
    return render(request, 'main/guide.html', {'title': 'Guide'})

#search request 
def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        start_time = time.time() #start recording time

        #print(search) #debug
        formatted_search = urllib.parse.quote_plus(search) 

        if (search == ""): #if no search query
            context = { 
                #'result': Post.objects.all(), #database content
                'title': 'Home', #how we pass the title
                'textSearch': randomText[random.randint(0, len(randomText)-1)] 
                #ignore
            }
            return render(request, 'main/home.html', context) #do nothing
        elif(encrypt(search.replace(" ", ""), 5) == "bmfynxnxmfs"): #debug ############################## debug
                colours = ["blue", "green", "red", "orange"]

                context = {
                    'title': 'Search', #how we pass the title
                    'Search': search, #
                    'debug': True,
                    'text': encrypt("mwlimr", -4),
                    'type': 'uhhh.... you found it: ',
                    'debug_text': colours[random.randint(0, len(colours)-1)],


                    
                    #pass more stuff to be shown
                }

                return render(request,'main/SearchErr.html', context) ####################################### debug
        else: #get output
            instance = Main.API_instance() #create instance of our api class: main.py class. 

            
            result = instance.main(search) #takes in a query 
            #print(result)
            
            if(result[0] == "True"): #if no results found
                #trouble shooting tips.
                shoot = ['Narrow down your search to simple key word terms, for example: "python print hello world"', 'send feedback'] 
                context = {
                    'title': 'No results found', #how we pass the title
                    'Search': result[1], #the 
                    'debug': False,
                    'type': 'No Results for ',
                    'info': 'Unfortunately, it appears that no results could be found for your search, but don\'t worry, here are a few things you can try: ',
                    'shoot': shoot,
                    
                    
                    #pass more stuff to be shown
                }

                return render(request,'main/SearchErr.html', context) #show user that no result was found
            elif(result == "Failed"): #query error 
                shoot = ['make sure tags are correct', 'send feedback']
                context = {
                    'title': 'Search Error', #how we pass the title
                    'Search': search, #
                    'debug': False,
                    'type': 'Error While Searching ',
                    'info': 'Unfortunately, it appears that an error has occurred, but don\'t worry, here are a few things you can try: ',
                    'shoot': shoot,
                    
                    #pass more stuff to be shown
                }

                return render(request,'main/SearchErr.html', context) #show user query error. 
            else: #if working
                #print(result[2]) #debug

    
                global resultContent
                
                
                p = Paginator(result[1], pageLength) #create a paginator

                

                page_num = request.GET.get('page', 1) #given through url

                try:

                    page = p.page(page_num) #set page to current page
                except:
                    page = p.page(1)

                
                
                global scoreTag
                #scoreTag = 0

                #clear all arrays
                resultBody.clear()
                resultTitle.clear()
                resultLink.clear()
                resultTags.clear()
                resultContent.clear()
                
                


                #threading speeds up the search
                threads = []
                length = 0

                counter = 0
                for item in page: #five items should exist or not, doesnt matter

                    t = threading.Thread(target=threadTarget, args=(item, instance, counter))
                    t.daemon = True #when program is shut down, so do the threads
                    
                    threads.append(t)
                    length += 1
                    counter += 1
                
                for i in range(length):
                    resultBody.append('')
                    resultTitle.append('')
                    resultLink.append('')
                    resultTags.append('')
                    resultContent.append('')
                    

               

                if int(page_num) == 1: #if this is the top answer, add the top answer result to the pool of threads
                    print("getting top")
                    t2 = threading.Thread(target=threadTop, args=(result, instance, result[5]))
                    t2.daemon = True
                    threads.append(t2)
                    length += 1


                    
                #print(str(length) + "|" + str(len(threads)))
                for i in range(length): #start all threads
                    threads[i].start()
                
                for i in range(length): #join all threads
                    threads[i].join()

                confident = False

                scoreTag = round(scoreTag, 2)


                if (scoreTag > 50):
                    confident = True
                
                
                arrayFinal = zip(resultBody, resultTitle, resultLink, resultTags, result[9])

                print ("is confident: " + str(confident) + " | score: " + str(scoreTag))

                total = time.time() - start_time
                
                #not very efficient method for numbering:
                pages = []
                for i in range(p.num_pages):
                    
                    pages.append(str(i + 1))

                print("paginated pages: " + str(len(pages)) + "|current page: " + str(page_num))

                

                prefix = "?search=" + formatted_search

                


                if int(page_num) == 1:
                    #print('asdf')
                    context = { #loop for other results?
                        'title': 'Search results', #how we pass the title
                        'Search': result[5], #the title
                        'resultCount': str(len(result[1]) + 1), #
                        'tags': result[0],
                        'confident': confident,
                        'time': int(total*1000),
                        'ArrayFinal': arrayFinal,
                        'pages': pages,
                        'currentPage': int(page_num),
                        'TotalPages': len(pages),
                        'TopAns': str(resultContent[0]), #body
                        'TopID': int(result[8]), #top id
                        'TopTitle': html.unescape(resultContent[1]), #title
                        'link': resultContent[2],
                        'tagsQ': resultContent[3],
                        'pre': prefix,
                        'items': page,
                        'language': result[7],
                        'type': result[6],
                        'confidence': str(scoreTag),
                        'sort': result[10],
                        'order': result[11],
                        #pass more stuff to be shown
                    }
                else:
                    print(page_num)
                    context = { #loop for other results?
                        'title': 'Search results', #how we pass the title
                        'Search': result[5], #the title
                        'resultCount': str(len(result[1]) + 1), #
                        'tags': result[0],
                        'confident': confident,
                        'time': int(total*1000),
                        'ArrayFinal': arrayFinal,
                        'pages': pages,
                        'currentPage': int(page_num),
                        'TotalPages': len(pages),
                        'pre': prefix,
                        'items': page,
                        'language': result[7],
                        'type': result[6],
                        'confidence': str(scoreTag),
                        'sort': result[10],
                        'order': result[11],
                        #pass more stuff to be shown
                    }

                #print(context)




                #todo: get a list of elements to be set as global
        return render(request, 'main/search.html', context) #renders entire html
        #return a render of the desired page with appropriate content #the search page

def threadTop(item, instance, search): #this code determines the search confidence
    global resultContent
    
    resultContent = instance.fetchResult(item[2]) #pass the json: 0 - body content | 1 - title | 2 - url | 3 - tags as array

    global scoreTag #a score to deduct values from
    score = 0
    if (len(item[1]) < 10):
        score += 0.1 #less results? hmmm?
    
    '''
    for i in range(len(item[0])):
        if (item[0][i] not in resultContent[3]) and (len(resultContent[3]) >= len(item[0])): #if our tags are not in the top answer array
            score += 2
    '''
    '''
    if search not in resultContent[1]: #split this?
        score += 2
    '''

    avg = round(sum(item[3])/len(item[3]),2)
    if avg < 50:
        score += 0.2

    print ("average score: "+ str(avg))

    #we'll get machine learning to handle the whole title part
    if (item[7] == "Unknown Language"):
        score += 0.1
    
    if (item[6] == "Unknown type"):
        score += 0.1
        
    #item[4] is average confidence
    scoreTag = (item[4] * 100)*(1-score)
    
def answer(request, id):
    
    print("debugg: " + str(id))
    instance = Main.API_instance() #create instance of our api wrapper

    resultX = instance.FetchResultByID(id)
    print(resultX)

    if (resultX == False):
        #failed
        

        shoot = ['Make sure the URL is correct', 'send feedback'] 
        context = {
            'title': 'No results found', #how we pass the title
            'failed': True,
            
            
            'info': 'Unfortunately, it appears that this answer does not exist, but don\'t worry, here are a few things you can try: ',
            'shoot': shoot,
            
            
            #pass more stuff to be shown
        }
    else:

        body = str(resultX[0])
        title = html.unescape(resultX[1])
        link = resultX[2]
        tagsArray = resultX[3]
        questionbody = resultX[4]


        context = {
            'title': title, #how we pass the title
            'body': body,
            'link': link,
            'tags': tagsArray,
            'questionbody': questionbody,
            'failed': False,
            
            #pass more stuff to be shown
        }

    return render(request,'main/answer.html', context)



def threadTarget(item, instance, i):
    resultX = instance.fetchResult(item)
    resultBody[i] = str(resultX[0])
    resultTitle[i] = html.unescape(resultX[1])
    resultLink[i] = resultX[2]
    resultTags[i] = resultX[3]
  


def encrypt(text,s):
    
    result = ""
    # transverse the plain text
    for i in range(len(text)):
      char = text[i]
      # Encrypt uppercase characters in plain text
      
      if (char.isupper()):
        result += chr((ord(char) + s-65) % 26 + 65)
      # Encrypt lowercase characters in plain text
      else:
        result += chr((ord(char) + s - 97) % 26 + 97)
    return result


#error pages

def handler_404(request, *args, **argv):
    data = {"title": "Page not found"}
    return render(request,'main/404.html', data)

def handler_500(request, *args, **argv):
    type_, value, traceback = sys.exc_info()
    data = {
        "title": "This Question does not exist!",
        "value": value,
        "traceback": traceback,
        }
    
    #print(str(type_) + "|" + str(value) + "|" + str(traceback))

    return render(request,'main/500.html', data)

#EULA

def legal(request):
    data = {"title": "Legal"}
    return render(request,'main/Legal.html', data)