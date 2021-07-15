'''
Python search engine by clarence yang 28/12/2020
This script is the main backend of SimpleStack, it handles the API

visit the website here: https://simplestack.pythonanywhere.com/

ALGORITHM: copyright clarence yang 2021

1) SimpleStack will use the given search query to find a list of relevant results and compare each to the following criteria:

    criteria:                                   good result:
    - will sort by score: vote count            [high]          
    - is answered                               [yes]      
    - answer count                              [high]    
    - view count                                [high]          
    - count of common tags                      [high]          
    - AI relevancy                              [high]
    - detected language                         [yes]
    - detected question type                    [yes]     

2) SimpleStack will unpack all answers and output the top answer to the user. 

3) Each subsequent answer is ranked according to a score derived from the criteria above. 

4) to fetch answers, an API call is made, getting the answer as JSON




note:
- confidence: determines relevancy of search
- %? = determines the relevancy of particular result


see data dictionary for all variables.

note: to download modules, make sure they are downloaded in venv

'''

#import libraries
import re
import json
import urllib
#import requests #json library
import numpy as np
import gzip
from urllib.request import Request, urlopen
from difflib import SequenceMatcher
#api
from wit import Wit 
from stackapi import StackAPI


class API_instance: #Object class is instantiated from views.py

    #language = ""
    #tags = []
    
    #array of question items
    selectedQuestions = [] # 5 items, will load more when show more.
    QuestionID = []
    scores = []

    #custom tags
    order = "desc"
    sort = "relevance"


    #probably useless words: common english words: https://gist.github.com/gravitymonkey/2406023 
    tagWhitelist = ["the","of","and","a","to","in","is","you","that","it","he","was","for","on","are","as","with",
    "his","they","I","at","be","this","have","from","or","one","had","by","word","but","not","what","all","were",
    "we","when","your","can","said","there","use","an","each","which","she","do","how","their","if","will","up",
    "other","about","out","many","then","them","these","so","some","her","would","make","like","him","into","time",
    "has","look","two","more","write","go","see","number","no","way","could","people","my","than","first","water",
    "been","call","who","oil","its","now","find","long","down","day","did","get","come","made","may","part", "carry",
    "help"]



    Search_query = "" #the search query



    
    #main function
    def main(self, query):

        
        print("\n") #formatting
        tag = self.Tag(query) #get tags

        #download json
        try:
            global SITE 
            global Search_query

            #instantiate API class
            SITE = StackAPI('stackoverflow', key = "eL78fGuZHts4TPORMYGiJw((") # The authetication key is passed to allow for an increased quota
            #preferences for API
            SITE.max_pages = 1
            SITE.page_size = 5

            #url formatter: this section deals with all the json mumbo jumbo
            text = "" #basically the contant "&tagged=", if it is not present, text2 should not be present
            text2 ="" #the search query

            #handling tags
            if (tag[5]): #if manual tagging
                #print("manual")
                text = "&tagged="
                if (tag[3] != "Unknown Language"): #if language is known
                    text2 = tag[3] 
                
                #if its unknown, whatever.
                for i in tag[0]: 
                    if (i != tag[3]): #tags except language
                        text2 = text2 + "; " + i 
            else:
                #print("automatic")
                text = "&tagged="
                if (tag[3] != "Unknown Language"):
                    text2 = tag[3]
                else:
                    #if language is unknown dont add anything to the tags.
                    text = ""
                    text2 = ""
            
            
            Search_query = tag[1]

            URL = ["https://api.stackexchange.com/2.2/search/advanced?order={0}&sort={1}&q=".format(self.order, self.sort), "&filter=default&closed=False&site=stackoverflow&run=true&key=eL78fGuZHts4TPORMYGiJw(("] #will append with appropriate query

            urlDownload = URL[0] + urllib.parse.quote_plus(tag[1]) + text + urllib.parse.quote_plus(text2) + URL[1] #get our formatted url -> to stack api
            print(urlDownload) #debug
            jreq = Request(urlDownload) #make a request
            html = gzip.decompress(urlopen(jreq).read()).decode('utf-8') #read it
            jsonMain = json.loads(html) #make it json readable

            #some debug statements
            #print("initial: " + str(len(jsonMain[0].items())))
            print("initial: " + str(len(jsonMain['items']))) #debug to console

            self.rank(jsonMain['items'], tag[0]) # ranking function -> will run once per query 

            #more debug
            print("final: " + str(len(jsonMain['items']))) #
            print("Results Found [questions/scores]: " + str(len(self.selectedQuestions)) + " " + str(len(self.scores)))
            print("\n")

            

            #if no matches found
            if (len(self.selectedQuestions) == 0):
                print("Failed to find any matches") #output result
                
                return "True", tag[1] #return result to views.py 
            else: #if matches are found
                
                try: #catch for errors
                    index = self.scores.index(max(self.scores)) #get the top answer's index (score)

                    top = self.selectedQuestions[index] #get the top question from this index

                    idTop = self.QuestionID[index] #get the ID of this top question

                    self.selectedQuestions.pop(index) #remove it because it is already displayed and we need the rest of the results to output ranked results                 
                    self.scores.pop(index) #remove the top score, it is already shown to the user.
                    self.QuestionID.pop(index) #remove top id. 
                except Exception as e:
                    print(str(e)) #print error if error present



            #sort all results in descending order
            result = self.sorter(self.selectedQuestions, self.scores, self.QuestionID)
            #print(result[1])
            #print(result[0])

            #return results to views.py (success)
            return tag[0], result[0], top, result[1], tag[4], tag[1], tag[2], tag[3], idTop, result[2], self.sort, self.order,
            #[0]tags, [1]questions array ranked, [2]top answer as question json, [3]scores array ranked, [4]ai confidence, [5]formatted query, [6]typestring, [7]language, [8]topid, [9]id array ranked, [10] sort type, [11] order type
        except Exception as e:
            print(str(e))
            return "Failed"

    #sorter: ranks the entire array: sorts it
    def sorter(self, questionsArray, scoresArray, idArray):
        s = np.array(scoresArray) #sort array using numpy
        array_sorted = np.argsort(s) #sorted array as index

        #arrays to return
        questions = [] 
        scores = []
        ids = []
        
        #assign values
        for i in range(len(array_sorted)):
            questions.append(questionsArray[array_sorted[i]])
            scores.append(scoresArray[array_sorted[i]])
            ids.append(idArray[array_sorted[i]])

        #gotta reverse array
        questions.reverse()
        scores.reverse()
        ids.reverse()

        #return arraays as descending order
        return questions, scores, ids


     
    #Ranking function: finds best results -> This function rates all results and is called once per query
    def rank(self, json, tags): #this function ranks all the given json from the API.
        #clear all arrays
        self.selectedQuestions.clear() 
        self.QuestionID.clear()
        self.scores.clear()

        
        #loop through the json file
        for i in range(len(json)):
            #scan the question, it is added if True is returned

            if self.itemScanner(json[i], tags): #algorithm to find optimal/best items <-- scanner function
                #the code below is only executed if true is returned, i.e., the question is good!
                self.selectedQuestions.append(json[i]) #add to our questions bank

                id_val = json[i]['question_id'] #get question id from question
                self.QuestionID.append(id_val) #add the ID

                #print("item added to array")


        #at this point we should have a list of satisfactory results

            


    #assignes a score to each potential answer: scans each question
    def itemScanner(self, item, tagsList): #this section of code assigns a value to each question
        
        #if no answers exist for this question, it should not be used
        if int(item['answer_count']) == 0: #this question no good if no answer
            return False #returns false, the question is not added because there are no answers

        score = 0 #begin scoring each question
        
        #the lower score means a better question.

        #print()
        if int(item['view_count']) < 80: #add score if views are inadequate.
            score += 0.1 
        

        

        if int(item['score']) > 400: #reduce score if upvotes are good
            score -= 0.15
        elif int(item['score']) <= 400 and int(item['score']) > 100: #reduce score if score is ok
            score -= 0.1
        elif int(item['score']) <= 100 and int(item['score']) > 0: 
            score -= 0.08
        elif score < 0: #we dont want questions with negative scores
            score += 0.1
        else:
            score += 0.15

        
        if item['is_answered'] == 'false': #give a score if the question is unanswered
            score += 0.1
        else: 
            score -= 0.15
        
        
            


        


        if 'tags' in item: #give score for each tag in the question
            for tag in item['tags']:
                if (tag not in tagsList):
                    score += 0.05
                else:
                    score -= 0.05

        

        #machine learning library here to check releavancy of title
        s = SequenceMatcher(None, item['title'], Search_query).ratio()
        if (s > 0.6): #if confidence is greater than 0.6, reduce score
            score -= 0.1

        scoreFinal = round((s*100)*(1-score), 2) #take average
        
        #print(str(scoreFinal))

        self.scores.append(scoreFinal) #add score to array
        return True #return true for good question


        






    #parser <-- to get a formatted answer this is the wrapper function
    def fetchResult(self, Item): #gives an array | gets one result of many answers
        #print(str(Item))
        #data = gzip.decompress(Item.read()).decode('utf-8')
        #data = json.dumps(str(Item)) 
        try:
            #get question ID from our saved question
            data = json.dumps(Item) #get json information
            jsonVal = json.loads(data) #format as json
            #will belong in standard results
            id_val = jsonVal['question_id'] #get question id from question json
            #title_val = Item['title']
            #url_val = Item['link']
            #user_val = Item['owner']['display_name']

            #print(jsonVal)

            #issue is that questions dont have answers

            resultTemp = SITE.fetch('questions/{ids}/answers', ids = [id_val], filter='withbody') #use API to fetch the answers of this ID

            #format answer JSON
            data2 = json.dumps(resultTemp)
            jsonDat = json.loads(data2)

            #print(jsonDat)

            index = 0 
            found = False
            score = [] #scores array for each answer item
            length = len(jsonDat['items'])
            #print("fetching data")
            for i in range(length): #loop through all items in answer array
                #print(jsonDat[i]['is_accepted'])
                
                if jsonDat['items'][i]['is_accepted'] == True:  #if an accepted question is found, use this one by default
                    index = i
                    found = True
                    break #break loop
                
                score.append(int(jsonDat['items'][i]['score'])) #add scores for each NON-ACCEPTED answer to an array

            #print(score)
            
            if found == False: #if no accepted question is found
                index = score.index(max(score)) #get highest score from scores array
            result = [] #result array
            #add each item of the top answer to the array above
            result.append(jsonDat['items'][index]['body'])  #0 : body content
            result.append(jsonVal['title'])                 #1 : title
            result.append(jsonVal['link'])                  #2 : url
            result.append(jsonVal['tags'])                  #3 : tags as array


            return result #return this answer 
        except Exception as e:
            print(str(e))
            return "an error has occured: " + str(e)


    #some cases require use to get a search query by its ID. You can see this in action if we manually plug in the id
    # https://simplestack.pythonanywhere.com/answer/[ID]
    def FetchResultByID(self, id): #requires the ID parameter of question
        try:
            global SITE 
            
            #API 
            SITE = StackAPI('stackoverflow', key = "eL78fGuZHts4TPORMYGiJw((") #where we source it, it could change depending on our algorithm, also an authetication key is passed to allow for a greater quota
            #preferences
            SITE.max_pages = 1
            SITE.page_size = 5

            result1 = SITE.fetch('questions/{ids}', ids = [id], filter='withbody') #get question from ID 

            #format QUESTION JSON
            data = json.dumps(result1)
            jsonVal = json.loads(data)


            resultTemp = SITE.fetch('questions/{ids}/answers', ids = [id], filter='withbody') #get answer from question ID
            #format answer JSON
            data2 = json.dumps(resultTemp) 
            jsonDat = json.loads(data2)

            index = 0
            found = False
            score = []
            length = len(jsonDat['items'])
            #print("fetching data")
            for i in range(length): #loop through all items of the answer JSON
                #print(jsonDat[i]['is_accepted'])
                
                if jsonDat['items'][i]['is_accepted'] == True: #if an accepted question is found, use this one by default
                    index = i
                    found = True
                    break #break from loop
                
                score.append(int(jsonDat['items'][i]['score'])) #add scores for each NON-ACCEPTED answer to an array

            #print(score)
            
            if found == False: #if no accepted question is found
                index = score.index(max(score)) #get max score
            result = []

            result.append(resultTemp['items'][index]['body'])           #0 : body content of question
            #answer stuff
            result.append(jsonVal['items'][0]['title'])                 #1 : title
            result.append(jsonVal['items'][0]['link'])                  #2 : url
            result.append(jsonVal['items'][0]['tags'])                  #3 : tags as array
            result.append(jsonVal['items'][0]['body'])                  #4 : body
            return result
        except Exception as e: 
            print("error: " + str(e))
            return False




    #this function gets the keywords or tags from a user's input. 
    #it utilises wit.ai to get the language and type of question
    #this function handles the custom tagging
    #this function returns: [0] tags [1] formatted query [2] language [3] type of answer [4] confidence
    def Tag(self, inputs):
        try:

            #variables for wit.ai
            searchType = ""
            sortx = ""

            #first lets find all text inside square brackets from the query
            try:

                searchType = re.findall(r'\[search:(.+?)\]', inputs)[0] #the search type, e.g. [search=relevance], this code gets string "relevance"
            except:
                print("error") #none found

            try:
                sortx = re.findall(r'\[order:(.+?)\]', inputs)[0] #the sort type, e.g. [order=desc], this code gets string "desc"
            except:
                print("error") #none found
            
            #debug
            #print("The search type " + str(searchType))
            #print("The order " + str(sortx))

            #variables
            formatQuery = "" 
            newtags = []
            language = ""
            typeString = ""
            
            manual = False #
            replace1 = "[search:" + str(searchType) + "]" #get custom tag string user typed
            #print(replace1)
            inputs = inputs.replace(replace1, "") #replace from query
            replace2 = "[order:" + str(sortx) + "]" #get custom tag string user typed
            inputs = inputs.replace(replace2, "") #replace from query

            res = re.findall(r"\[(\w+)\]", inputs) #this represents the user's manual tag input 
            #print("The element between brackets : " + str(res))  #debug
            #print(str(inputs))

            if searchType != "": #if the search type is specified by the user
                self.sort = searchType #set global variables to be added to the URL. 
            
            if sortx != "": #if the sort type is specified by the user
                self.order = sortx #set global variable to be used by API

            if ((len(res) > 0) and ("tagoff" not in res)):  #if the user manually set tags 
                
                formatQuery = inputs
                newtags = res #our array
                for item in res: #loop through array
                    formatQuery = formatQuery.replace("[" + item +"]", "") #remove this manual tag
                manual = True
                formatQuery = formatQuery.lstrip() #removes any excess spaces
            else: #other wise we gotta use the algorithm to guess the tags
                #formatted = re.sub('[^A-Za-z0-9]+', '', input) #remove special characters
                inputs = inputs.replace("[tagoff]", "") # replace the tagoff custom tag if needed
                
                tags = inputs.split() #split all words
                
                for item in tags: #remove redundant words from the query
                    if item.lower() not in self.tagWhitelist:
                        
                        newtags.append(item) #add 'key' words to the array
                
                formatQuery = inputs.lstrip() #remove redundant spaces
            

                
            confidence = 0 #confidence meter.
            #get language from wit.ai. Trained from https://wit.ai/ 
            try: 
                #
                client = Wit('FNOV34ELP36N42GEHKKHYY27YMWQTJEW') #instantiate a wit.ai instance
                response = client.message(inputs) #call function with formatted input
                #print(response) #debug
                r = json.dumps(response) #get json
                jsonMain = json.loads(r) #make it json readable
                typeString = jsonMain['intents'][0]['name'] #get type of query: question, error, etc. 
                
                confidence1 = float(jsonMain['intents'][0]['confidence']) #get confidence of intent 

                try: #we can get the confidence value from the AI
                    language = jsonMain['entities']['language_detect:language_detect'][0]['value'] #confidence of language type
                    confidence2 = float(jsonMain['entities']['language_detect:language_detect'][0]['confidence']) #as float
                except:
                    confidence2 = confidence1 #ignore
                    
                

                confidence = (confidence1 + confidence2)/2 #average confidence
                #print("confidence: " + str(confidence)) #debug
            except Exception as e: #doesnt work?
                print("error: " + str(e))

            #default
            if (typeString == ""):
                typeString = "Unknown type"
            
            if (language == ""):
                language = "Unknown Language"

            newtags = list(dict.fromkeys(newtags)) #remove any duplicate items from tags
            
            #print(newtags)
            

            return newtags, formatQuery, typeString, language, confidence, manual #return tag values
        except Exception as e: #debug purposes
            print(str(e))
            return "an error has occured: " + str(e)

        



