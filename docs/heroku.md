destroy app  > heroku apps:destroy --app <app name>

heroku login
heroku create <your-app-name>
heroku stack:set container --app <your-app-name>
git push heroku main
heroku ps:scale web=1 --app <your-app-name> 


heroku run python manage.py migrate --app <app name>
heroku open --app <app name>
