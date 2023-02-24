# Github Actions

[Documentation](https://docs.github.com/en/actions)

Github Actions is a feature that allows you to automate and execute different processes related to the development of your repository.

For example, you can always run all tests locally before you commit any changes to a repository or you can automate this process by using Github Actions.

Read this [page](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions) carefully as it explains the basics of how Github Actions works.

## Example for a Django project with Poetry

The following code covers how to setup a workflow in Github Actions that will run your tests.
It makes some assumptions, like the python version that it uses, poetry for package dependency and postgres for the database. However, you can infer what may be necessary according to your environment setup, as the workflow is neatly divided into steps.

### Setup

The basic setup is creating a .github folder in the root of your repository, then a workflows folder inside the .github folder, and then a django.yml file inside the workflows folder. Folder structure summary:

- .github
  - workflows
    - django.yml

### The Workflow

The workflow is defined in the django.yml file.

```yaml
# The visible name that will appear in the github interface.
name: Django Tests

# You can specify branches and other actions, but the on: push directive is one of the most basics. Everytime there's a push on any branch, this workflow will be triggered and will execute its jobs.
on: push

# You can define environment variables on a global level for the workflow.
# Here we define variables for the postgres database.
# More information on how environment variables work here: https://docs.github.com/en/actions/learn-github-actions/variables#defining-environment-variables-for-a-single-workflow
env:
  POSTGRES_DB: postgres
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres
  POSTGRES_HOST: 127.0.0.1
  POSTGRES_PORT: 15433

jobs:
  # Defines the name of the first and only job in this workflow.
  django_tests:
    # This job will run on a Ubuntu Linux runner with the Ubuntu version 22.04.
    # Because this job requires a postgres database and it uses a docker container for that purpose. The Runner must be a Linux-based OS.
    runs-on: ubuntu-22.04

    # Services are Docker containers. For this job, we are using a postgres container for the database.
    # See more information regarding the services here: https://docs.github.com/en/actions/using-containerized-services/about-service-containers
    services:
      # A name for the service.
      postgres:
        # Use postgres version 15.
        image: "postgres:15"
        # Define the variables for the postgres container.
        env:
          POSTGRES_PASSWORD: ${{env.POSTGRES_PASSWORD}}
          POSTGRES_USER: ${{env.POSTGRES_USER}}
          POSTGRES_DB: ${{env.POSTGRES_DB}}
        # Note that we didn't use ${{env.POSTGRES_PORT}} in the ports section. That's because you don't have access to the env object in the ports section.
        # Read more about this here: https://docs.github.com/en/actions/learn-github-actions/contexts#context-availability
        # TODO: If anyone knows if there's a way to use the env value in the ports, feel free to make a PR.
        ports:
          # Here we are saying that the port 5432 is exposed outwards through port 15433.
          - 15433:5432
        # These are just some optional yet recommended health checks.
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    # steps is important as it divides a job into smaller parts.
    # In this case, the job is to run django tests, and we can divide that job into smaller steps.
    steps:
      # This is the first step. The "uses" keyword specifies that this step will run v3 of the actions/checkout action. This is an action that checks out your repository onto the runner, allowing you to run scripts or other actions against your code (such as build and test tools).
      # You can read more about this action here: https://github.com/actions/checkout#readme
      - uses: actions/checkout@v3

      # You can also name your steps so that everything is clearer.
      - name: Set up Python 3.11
        # This setup-python action will do exactly what it suggests, install python in your runner's OS. Note that v4 is not the version of python, it's the version of the action.
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      # I chose to do a custom installation of poetry, but there are actions that will handle this for you. For example: https://github.com/snok/install-poetry
      - name: Install and configure Poetry
        run: |
          INSTALL_PATH="$HOME/.local"
          INSTALLATION_SCRIPT="$(mktemp)"
          VIRTUALENVS_PATH="{cache-dir}/virtualenvs/#\~/$HOME"

          curl -sSL https://install.python-poetry.org/ --output "$INSTALLATION_SCRIPT"

          POETRY_HOME=$INSTALL_PATH python3 "$INSTALLATION_SCRIPT" --yes --version="1.3.2"

          export PATH="/root/.local/bin:$PATH"

          poetry config virtualenvs.create true
          poetry config virtualenvs.in-project true
          poetry config virtualenvs.path "$VIRTUALENVS_PATH"

          echo "VENV=.venv/bin/activate" >> "$GITHUB_ENV"

      # The last step installed and configured poetry, now we can install our dependencies.
      - name: Install Dependencies
        run: |
          export PATH="/root/.local/bin:$PATH"
          poetry install --no-interaction

      # This is all very self-explanatory, everything is configured and ready for execution, simply invoke the tests.
      - name: Run Tests
        run: |
          source $VENV
          cd project_name && python manage.py test
```

### Results

Once you've commit-pushed your workflow, you can access the actions page of your repository. For example, this knowledge base, also has a continuous integration workflow defined, you can the actions page [here](https://github.com/runtimerevolution/python-knowledge-base/actions).

You can inspect each run individually and see if it's running correctly or not, or if the tests are accusing something wrong.

If there is something wrong, like an ill-defined configuration or an error in a step, you have to fix and add-commit-push, which is laborious but a necessary evil. To work around this, you can use something like [act](https://github.com/nektos/act). However, these tools aren't perfect and for example, act doesn't work with the services containers, so this workflow would never work in act; but it can be used for smaller and simple workflows because you can test locally without having to constantly commit-push every change you want to test.
