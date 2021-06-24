'''
Python search engine by clarence yang 28/12/2020
This script is the main backend of SimpleStack, it handles the API



ALGORITHM: copyright clarence yang 2021

1) will use search query to find a list of relevant results: not using wrapper: getting list of most appropriate questions and getting their ID
    criteria:                                   a good result:
    - will sort by score: vote count            [high]          //
    - if it is answered                         [answered]      //
    - if is is closed or not                    [not closed]    
    - view count                                [high]          //
    - count of how many tags are common         [high]          
    - count of how many answers                 [high]          
2) will unpack all answers and output the top/accepted one to the user. 
3) this will only show the top one [change if needed], the user will press MORE to show more answers
4) link/button at bottom of page will enable user to refresh and find better question either manually from my list or automatically via the algorithm
5) this repeats step 2 and below.



note:
- confidence: determines relevancy of search
- %? = determines the relevancy of particular result


see data dictionary for all variables.

note: to download modules, make sure they are downloaded in venv

'''

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

class API_instance: #Object class could be instantiated from external code, i.e. the DJANGO frontend: blueprint for backend logic

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



    Search_query = ""



    
    #main function
    def main(self, query):

        
        print("\n") #debug
        tag = self.Tag(query) #get tags

        #download json
        try:
            global SITE 
            global Search_query

            #instantiate API class
            SITE = StackAPI('stackoverflow', key = "eL78fGuZHts4TPORMYGiJw((") # The authetication key is passed to allow for an increased quota
            #preferences
            SITE.max_pages = 1
            SITE.page_size = 5

            #url formatter: this section deals with all the json mumbo jumbo
            text = "" #basically the contant "&tagged=", if it is not present, text2 should not be present
            text2 ="" #the search query

            
            if (tag[5]): #if manual tagging
                text = "&tagged="
                if (tag[3] != "Unknown Language"): #if language is known
                    text2 = tag[3]
                
                #if its unknown, whatever.
                for i in tag[0]: 
                    if (i != tag[3]): #tags except language
                        text2 = text2 + "; " + i 
            else:
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
            print("initial: " + str(len(jsonMain['items'])))

            self.rank(jsonMain['items'], tag[0]) # ranking function -> will run once per query 

            print("final: " + str(len(jsonMain['items']))) #
            print("Results Found [questions/scores]: " + str(len(self.selectedQuestions)) + " " + str(len(self.scores)))
            print("\n")

            #show top result

            #if no matches found
            if (len(self.selectedQuestions) == 0):
                print("Failed to find any matches")
                
                return "True", tag[1]
            else: #if matches are found
                
                try: #catch for errors
                    index = self.scores.index(max(self.scores)) #get the top answer's index (score)

                    top = self.selectedQuestions[index] #get the top question from this index

                    idTop = self.QuestionID[index]

                    self.selectedQuestions.pop(index) #remove it because it is already displayed and we need the rest of the results to output ranked results                 
                    self.scores.pop(index) #remove the top score, it is already shown to the user.
                    self.QuestionID.pop(index)
                except Exception as e:
                    print(str(e)) #print error



            #sort all results in descending order
            result = self.sorter(self.selectedQuestions, self.scores, self.QuestionID)
            #print(result[1])
            print(result[0])
            return tag[0], result[0], top, result[1], tag[4], tag[1], tag[2], tag[3], idTop, result[2], self.sort, self.order,
            #[0]tags, [1]questions array ranked, [2]top answer as question json, [3]scores array ranked, [4]ai confidence, [5]formatted query, [6]typestring, [7]language, [8]topid, [9]id array ranked, [10] sort type, [11] order type
        except Exception as e:
            print(str(e))
            return "Failed"

    #sorter: ranks the entire array
    def sorter(self, questionsArray, scoresArray, idArray):
        s = np.array(scoresArray) #sort array
        array_sorted = np.argsort(s)

        questions = []
        scores = []
        ids = []
        #gotta reverse array
        for i in range(len(array_sorted)):
            questions.append(questionsArray[array_sorted[i]])
            scores.append(scoresArray[array_sorted[i]])
            ids.append(idArray[array_sorted[i]])

        questions.reverse()
        scores.reverse()
        ids.reverse()

        return questions, scores, ids


     
    #Ranking function: finds best results -> This function rates all results
    def rank(self, json, tags): #this function ranks all the given json from the API.
        self.selectedQuestions.clear() #LIST OF ALL SATISFACTORY QUESTIONS: we clear
        self.QuestionID.clear()
        self.scores.clear()
        counterAppend = 0 
        
        
        count = len(self.selectedQuestions) 
        
        #loop through the json file
        for i in range(len(json)):
            #scan the question, it is added if True is returned

            if self.itemScanner(json[i], tags): #algorithm to find optimal/best items

                self.selectedQuestions.append(json[i]) #add to our questions bank

                id_val = json[i]['question_id'] #get question id from question
                self.QuestionID.append(id_val)



        #at this point we should have a list of satisfactory results

            


    #assignes a score to each potential answer

    def itemScanner(self, item, tagsList): #this section of code assigns a value to each question
        
        #if no answers exist for this question, it should not be used
        if int(item['answer_count']) == 0: #this question no good if no answer
            return False

        score = 0
            
        #print()
        if int(item['view_count']) < 80:
            score += 0.1
        

        

        if int(item['score']) > 400:
            score -= 0.15
        elif int(item['score']) <= 400 and int(item['score']) > 100:
            score -= 0.1
        elif int(item['score']) <= 100 and int(item['score']) > 0:
            score -= 0.08
        elif score < 0:
            score += 0.1
        else:
            score += 0.15

        
        if item['is_answered'] == 'false': #give a score if the question is answered
            score += 0.1
        else:
            score -= 0.15
        
        
            


        


        if 'tags' in item: #give score for each tag in the question
            for tag in item['tags']:
                if (tag not in tagsList):
                    score += 0.05
                else:
                    score -= 0.05

        

        #add machine learning here to check releavancy of title
        s = SequenceMatcher(None, item['title'], Search_query).ratio()
        if (s > 0.6):
            score -= 0.1

        scoreFinal = round((s*100)*(1-score), 2)
        
        print(str(scoreFinal))

        self.scores.append(scoreFinal) #get a percentage score for each 
        return True


        






    #parser <-- to get a formatted answer this is the wrapper function
    def fetchResult(self, Item): #gives an array | gets one result of many answers
        #print(str(Item))
        #data = gzip.decompress(Item.read()).decode('utf-8')
        #data = json.dumps(str(Item)) 
        try:
            #get question ID from our saved question
            data = json.dumps(Item)
            jsonVal = json.loads(data)
            #will belong in standard results
            id_val = jsonVal['question_id'] #get question id from question
            #title_val = Item['title']
            #url_val = Item['link']
            #user_val = Item['owner']['display_name']

            #print(jsonVal)

            #issue is that questions dont have answers

            resultTemp = SITE.fetch('questions/{ids}/answers', ids = [id_val], filter='withbody') #use

            data2 = json.dumps(resultTemp)
            jsonDat = json.loads(data2)

            #print(jsonDat)

            index = 0
            found = False
            score = []
            length = len(jsonDat['items'])
            #print("fetching data")
            for i in range(length): #loop through all items
                #print(jsonDat[i]['is_accepted'])
                
                if jsonDat['items'][i]['is_accepted'] == True: 
                    index = i
                    found = True
                    break
                
                score.append(int(jsonDat['items'][i]['score']))

            #print(score)
            
            if found == False:
                index = score.index(max(score)) #error
            result = []
            #
            result.append(jsonDat['items'][index]['body'])  #0 : body content
            result.append(jsonVal['title'])                 #1 : title
            result.append(jsonVal['link'])                  #2 : url
            result.append(jsonVal['tags'])                  #3 : tags as array


            return result
        except Exception as e:
            print(str(e))
            return "an error has occured: " + str(e)

    def FetchResultByID(self, id):
        try:
            global SITE 
            
            SITE = StackAPI('stackoverflow', key = "eL78fGuZHts4TPORMYGiJw((") #where we source it, it could change depending on our algorithm, also an authetication key is passed to allow for a greater quota
            #preferences
            SITE.max_pages = 1
            SITE.page_size = 5

            result1 = SITE.fetch('questions/{ids}', ids = [id], filter='withbody') #use

            data = json.dumps(result1)
            jsonVal = json.loads(data)


            resultTemp = SITE.fetch('questions/{ids}/answers', ids = [id], filter='withbody') #use
            data2 = json.dumps(resultTemp)
            jsonDat = json.loads(data2)
            index = 0
            found = False
            score = []
            length = len(jsonDat['items'])
            #print("fetching data")
            for i in range(length): #loop through all items
                #print(jsonDat[i]['is_accepted'])
                
                if jsonDat['items'][i]['is_accepted'] == True: 
                    index = i
                    found = True
                    break
                
                score.append(int(jsonDat['items'][i]['score']))

            #print(score)
            
            if found == False:
                index = score.index(max(score)) #error
            result = []

            result.append(resultTemp['items'][index]['body'])           #0 : body content
            #question
            result.append(jsonVal['items'][0]['title'])                 #1 : title
            result.append(jsonVal['items'][0]['link'])                  #2 : url
            result.append(jsonVal['items'][0]['tags'])                  #3 : tags as array
            result.append(jsonVal['items'][0]['body'])                  #4 : body
            return result
        except Exception as e:
            print("error: " + str(e))
            return False

    #this function gets the keywords or tags from a user's input. 
    #it also utilises wit.ai to get the language and type of question
    #this function returns: [0] tags [1] formatted query [2] language [3] type of answer [4] confidence
    def Tag(self, inputs):
        try:

            #function to extract tags 
            #we want to extract key words
            searchType = ""
            sortx = ""
            #first lets find all text inside square brackets from the query
            try:

                searchType = re.findall(r'\[search:(.+?)\]', inputs)[0]
            except:
                print("error")

            try:
                sortx = re.findall(r'\[order:(.+?)\]', inputs)[0]
            except:
                 print("error")
            
            print("The search type " + str(searchType))
            print("The order " + str(sortx))
            #declare some variables
            formatQuery = "" 
            newtags = []
            language = ""
            typeString = ""
            
            manual = False
            replace1 = "[search:" + str(searchType) + "]"
            print(replace1)
            inputs = inputs.replace(replace1, "")
            replace2 = "[order:" + str(sortx) + "]"
            inputs = inputs.replace(replace2, "")

            res = re.findall(r"\[(\w+)\]", inputs) #this represents the user's manual tag input
            print("The element between brackets : " + str(res))  #debug
            print(str(inputs))

            if searchType != "":
                self.sort = searchType
            
            if sortx != "":
                self.order = sortx

            if ((len(res) > 0) and ("tagoff" not in res)):  #check if the user manually set tags
                #do whatever
                formatQuery = inputs
                newtags = res #our array
                for item in res:
                    formatQuery = formatQuery.replace("[" + item +"]", "") #remove this manual tag
                manual = True
                formatQuery = formatQuery.lstrip()
            else: #other wise we gotta use the algorithm to guess the tags
                #formatted = re.sub('[^A-Za-z0-9]+', '', input) #remove special characters
                inputs = inputs.replace("[tagoff]", "")
                
                tags = inputs.split() #split all words
                
                for item in tags: #remove redundant words from the query
                    if item.lower() not in self.tagWhitelist:
                        
                        newtags.append(item) #add 'key' words to the array
                
                formatQuery = inputs.lstrip() #its not really formatted
            

                
            confidence = 0
            #get language from wit.ai
            try: 
                #
                client = Wit('FNOV34ELP36N42GEHKKHYY27YMWQTJEW') #instantiate a wit.ai instance
                response = client.message(inputs)
                print(response)
                r = json.dumps(response)
                jsonMain = json.loads(r) #make it json readable
                typeString = jsonMain['intents'][0]['name']
                
                confidence1 = float(jsonMain['intents'][0]['confidence'])

                try:
                    language = jsonMain['entities']['language_detect:language_detect'][0]['value']
                    confidence2 = float(jsonMain['entities']['language_detect:language_detect'][0]['confidence'])
                except:
                    confidence2 = confidence1
                    
                

                confidence = (confidence1 + confidence2)/2
                print("confidence: " + str(confidence))
            except Exception as e: #doesnt work?
                print("error: " + str(e))

            if (typeString == ""):
                typeString = "Unknown type"
            
            if (language == ""):
                language = "Unknown Language"

            newtags = list(dict.fromkeys(newtags)) #remove any duplicate items
            
            #print(newtags)
            

            return newtags, formatQuery, typeString, language, confidence, manual
        except Exception as e: #debug purposes
            print(str(e))
            return "an error has occured: " + str(e)

        



