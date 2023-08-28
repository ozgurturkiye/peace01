Fixture

# Dump data
```python manage.py dumpdata words.English words.Turkish --indent 4 > words/fixtures/mydata.json```

# Load data
python manage.py loaddata mydata.json


./manage.py loaddata user.json


# Dump all data
python manage.py dumpdata > alldata.json
python manage.py dumpdata --indent 4 > alldata.json

# Exclude app.model and app
python manage.py dumpdata --exclude admin.logentry --exclude auth --indent 4 > example.json

python manage.py dumpdata --exclude auth.permission > example.json

# Using Yaml
First -> ```python -m pip install PyYAML```

python manage.py dumpdata words.English words.Turkish --format yaml> mydata.yaml

python manage.py loaddata mydata.yaml