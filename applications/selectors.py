from .models import Application


def get_application_queryset():
    return Application.objects.select_related(
        'status',
        'applicant_counterparty',
        'applicant_account',
        'terminal',
        'product',
        'power_of_attorney',
        'master_application',
    )


class ApplicationDocumentResolver:
    DOC_FORM_370_1 = 'form_370_1'
    DOC_FORM_370_2 = 'form_370_2'
    DOC_FORM_370_3 = 'form_370_3'
    DOC_COK_QUALITY = 'cok_quality'
    DOC_SPLIT = 'split_by_receivers'
    DOC_IKR = 'ikr_letter'
    DOC_ON_BEHALF = 'on_behalf_letter'
    DOC_COLOR = 'color_letter'

    def resolve(self, application: Application) -> list[str]:
        docs = [self.DOC_FORM_370_1, self.DOC_FORM_370_2, self.DOC_FORM_370_3]

        if application.application_type_code in (
            Application.TYPE_COK_SINGLE,
            Application.TYPE_COK_SPLIT,
        ):
            docs.append(self.DOC_COK_QUALITY)

        if application.application_type_code == Application.TYPE_COK_SPLIT:
            docs.append(self.DOC_SPLIT)

        if application.ikr_number and application.ikr_date:
            docs.append(self.DOC_IKR)

        if application.is_on_behalf:
            docs.append(self.DOC_ON_BEHALF)

        if application.need_color_letter:
            docs.append(self.DOC_COLOR)

        return docs
