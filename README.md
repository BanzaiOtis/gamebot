# gamebot

A simple Slack bot based on the starter code from Matt Makai at https://www.fullstackpython.com/blog/build-first-slack-bot-python.html. The bot is deployed on a free-tier Heroku dyno. This is a work in progress. I've done my best to explain what I've done below, and how to replicate it.

NOTE: Most of these instructions assume a pre-existing Heroku app linked to this GitHub account, and a pre-existing Slack bot. If this isn't the case, see the bottom-most section for additional setup instructions.

NOTE2: This is for a Slack *bot*, not a Slack *app*. They're different, which took me a while to figure out. A bot can be wrapped in an app, but this repo is a standalone bot.

## What you need to edit/deploy
At bare minimum, you only need to clone this repo. When code is pushed back to the master branch, Heroku automatically redeploys the app with the new code.

If you want more flexibility, such as being able to start/stop the app or having Heroku automatically run the app locally in an identical environment, you need to install the Heroku CLI:
1. Get a [free heroku account](https://signup.heroku.com/dc?_ga=2.57799971.807021217.1505711200-711150842.1505531059)
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

NOTE: You can ignore all other setup instructions at the above Heroku CLI link (i.e. `pipenv` and `postgres`) if you don't care about running in a local environment. Otherwise you can set all that up.

## How to edit/deploy
1. Clone the GitHub repo.
2. Edit `gamebot.py` as needed (see below). If you add import statements for non-standard libraries, you need to add those libraries to `Procfile`. Just follow the format in that file and Heroku will make sure they are installed on the dyno automatically.
3. Add and commit changes: `git add .` and `git commit -m 'your commit msg here'`
4. Push changes back to the GitHub repo `git push origin master`. Heroku will automatically redeploy the app.

## Programming gamebot
All of the action takes place in the `handle_command()` inside `gamebot.py`. This function is passed a `command` parameter, which is everything after somebody references gamebot in Slack. So `@gamebot why is Jason so awesome?` will be parsed and `why is Jason so awesome?` will be a string in the `command` variable.

Currently, it's a series of ifelse statements. If you want to add a new gamebot response, add an `elif` statement in the function, using whatever logic you want to identify the right trigger for that response, and then store your response inside the if statement in the `response` variable.

More abstractly, `handle_command` will receive a command, and then the bot needs to issue a postMessage api call of this form to reply in Slack: `slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)`. It doesn't matter how we get from command to postMessage.

## Running locally
To run the bot from your local machine:
1. Set two environmental variables, `BOT_ID` and `SLACK_BOT_TOKEN`. You can retrieve the environmental variable values from Heroku using `heroku config`.
2. Make sure all of the packages in `Pipfile` are installed locally.
3. Run `python gamebot.py`.

NOTE: you can stop the gamebot app in Heroku using `heroku ps:stop "gamebotapp"` before you run local testing and the restart it with `heroku ps:restart "gamebotapp"` after to start. It will automatically start after a push to the heroku repo though. To get a list of current dynos and their status, use `heroku ps`.

# Additional Setup Instructions for Heroku and Slack
These instructions are only needed if creating a new bot and/or Heroku app.
## Creating a new Slack bot
1. Go to the [Slack API bot page](https://api.slack.com/bot-users) and select [creating a new bot user](https://my.slack.com/services/new/bot).
2. Follow directions and make note of your bot api token. You'll need it in setting up a Heroku App (see below) or setting environmental variables in the local environment.

## Setting up your own Heroku App
The above instructions assume you are using a pre-existing Heroku app that is synched with the this GitHub repo. If you would like to duplicate the repo and use it in a different Heroku app:
1. Install Heroku CLI as described in the relevant link above.
2. Clone this repo.
3. Navigate to the repo directory. e.g. `cd ./gamebot`
4. `heroku create <new_app_name>`
5. Set your Slack bot token environmental variable `heroku config:set SLACK_BOT_TOKEN=your_slackbot_token`
6. Edit `print_bot_id.py` by substituting your bot name for the `BOT_NAME` variable and run `python print_bot_id.py` in terminal to obtain your bot ID number.
7. Set bot ID environmental variable `heroku config:set BOT_ID=your_bot_id`
8. From this point you can either push to Heroku to deploy the app `git push heroku master` or configure Heroku to deploy from your GitHub repo (or other options). To do the latter, go to [your app dashboard](https://dashboard.heroku.com/apps), select the app, and choose the appropriate deployment method under the deploy tab. Then push your code to the deployment source you chose, for example `git push origin master` to GitHub.
