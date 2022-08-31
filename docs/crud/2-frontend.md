[Index](0-index.md)
# Flow (Frontend - Next.js)

#### Again, assuming you already have an project created, let’s skip the create react app step.
#

# Authentication 
[Source](https://nextjs.org/docs/authentication)
## Authenticating Statically Generated Pages
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

# Validation
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


## JavaScript-based Form Validation (Example)
Form Validation is important to ensure that a user has submitted the correct data, in a correct format. JavaScript offers an additional level of validation along with HTML native form attributes on the client side. Developers generally prefer validating form data through JavaScript because its data processing is faster when compared to server-side validation, however front-end validation may be less secure in some scenarios as a malicious user could always send malformed data to your server.

```tsx
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
# TypeScript
## Creating TypeScript types in Next.js [Source](https://blog.logrocket.com/using-next-js-with-typescript/)

You can create types for anything in your application, including prop types, API responses, arguments for your utility functions, and even properties of your global state.

The interface below reflects the shape of a Post object. It expects id, title, and body properties.
```tsx
// types/index.ts

export interface IPost {
  id: number
  title: string
  body: string
}
```

```tsx
// components/AddPost.tsx

import * as React from 'react'
import { IPost } from '../types'

type Props = {
  savePost: (e: React.FormEvent, formData: IPost) => void
}

const AddPost: React.FC<Props> = ({ savePost }) => {
  const [formData, setFormData] = React.useState<IPost>()

  const handleForm = (e: React.FormEvent<HTMLInputElement>): void => {
    setFormData({
      ...formData,
      [e.currentTarget.id]: e.currentTarget.value,
    })
  }

  return (
    <form className='Form' onSubmit={(e) => savePost(e, formData)}>
      <div>
        <div className='Form--field'>
          <label htmlFor='name'>Title</label>
          <input onChange={handleForm} type='text' id='title' />
        </div>
        <div className='Form--field'>
          <label htmlFor='body'>Description</label>
          <input onChange={handleForm} type='text' id='body' />
        </div>
      </div>
      <button
        className='Form__button'
        disabled={formData === undefined ? true : false}
      >
        Add Post
      </button>
    </form>
  )
}

export default AddPost
```

# Responses
## Response Types
Another thing you might be using is the API routes from Next.js.
```tsx
export default function handler(req, res) {
  res.status(200).json({ name: 'John Doe' });
}
```
We can typecast the req and res to be types like this:
```tsx
import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ name: 'John Doe' });
}
```


# Axios
## Front-end - Back-end connection
#### Using the Axios API [Source](https://www.digitalocean.com/community/tutorials/react-axios-react)
Axios is promise-based, which gives you the ability to take advantage of JavaScript’s async and await for more readable asynchronous code. 
```sh
npm install axios
```


### Response type conversion

Sometimes the data coming from the API has values that may break our application. Due to this fact you should always parse the response. For example:
```js
  baseUrl = "https://jsonplaceholder.typicode.com";
  async getUser(id){
    try{
      const req = await fetch(`${this.baseUrl}/users/${id}`);
      this._handleRequest(req);
      const user = await req.json();
      return { email: user.email, name: user.name }
    } catch(e){
      throw e;
    }
  }
```

### Examples Axios call
````tsx
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
````tsx
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
````tsx
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
````

### Making Http GET requests with Axios in TypeScript
```tsx
// servies/types

type User = {
  id: number;
  email: string;
  first_name: string;
};

type GetUsersResponse = {
  data: User[];
};
```

```tsx
import axios from 'axios';
import { User, GetUsersResponse } from '../services/types'

async function getUsers() {
  try {
    const { data, status } = await axios.get<GetUsersResponse>(
      'https://reqres.in/api/users',
      {
        headers: {
          Accept: 'application/json',
        },
      },
    );

    console.log(JSON.stringify(data, null, 4));

    console.log('response status is: ', status);

    return data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log('error message: ', error.message);
      return error.message;
    } else {
      console.log('unexpected error: ', error);
      return 'An unexpected error occurred';
    }
  }
}

getUsers();
```