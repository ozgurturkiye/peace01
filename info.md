# 📖 How to use Fixtures in Django 📖
> For detailed information: [Serializing Django objects](https://docs.djangoproject.com/en/4.2/topics/serialization/)

# Dump data by using `dumpdata` command:

`django-admin dumpdata [app_label[.ModelName] [app_label[.ModelName] ...]]`

Dump all data in database:

```python manage.py dumpdata > mydata.json```

Dump only selected model data:

```python manage.py dumpdata words.English words.Turkish > mydata.json```

Specifies the number of indentation spaces:

```python manage.py dumpdata --indent 4 > mydata.json```

# Exclude app.model and app
```python manage.py dumpdata --exclude admin.logentry --exclude auth > mydata.json```

```python manage.py dumpdata --exclude auth.permission > mydata.json```

# Load data
```python manage.py loaddata mydata.json```

```./manage.py loaddata mydata.json```

# Using Yaml
> First you MUST Install PyYAML: 
> 
> ```python -m pip install PyYAML```

Dump data that serialized as YAML format:

```python manage.py dumpdata words.English --format yaml > mydata.yaml```

Load data from YAML file:

```python manage.py loaddata mydata.yaml```

# Using JSONL
> JSONL stands for JSON Lines. With this format, objects are separated by new lines, and each line contains a valid JSON object. JSONL serialized data looks like this:

```{"pk": "4b678b301dfd8a4e0dad910de3ae245b", "model": "sessions.session", "fields": {...}}```

```python manage.py dumpdata words.WordBox --format jsonl > mydata.jsonl```
 
# Using XML
```python manage.py dumpdata words.WordBox --format xml --indent 4 > mydata.xml```

