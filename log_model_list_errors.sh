#!/bin/sh

cd forty_two_test_stilgar >/dev/null 2>&1
python manage.py list_models 2>../`date +%F`.dat
result=$?
cd - >/dev/null 2>&1
exit $result
