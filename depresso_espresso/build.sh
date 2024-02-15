cd frontend
npm run build
cd ..
rm -rf staticfiles
python manage.py collectstatic --noinput
python manage.py runserver