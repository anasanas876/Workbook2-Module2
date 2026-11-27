
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate


#!/usr/bin/env bash
set -o errexit
# I have temporary added this data for testing
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
from django.apps import apps
M = {m.__name__: m for m in apps.get_models()}
c, _ = M['Company'].objects.get_or_create(company_name='Google')
w, _ = M['WorkSpace'].objects.get_or_create(name='Engineering Hub')
r, _ = M['Room'].objects.get_or_create(room_name='General Chat', workspace=w)
u, cr = M['User'].objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'role': 'admin', 'company': c, 'workspace': w, 'room': r, 'is_staff': True, 'is_superuser': True})
if cr: u.set_password('admin123'); u.save()
e, cr2 = M['User'].objects.get_or_create(username='employee1', defaults={'email': 'emp1@example.com', 'role': 'employee', 'company': c, 'workspace': w, 'room': r})
if cr2: e.set_password('pass1234'); e.save()
print('SEED COMPLETE')
"
