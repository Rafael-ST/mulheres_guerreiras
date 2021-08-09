import tempfile

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def export_pdf(context, file_name, html_file, base_url):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(file_name)
    response['Content-Transfer-Encoding'] = 'binary'

    html_string = render_to_string(html_file, context)
    html = HTML(string=html_string, base_url=base_url)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def try_or(func, default=None, expected_exc=(Exception,)):
    try:
        return func()
    except expected_exc:
        return default