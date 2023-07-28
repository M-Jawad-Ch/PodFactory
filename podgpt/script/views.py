from django.shortcuts import render
from .models import Script

import json


def view_script(request, pk):
    script = Script.objects.get(pk=pk)

    return render(request, 'episode.html', {
        'title': script.title,
        'content': [section for section in json.loads(script.contents)]
    })
