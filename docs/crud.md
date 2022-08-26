# What is CRUD?

The current state of web development almost always involves interaction with a database. That said, it is necessary to perform certain operations with it. Hence the need to use the 4 basic CRUD operations.
A great advantage of these operations is that with them alone you can create a complete web application.
### Crud Meaning
Meaning of CRUD: acronym referring to the 4 basic functions that are executed in a database model:

##### Create:
- This function allows the application to create data and save it to the database.
##### Read:
- This function allows the application to read data from the database.
##### Update
- This function allows the application to update existing data in the database.
##### Delete
- This function allows the application to delete information from the database.

#
#


# Flow (Backend)

###### Assuming you already have an project created, let's skip the create project and app steps.
#

##### Models (Example)
#
````python
class Movie(models.Model):
    name = models.CharField(max_length=250)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=200)
    starring = models.CharField(max_length=350)
    
    def __str__(self):
        return self.name
````


##### Apply models to the DB
#
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```
##### Create Super User
#
```sh
python manage.py createsuperuser
```
##### Serializer
#
````python
from rest_framework import serializers
from backend_api.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
````

##### Create ViewSet
As seen in Django Rest Framework docs [(Link)](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset), the ModelViewSet class inherits from GenericAPIView and includes implementations for various actions, by mixing in the behavior of the various mixin classes. The actions provided by the ModelViewSet class are .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy().

````python
class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
````

##### Adding authentication permissions to views (Example)
REST framework includes a number of permission classes that we can use to restrict who can access a given view. In this case the one we're looking for is IsAuthenticatedOrReadOnly, which will ensure that authenticated requests get read-write access, and unauthenticated requests get read-only access. [(Link)](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/)

````python
from rest_framework import permissions
````
````python
class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
````

##### Adding addicional validations to default ModelViewSetFunctions (Example)
This function calls the given model and get object from that if that object or model doesn't exist it raise 404 error.
````python
def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object_or_404(Movie, pk=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
````

### Extra actions with validation (Example)

Getting the Movie director by using an extra action with a different serializer
````python            
class MovieDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'director')
````  

````python            
@action(detail=True, methods=["get"], url_path='movie-director')
    def movie_director(self, request, pk=None):
        movie = self.get_object_or_404(Movie, pk=pk)
        serializer = self.get_serializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
````
Another example using actions:
````python
@action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        user = self.get_object_or_404(User, pk=pk)
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
@action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
````  

#
# Flow (Frontend - Next.js)

###### Again, assuming you already have an project created, let’s skip the create react app step.
# 
#

#### User Authentication [Source](https://nextjs.org/docs/authentication)
##### Authenticating Statically Generated Pages
Next.js automatically determines that a page is static if there are no blocking data requirements. This means the absence of getServerSideProps and getInitialProps in the page. Instead, your page can render a loading state from the server, followed by fetching the user client-side.
One advantage of this pattern is it allows pages to be served from a global CDN and preloaded using next/link. In practice, this results in a faster TTI (Time to Interactive).
Let's look at an example for a profile page. This will initially render a loading skeleton. Once the request for a user has finished, it will show the user's name:

```sh
// pages/profile.js

import useUser from '../lib/useUser'
import Layout from '../components/Layout'

const Profile = () => {
  // Fetch the user client-side
  const { user } = useUser({ redirectTo: '/login' })

  // Server-render loading state
  if (!user || user.isLoggedIn === false) {
    return <Layout>Loading...</Layout>
  }

  // Once the user request finishes, show the user
  return (
    <Layout>
      <h1>Your Profile</h1>
      <pre>{JSON.stringify(user, null, 2)}</pre>
    </Layout>
  )
}

export default Profile
```
##### Authenticating Server-Rendered Pages (Example)
#
```sh
// pages/profile.js

import withSession from '../lib/session'
import Layout from '../components/Layout'

export const getServerSideProps = withSession(async function ({ req, res }) {
  const { user } = req.session

  if (!user) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    }
  }

  return {
    props: { user },
  }
})

const Profile = ({ user }) => {
  // Show the user. No loading state is required
  return (
    <Layout>
      <h1>Your Profile</h1>
      <pre>{JSON.stringify(user, null, 2)}</pre>
    </Layout>
  )
}

export default Profile
```


#### Built-in Form validation (Example) [Source](https://nextjs.org/docs/guides/building-forms)

```sh
<form action="/send-data-here" method="post">
  <label for="roll">Roll Number</label>
  <input
    type="text"
    id="roll"
    name="roll"
    required
    minlength="10"
    maxlength="20"
  />
  <label for="name">Name:</label>
  <input type="text" id="name" name="name" required />
  <button type="submit">Submit</button>
</form>
```

With these validation checks in place, when a user tries to submit an empty field for Name, it gives an error that pops right in the form field. Similarly, a roll number can only be entered if it's 10-20 characters long.


#### JavaScript-based Form Validation (Example)
Form Validation is important to ensure that a user has submitted the correct data, in a correct format. JavaScript offers an additional level of validation along with HTML native form attributes on the client side. Developers generally prefer validating form data through JavaScript because its data processing is faster when compared to server-side validation, however front-end validation may be less secure in some scenarios as a malicious user could always send malformed data to your server.

```sh
  function validateFormWithJS() {
    const name = document.querySelector('#name').value
    const rollNumber = document.querySelector('#rollNumber').value

    if (!name) {
      alert('Please enter your name.')
      return false
    }

    if (rollNumber.length < 3) {
      toast('Roll Number should be at least 3 digits long.')
      return false
    }
  }
```


## Front-end - Back-end connection
#### Using the Axios API [Source](https://www.digitalocean.com/community/tutorials/react-axios-react)
Axios is promise-based, which gives you the ability to take advantage of JavaScript’s async and await for more readable asynchronous code. 
```sh
npm install axios
```

### Examples Axios call
````sh
import axios from 'axios';
  async getMovies(): Promise<any> {
  try {
    const {data} = await axios.get('http://127.0.0.1:8000/backend_api/movies');
    return data;
  } catch (error) {
    return { error };
  }
};

import axios from 'axios';
export default axios.create({
    baseURL: "http://127.0.0.1:8000/backend_api/movies",
    headers: {
        'Accept':'application/json',
        'Content-Type':'application/json',
    }
})
````

### Example Axios Post
````sh
async createMovie(body: { name: string; genre: string; starring: string }) {
    try {
      const {data} = await axios.post(`http://127.0.0.1:8000/backend_api/movies/`, body);
      return data;
    } catch (error) {
      const err = error as AxiosError;
      console.log('Error: ', err.message, err.response?.data);
      return null;
    }
}
````
### Example Axios Put
````sh
const res = await axios.put(`http://127.0.0.1:8000/backend_api/movies/${movie.id}`, {
    name: 'Movie edited',
    genre: 'Comedy',
    director: 'New director'
});


async updateMovie(body: { name: 'Movie edited', genre: 'Comedy', director: 'New director'}) {
    try {
      const {data} = await axios.put(`http://127.0.0.1:8000/backend_api/movies/`, body);
      return data;
    } catch (error) {
      const err = error as AxiosError;
      console.log('Error: ', err.message, err.response?.data);
      return null;
    }
}
