from django import forms


class ShippingForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address_line1 = forms.CharField(max_length=255, label="Address line 1")
    address_line2 = forms.CharField(max_length=255, required=False, label="Address line 2")
    city = forms.CharField(max_length=100)
    postcode = forms.CharField(max_length=20)
    country = forms.CharField(max_length=100, initial="United Kingdom")

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if len(phone) < 8:
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone
