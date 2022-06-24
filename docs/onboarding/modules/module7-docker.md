# Module 7 - Docker

## References

- [Docker overview](https://docs.docker.com/get-started/overview/)
  - [Get Docker](https://docs.docker.com/get-docker/)
  - [Get started](https://docs.docker.com/get-started/)
  - [Get started - Official Docker Video Tutorial](https://www.youtube.com/watch?v=iqqDU2crIEQ)
  - [Docker documentation](https://docs.docker.com/reference/)
  
## Timeline

### Day 1
[Part 1: Getting started](https://docs.docker.com/get-started/)

- Download and installation
- The Docker Dashboard
- What is a container?

[Part 2: Sample application](https://docs.docker.com/get-started/02_our_app/)

- Sample application (Node.js app)
- Building app's container image
- Starting an app container

[Part 3: Updating the application](https://docs.docker.com/get-started/03_updating_app/)

- Source code update
- Removing/Starting a container 

[Part 4: Sharing the application](https://docs.docker.com/get-started/04_sharing_app/) (Optional?)

- Creating a repo
- Pushing the image
- Running the image on a new instance

[Part 5: Persisting the DB](https://docs.docker.com/get-started/05_persisting_data/)

- Container's filesystem
- Container volumes
- Persisting db data

[Part 6: Using bind mounts](https://docs.docker.com/get-started/06_bind_mounts/)

- Starting a dev-mode container

[Part 7: Multi container apps](https://docs.docker.com/get-started/07_multi_container/)

- Container networking
- Starting DB container image (MySQL)
- Connecting to DB container image
- Connecting app to DB container image

[Part 8: Using Docker Compose](https://docs.docker.com/get-started/08_using_compose/)

- Installing Docker Composev
- Creating Docker Compose file
- Defining app and DB services
- Running the application stack

[Part 9: Image-building best practices](https://docs.docker.com/get-started/09_image_best/) (Optional)

- Security scanning
- Image layering
- Layer caching
- Multi-stage builds


## Possible troubleshooting (M1 related)
[Using Bind Mounts: error Couldn't find a package.json file in "/app" #76](https://github.com/docker/getting-started/issues/76)

[docker build command fails on yarn install step with error "gyp ERR! find Python" #124](https://github.com/docker/getting-started/issues/124)

## Useful tutorials/links

[Quickstart: Compose and Django](https://docs.docker.com/samples/django/)

[Introduction to Docker](https://docker-curriculum.com/#introduction)

[Docker for Beginners](https://docker-curriculum.com/)

[Postgres up and running in less than 3 minutes with docker-compose](https://dev.to/raphaelmansuy/postgres-up-and-running-in-less-than-3-minutes-with-docker-compose-1odd)

[How to Dockerize a Django web app elegantly](https://faun.pub/tech-edition-how-to-dockerize-a-django-web-app-elegantly-924c0b83575d)

[Dockerizing a Django + MySQL project](https://dev.to/foadlind/dockerizing-a-django-mysql-project-g4m)