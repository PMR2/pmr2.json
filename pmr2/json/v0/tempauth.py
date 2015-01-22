from pmr2.tempauth.browser import ContextTempAuthRequestForm


class VndContextTempAuthRequestForm(ContextTempAuthRequestForm):
    content_type = 'application/vnd.physiome.pmr2.json.0'
