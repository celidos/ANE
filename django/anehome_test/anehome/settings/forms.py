from django import forms

class ProductChooseForm(forms.Form):
    product = forms.ChoiceField(widget=forms.Select, choices=(('1', 'First',), ('2', 'Second',)))

    def initwith(self, snap):
        self.fields["product"].choices = snap.get_product_choose_form_options()


class SiteChooseForm(forms.Form):
    site = forms.ChoiceField(widget=forms.Select, choices=(('1', 'First',), ('2', 'Second',)))

    def initwith(self, snap):
        self.fields["site"].choices = snap.get_site_choose_form_options()