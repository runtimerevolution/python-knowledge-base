# Python/Django Onboarding

## References

- [A Byte of Python](https://python.swaroopch.com/) (Learn Python)
- [Awesome Python](https://github.com/vinta/awesome-python) (List of Python Resources)
- [Project Setup](./PROJECT-SETUP.md)
- [Getting Started with Django](https://www.djangoproject.com/start/)
  - [Quick install guide](https://docs.djangoproject.com/en/dev/intro/install/)
  - [Write your first Django app](https://docs.djangoproject.com/en/dev/intro/tutorial01/)
  - [Django documentation](https://docs.djangoproject.com/en/dev/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [pandas](https://pandas.pydata.org/docs/index.html)
- [kaggle](https://www.kaggle.com/learn/pandas)
- [cheatsheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

## Timeline

> Briefly describe what the developer can expect of his/her onboarding time wise

### Day 1

Set up your project environment by following this [guide](./PROJECT-SETUP.md).
Then get familiar with the language:

- [Basics](https://python.swaroopch.com/basics.html)
- [Operators and Expressions](https://python.swaroopch.com/op_exp.html)
- [Control Flow](https://python.swaroopch.com/control_flow.html)
- [Functions](https://python.swaroopch.com/functions.html)
- [Modules](https://python.swaroopch.com/modules.html)
- [Data Structures](https://python.swaroopch.com/data_structures.html)
- [Object Oriented Programming](https://python.swaroopch.com/oop.html)
- [Input and Output](https://python.swaroopch.com/io.html)
- [Exceptions](https://python.swaroopch.com/exceptions.html)
- [More](https://python.swaroopch.com/more.html)
Challenge yourself 💪. Do a [code challenge](https://leetcode.com/problems/two-sum/) in Python3.

### Day 2

[Django Tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/) (Part 1, 2)
[Part 1](https://docs.djangoproject.com/en/dev/intro/tutorial01/)

- Creating a project
- The development server
- Creating the Polls app
- Write your first view

[Part 2](https://docs.djangoproject.com/en/dev/intro/tutorial02/)

- Database setup
- Creating models
- Activating models
- Playing with the API
- Introducing the Django Admin

### Day 3

[Django Tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial03/) (Part 3, 4)
[Part 3](https://docs.djangoproject.com/en/dev/intro/tutorial03/)

- Writing more views
- Write views that actually do something
- Raising a 404 error
- Use the template system

[Part 4](https://docs.djangoproject.com/en/dev/intro/tutorial04/)

- Write a minimal form
- Use generic views: Less code is better

### Day 4

[Django Tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial05/) (Part 5, 6, 7)
[Part 5](https://docs.djangoproject.com/en/dev/intro/tutorial05/)

- Introducing automated testing
- Basic testing strategies
- Writing our first test
- Test a view
- When testing, more is better

Part [6](https://docs.djangoproject.com/en/dev/intro/tutorial06/) / 
[7](https://docs.djangoproject.com/en/dev/intro/tutorial07/) (Optional)

- Customize your app's look and feel
- Adding a background-image
- Customize the admin form
- Adding related objects
- Customize the admin change list
- Customize the admin look and feel
- Customize the admin index page

### Day 5

[Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/1-serialization/) (Part 1, 2)
[Part 1](https://www.django-rest-framework.org/tutorial/1-serialization/)

- Setting up a new environment
- Working with Models
- Working with Serializers
- Writing regular Django views using our Serializer
- Testing our first attempt at a Web API

[Part 2](https://www.django-rest-framework.org/tutorial/2-requests-and-responses/)

- Requests and Responses

[Part 3](https://www.django-rest-framework.org/tutorial/3-class-based-views/)

- Class Based Views
- Mixins
- Generic Class Based Views

### Day 6

[Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/) 
(Part 4, 5)
[Part 4](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/)

- Adding permissions to views
- Create a Login API
- Object level permissions
- Authenticating with the API

[Part 5](https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/)

- Adding a root API
- Hyperlinking our API
- Adding pagination

[Part 6](https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/)

- Using ViewSets
- Using routers
- Adding pagination

### Day 7
[pandas getting started](https://pandas.pydata.org/docs/getting_started/index.html)

- Installing pandas
- pandas overview
- Getting started tutorials

### Library Project

Talk to you team leader and try to design a Library project in Django.

#### Requirements

User needs to be able to manage Authors, Books, and Categories in the app.
Each Author can have many Books that he/her has written and each book can be included in multiple categories.
The User should be able to view lists of Authors and Books. The Books should be able to be filtered by Author and by 
Category

> Optional: You can also have a search bar for Authors and for Books (one for each)
The App should also include a page to view some basic statistics, like the number of Books per Author, or the number of 
> Books per Category. Feel free to add your own statistics here.

Optional: To complicate the models. A book can have many instances and users can request an instance to take home with a
requested date

## Finish

Congratulations, if you made it this far you deserve a medal, here you go 🏅