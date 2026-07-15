#run redis
sudo service redis-server start


# start djano server
cd backend
source .venv/bin/activate
python manage.py runserver &
cd ..

# start react server
cd frontend
npm start &
cd ..