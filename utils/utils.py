import sys
import threading

import PIL
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail


class Item():
    def __init__(self, id, descricao):
        self.id = id
        self.descricao = descricao

    def __str__(self):
        return self.descricao


class ItemGroup():
    def __init__(self, label, listItems):
        self.label = label
        self.listItems = listItems

    def __str__(self):
        return self.label


def resizeImage(imageField):
    if imageField:
        try:
            im = Image.open(imageField)
            output = BytesIO()

            factor = 500
            if im.width > im.height:
                im = im.resize((int(round(factor*(im.width/im.height))), factor))
            else:
                im = im.resize((factor, int(round(factor*(im.height/im.width)))))

            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB")
            im.save(output, format='JPEG', quality=80)
            output.seek(0)
            return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % imageField.name.split('.')[0], 'image/jpeg',
                                            sys.getsizeof(output), None)
        except PIL.UnidentifiedImageError as e:
            return imageField
        return


def rec_send_email(email, subject, message):
    r = send_mail(str(subject),
              str(message),
              'mulherempreendedora@sde.fortaleza.ce.gov.br',
              [email],
              fail_silently=False)
    print('rec_send_email: {}'.format(r))


def send_email_in_thread(email, subject, message):
    t1 = threading.Thread(target=rec_send_email, args=[email, subject, message])
    t1.start()


def mascarar_email(email):
    emails = email.split(';')
    emails_final= []
    for e in emails:
        em = e.strip().split('@')
        if len(em) == 2:
            first = '{}****{}'.format(em[0][:2], em[0][-3:])
            em = '{}@{}'.format(first, em[1])
        emails_final.append(em)
    return '; '.join(emails_final)
