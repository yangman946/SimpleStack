# SimpleStack



<p align="center">
<img src="https://github.com/yangman946/SimpleStack/blob/main/logo_hq.png?raw=true" alt="simple stack">

<h1 align="center">Simple Stack</h1>
</p>

## About 

Welcome to SimpleStack.

SimpleStack is a Search Engine dedicated to solving your programming issues. It searches the web - using <a href="https://stackexchange.com/">Stack Exchange</a> - for suitable solutions.

SimpleStack cuts through all the redundancies, giving you only what matters, through overcoming bugs and issues by shaping the your input to yield clear and efficient search results with the aid of AI.

SimpleStack is currently in it's Beta testing stage, please give feedback <a href="https://docs.google.com/forms/d/e/1FAIpQLSdAyl74t7nnGc5t78ZhApGON2LB7rt8ODKOEbc-OTHSJrSGtQ/viewform?usp=sf_link" target="_blank" rel="noopener noreferrer">here</a>.

## Cloning


`$ git clone https://github.com/yangman946/SimpleStack`

## Installation guide

There are two ways to access this project:

### Run Django Server

If you wish to run SimpleStack locally or make contributions:

1) Make sure [python](https://www.python.org/) is installed and added to path

<p align="center">
<img src="https://github.com/yangman946/SimpleStack/blob/main/install_1.png?raw=true" alt="simple stack">
</p>

2) open command prompt

3) Get Django: `$ pip install django` 

4) Get virtual environment: `$ pip install virtualenv`

4) Clone this project to your desired location: `$ git clone https://github.com/yangman946/SimpleStack` or download the source code:

<p align="center">
<img src="https://github.com/yangman946/SimpleStack/blob/main/install_2.PNG?raw=true" alt="simple stack">
</p>

5) Go to the project directory containing `manage.py` `$ cd [your desired location]/simplestack/website/simplestack` 

<p align="center">
<img src="https://raw.githubusercontent.com/yangman946/SimpleStack/main/install_3.PNG" alt="simple stack">
</p>

6) run `$ venv\Scripts\activate` to activate virtual environment

7) run `$ python manage.py runserver` to run server

8) Visit the locally hosted site (address shown on command prompt)

### Access directly via Web URL

1) Visit <a href="https://simplestack.pythonanywhere.com/">https://simplestack.pythonanywhere.com/</a> on your browser.

## The algorithm

Although websites like Google can also find results to programming issues, most developers, mainly beginners, struggle to find relevant information. 

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



<i>Created by Clarence Yang 2021 for the HSC SDD major project.</i>

