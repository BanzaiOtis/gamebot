# gamebot

A simple Slack bot based on the starter code from Matt Makai at https://www.fullstackpython.com/blog/build-first-slack-bot-python.html. The bot is deployed on a free-tier Heroku dyno.

## What you need to edit/deployed
1. A [free heroku account](https://signup.heroku.com/dc?_ga=2.57799971.807021217.1505711200-711150842.1505531059)
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

NOTE: You can ignore all other setup instructions at the above Heroku CLI link (i.e. `pipenv` and `postgres`) if you don't care about running in a local environment. Otherwise you can set all that up.

## How to edit/deploy
1. Clone the GitHub repo.
2. Edit `gamebot.py` as needed (see below). If you add import statements for non-standard libraries, you need to add those libraries to `Procfile`. Just follow the format in that file and Heroku will make sure they are installed on the dyno automatically.
3. Add and commit changes: `git add .` and `git commit -m 'your commit msg here'`
4. Push changes to Heroku `git push heroku master`
5. Push changes back to the GitHub repo so we can all stay on the same page `git push origin master`

## Programming gamebot
All of the action takes place in the `handle_command()` inside `gamebot.py`. This function is passed a `command` parameter, which is everything after somebody references gamebot in Slack. So `@gamebot why is Jason so awesome?` will be parsed and `why is Jason so awesome?` will be a string in the `command` variable.

From here, it's a series of ifelse statements. If you want to add a new gamebot response, add an `elif` statement in the function, using whatever logic you want to identify the right trigger for that response, and then store your response inside the if statement in the `response` variable. 
