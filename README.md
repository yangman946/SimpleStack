# SimpleStack



<p align="center">
<img src="https://github.com/yangman946/SimpleStack/blob/main/logo_hq.png?raw=true" alt="simple stack">

<h1 align="center">Simple Stack</h1>
</p>

## About 

Welcome to SimpleStack.

SimpleStack is a Search Engine dedicated to solving your programming issues. It searches the web - using <a href="https://stackexchange.com/">Stack Exchange</a> - for suitable solutions.

SimpleStack cuts through all the redundancies, giving you only what matters, through overcoming bugs and issues by shaping the your input to yield clear and efficient search results with the aid of AI.

SimpleStack is a search engine designed for beginner developers and programmers with the intention to teach them efficient googling for overcoming bugs and issues. This tool searches “Stack Exchange” using their [API](https://api.stackexchange.com/docs) and shapes the user's input to yield clear and efficient search results. 



## Cloning


`$ git clone https://github.com/yangman946/SimpleStack`

## run

There are two ways to access this project:

### Run Django Server

If you wish to run SimpleStack locally or make contributions:

1) Make sure [python](https://www.python.org/) is installed and added to path
2) Get Django: `$ pip install django` via CMD
3) Get virtual environment: `$ pip install virtualenv`
4) Clone this project to your desired location: `$ git clone https://github.com/yangman946/SimpleStack`
5) In CMD: `$ cd [project directory]` (this directory should contain `manage.py`)
6) run `$ venv\Scripts\activate` to activate virtual environment
7) run `$ python manage.py runserver` to run server
8) Visit the locally hosted site (address shown on command prompt)

### Access directly via Web URL

1) TBA

## The algorithm

Although websites like Google can find results to programming issues, most developers, mainly beginners, struggle to find relevant information. 

### What makes SimpleStack Special?

```

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

```




Created by Clarence Yang 2021 for the HSC SDD major project.
