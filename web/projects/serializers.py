import re

from rest_framework import serializers

from europaea.choices import DEPARTMENT
from europaea.auto_title import fetch_title
from projects.models import Project


class ProjectNSerializer(serializers.ModelSerializer):
    eng = serializers.BooleanField(default=False, write_only=True)
    info = serializers.CharField(write_only=True)

    class Meta:
        model = Project
        fields = ('pid', 'info', 'eng', 'note')
        read_only_fields = ('pid',)

    def validate(self, attrs):
        ino_or_url, title = attrs.pop('info').split(';')
        ino_or_url = ino_or_url.lower()
        if title:
            attrs['title'], attrs['doc_url'] = title, ino_or_url
            return attrs
        primary = re.match('^(?:cn-)?([0-9]{3,4})(?:(-j)|(-ex))?$', ino_or_url)
        if primary:
            # SCP-000 SCP-000-J SCP-000-EX
            # SCP-CN-000 SCP-CN-000-J SCP-CN-000-EX
            pg = 1
            if '-j' in ino_or_url:
                url = 'joke-scps'
            elif '-ex' in ino_or_url:
                url = 'scp-ex'
            else:
                pg = int(int(primary.group(1)) / 1000) + 1
                url = 'scp-series'
            url += '-cn' if 'cn-' in ino_or_url else ''
            url += f'-{pg}/' if pg != 1 else '/'
            attrs['doc_url'] = f'scp-{ino_or_url}/'
        elif re.match('^[0-9]{3,4}-jp(-j)?$', ino_or_url):
            url = 'scp-international/'
            attrs['doc_url'] = f'scp-{ino_or_url}/'
        else:
            url = ino_or_url
            url += '' if '/' in url else '/'
            attrs['doc_url'] = url
        attrs['title'] = fetch_title(attrs['doc_url'], url, attrs['eng'])
        return attrs

    def create(self, validated_data):
        eng = validated_data.pop('eng')
        project = super().create(validated_data)
        project.progress.roles = dict([
            ('60', []),
            ('70', ['FA']),
            ] + [('50', ['FA']) if not eng else('51', ['FA'])])
        project.progress.save()
        return project


class ProjectUSerializer(serializers.Serializer):
    roles = serializers.ListField(child=serializers.CharField(),
                                  write_only=True)
    dep = serializers.ChoiceField(choices=DEPARTMENT, write_only=True)

    def validate(self, attrs):
        # TODO check if user joined if user in group 60, ignore
        if attrs['dep'] == 60:
            if 60 in attrs['user'].groups or 70 in attrs['user'].groups:
                return attrs
        elif attrs['dep'] in attrs['user'].groups:
            return attrs
        raise serializers.ValidationError(
            f'editing denied for this dep({data["dep"]})')

    def perform_update(self, instance, validated_data):
        instance.progress.roles[validated_data['dep']] = validated_data['roles']
        if validated_data['roles']:
            setattr(instance.progress, f'd{validated_data["dep"]/10}_state', 1)
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = fields
        depth = 1
