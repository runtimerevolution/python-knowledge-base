# DataDog boilerplate

This boilerplate is intended for development use only. You should not deploy this to production!

## Instaling

You will need:

 - A funtioning python environment with pipenv, for the purpose of this boilerplate we are using v3.9.6
 - The DataDog macos agent:
    - `DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"`

## Configuring

 - Once you have installed the requirements you need to configure your agent:
    - Run the DataDog agent
    - In the menu bar select "Open Web UI" [Menu Bar Interface](./images/datadog-agent.png)
    - Go to settings [reference](./images/datadog-settings.png), and add the following:
        - `logs_enabled: true`
        - `apm_non_local_traffic: true`
    - Go to Checks [ref.](./images/datadog-checks-config.png)
    - Add a new check for **python** [ref.](./images/datadog-add-check.png)
    - Change the content of `conf.yml` to your needs
        - note that you can have multiple entries in this file
    - Paste the contens of `conf.yml` into you **python** Check and Save
    - Restart your agent

## Testing / Running

You should now be able to test your DataDog logging ability locally, for that, you just need to run `run.py`.

> Don't forget to activate your `pipenv` environment and install the dependencies