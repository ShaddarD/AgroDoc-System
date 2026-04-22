class MasterApplicationService:

    def create(self, application_ids):

        apps = Application.objects.filter(uuid__in=application_ids)

        self._validate(apps)

        master = Application.objects.create(
            application_type_code=Application.TYPE_COK_SPLIT,
        )

        apps.update(master_application=master)

        return master

    def _validate(self, apps):

        senders = {a.terminal_id for a in apps}

        if len(senders) > 1:
            raise ValidationError('Разные отправители')