from hashlib import sha3_256
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.response import Response
import magic

from europaea import files

from .models import Storage
from .serializers import StorageSerializer


class StorageAPIViewSet(viewsets.ModelViewSet):

    queryset = Storage.objects.all()

    lookup_field = 'work'
    serializer_class = StorageSerializer

    def list(self, request):
        # admin
        return super().list(request)

    def create(self, request):
        # if amind then use uid in request
        # check user in work
        # check file head
        # create object
        # take hash
        # add time or pic
        wid = request.data['work']
        if not wid:
            return Response({"work": "must include this field"},
                            status=status.HTTP_400_BAD_REQUEST)
        work = Work.objects.get(wid=wid)
        file_dir = f'{settings.STOEAGE_DIR}/{work.project}/{work.dep}-{work.role}-{work.user}'
        files.create_if_not_exist(file_dir)
        hasher = sha3_256()
        type_id = None
        with open(file_dir, 'wb') as f:
            for i, chunk in enumerate(f.chunks()):
                if i == 0:
                    mime = magic.from_buffer(chunk, mime=True)
                    type_id = files.mime_to_type_id(mime)
                f.write(chunk)
                hasher.update(chunk)
        metadata = dict()
        if mime in ('audio/flac', 'audio/mpeg', 'aduio/wav'):
            try:
                metadata = files.get_audio_info(file_dir, mime)
            except Exception:
                return Response(
                    {"msg": "must upload a audio that contains 2 channels"},
                    status=status.HTTP_400_BAD_REQUEST)
            work.project.audio_length += metadata['duration']
        try:
            Storage.objects.create(work=work,
                                   type_id=type_id,
                                   fingerprint=hasher.digest(),
                                   metadata=metadata)
        except Exception:
            return Response(Exception.args, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().retrieve(request, work)

    def retrieve(self, request, work=None):
        # if admin or user uploaded or spec group
        return super().retrieve(request, work)

    def destroy(self, request, work=None):
        # if admin or user uploaded
        # minus time or pic
        # clear flag
        # move file
        # delete object
        return super().destroy(request, work)
