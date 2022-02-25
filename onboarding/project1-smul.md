### Smul Project

Talk to you team leader and try to design a URL Shortener project in Django. (There is already a project made in Django but we want you to try to solve this one by yourself. You can do it 🚀)

#### Requirements

User needs to be able to go to a webpage input a big url into a form and retrieve a *smul* url.

If clicked, this url should redirect the user to the original url.

If user inputs the same big url multiple times the *smul* url should always be the same.

#### Steps (optional)

If you have an idea already of how you going to do it don't bother reading this but if you want some ~~help~~ inspiration here are some steps to follow.

- create a django project from scratch or add to your existing one
- create a django app called `smul`
- create endpoints one for your home view and another for url redirection
  - the home view is going to serve our homepage html with a form to shorten a url
  - the redirection view is going to be a dynamic endpoint with an id/code as the url path where we are going to redirect them to the original url
- create a form in django
  - we only need one input field for the url
- create home view html template
  - create a GET handler in the home view and render the html template with the form
- create a model to map out your big urls to your *smul* urls
- create a way to generate a unique id/code for the *smul* urls
- create a POST handler in the home view to retrieve the form data
  - here you want to check if the big url is already in the database
  - if it is return the *smul* url
  - else create the *smul* url with the id/code generation tool that you created and save if to the database
  - return the *smul* url either in a new html template or reuse the home page one
- finally complete your redirection endpoint by fetching the big url from the database and redirecting them to that url