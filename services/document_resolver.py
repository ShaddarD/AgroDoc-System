class DocumentResolver:

    def resolve(self, app):

        docs = ['doc1', 'doc2', 'doc3']

        if app.application_type_code != 'vnikkr':
            docs.append('quality')

        if app.master_application_id:
            docs.append('split')

        if app.ikr_number:
            docs.append('ikr')

        if app.is_on_behalf:
            docs.append('on_behalf')

        if app.need_color_letter:
            docs.append('color')

        return docs