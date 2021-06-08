from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('poll', '0001_initial')]
    operations = [migrations.AddField(model_name='useranswer', name=
        'domain', field=models.CharField(default='', editable=False,
        max_length=255)), migrations.AddField(model_name='useranswer', name
        ='ip', field=models.CharField(db_index=True, default='', editable=
        False, max_length=40))]
