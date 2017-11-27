'''
Created on 5 de jan de 2016

@author: Diego
'''

import cgi

from django.http.response import HttpResponse
from django.template import Context
from django.template.loader import get_template

import cStringIO as StringIO
import ho.pisa as pisa


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % 'relatorio.pdf'
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))