from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name='Answer', fields=[('id',
        models.AutoField(auto_created=True, primary_key=True, serialize=
        False, verbose_name='ID')), ('answer', models.CharField(max_length=
        255))]), migrations.CreateModel(name='Category', fields=[('id',
        models.AutoField(auto_created=True, primary_key=True, serialize=
        False, verbose_name='ID')), ('name', models.CharField(max_length=22
        )), ('display_all', models.BooleanField(default=False)), (
        'display_factor', models.PositiveSmallIntegerField(blank=True, null
        =True))], options={'verbose_name_plural': 'Categories'}),
        migrations.CreateModel(name='Question', fields=[('id', models.
        AutoField(auto_created=True, primary_key=True, serialize=False,
        verbose_name='ID')), ('question', models.CharField(max_length=255,
        verbose_name='Question')), ('is_active', models.BooleanField(
        default=False, verbose_name='is active')), ('type', models.
        CharField(choices=[('Multiplechoice', 'Multiplechoice'), (
        'Singlechoice', 'Singlechoice'), ('Textfield', 'Textfield'), (
        'Scala', 'Scala')], default='Textfield', max_length=20,
        verbose_name='Type')), ('number_range_end', models.IntegerField(
        default=0, help_text='Only required for Scala-Fields. ')), ('count',
        models.PositiveIntegerField(default=0)), ('description', models.
        CharField(blank=True, help_text=
        'Only required if you want to display a description.', max_length=
        255, null=True)), ('required', models.BooleanField(default=False)),
        ('answers', models.ManyToManyField(blank=True, to='poll.Answer')),
        ('category', models.ForeignKey(on_delete=django.db.models.deletion.
        CASCADE, to='poll.Category', verbose_name='Category'))]),
        migrations.CreateModel(name='UserAnswer', fields=[('id', models.
        AutoField(auto_created=True, primary_key=True, serialize=False,
        verbose_name='ID')), ('answer', models.CharField(max_length=255)),
        ('question', models.ForeignKey(on_delete=django.db.models.deletion.
        PROTECT, to='poll.Question'))]), migrations.CreateModel(name=
        'QuestionDashboard', fields=[], options={'proxy': True, 'indexes':
        []}, bases=('poll.question',))]
