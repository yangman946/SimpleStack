# SimpleStack
SimpleStack is a web application that allows developers to easily find solutions to their problems. 

SimpleStack is a ‘search engine’ designed for beginner developers and programmers with the intention of teaching them efficient googling for overcoming bugs and issues. This tool searches “Stack Exchange” using their [API](https://api.stackexchange.com/docs) and attempts to shape the user's input to yield clear and efficient search results. 

Although many have access to google and the internet, it is evident that beginners especially find it difficult or daunting to efficiently search the web for solutions to their issues. Usually, an inefficient search would yield useless results leading to confusion. SimpleStack aims to overcome this by training them to be more knowledgeable at how they search rather than being more knowledgeable at what they search. 


## Cloning


`$ git clone https://github.com/yangman946/SimpleStack`

## run

There are two ways to access this project:

### Run Django Server

1) Make sure [python](https://www.python.org/) is installed and added to path
2) Get Django: `$ pip install django`
3) Get virtual environment: `$ pip install virtualenv`
4) Clone this project to your desired location: `$ git clone https://github.com/yangman946/SimpleStack`
5) In CMD: `$ cd [project directory]` (this directory should contain `manage.py`)
6) `$ venv\Scripts\activate` to activate virtual environment
7) `$ python manage.py runserver`
8) Visit the locally hosted site (address shown on command prompt)

### Access directly via Web URL

1) TBA

## The algorithm

### What differentiates SimpleStack from the standard search functions?

```

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
```




Created by Clarence Yang 2021 for the HSC SDD major project.
