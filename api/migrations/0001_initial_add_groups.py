from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    def insert_groups(apps, schema_editor):
        group = apps.get_model('auth', 'Group')
        permissions = apps.get_model('auth', 'Permission')

        administrador_surtidor = group.objects.create(name='Administrador de Surtidor')
        administrador_refineria = group.objects.create(name='Administrador de Refinería')
        administrador_accesos = group.objects.create(name='Administrador de Accesos')
        vendedor = group.objects.create(name='Vendedor')
        chofer = group.objects.create(name='Chofer')

        # Add permissions to groups
        add_user = permissions.objects.get(codename='add_user')
        change_user = permissions.objects.get(codename='change_user')
        delete_user = permissions.objects.get(codename='delete_user')
        view_user = permissions.objects.get(codename='view_user')

        administrador_accesos_permissions = [add_user, change_user, delete_user, view_user]
        administrador_accesos.permissions.set(administrador_accesos_permissions)

    operations = [
        migrations.RunPython(insert_groups)
    ]