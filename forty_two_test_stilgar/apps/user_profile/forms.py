"""Forms for user profile app."""
from django import forms
from forty_two_test_stilgar.apps.user_profile.models import Profile
from forty_two_test_stilgar.apps.datepicker.widgets import DatePicker
from forty_two_test_stilgar.apps.progress_file_input.widgets import \
        ProgressFileInput


class ProfileEditForm(forms.ModelForm):
    """Profile edit form."""
    # pylint: disable=W0232,R0903,C0111
    class Meta:
        model = Profile
        widgets = {
            'date_of_birth': DatePicker(),
            'image': ProgressFileInput(attrs={'autocomplete': 'off'}),
        }

    # pylint: disable=W0232,R0903,C0111
    class Media:
        js = (
            'user_profile/jquery.form.js',
            'user_profile/edit-ajax.js',
        )

    def __init__(self, *args, **kwargs):
        """Conditionally reversing order of fields."""
        reverse_field_order = kwargs.get('reverse_field_order', False)
        try:
            del kwargs['reverse_field_order']
        except KeyError:
            pass
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        if reverse_field_order:
            #FIXME: get DRY.
            first_column = self.fields.keyOrder[:4]
            second_column = self.fields.keyOrder[4:]
            first_column.reverse()
            second_column.reverse()
            self.fields.keyOrder = first_column + second_column

    def save(self, commit=True, stored_image=None):
        """Override for saving stored image."""
        profile = super(ProfileEditForm, self).save(commit=False)
        if stored_image:
            profile.image = stored_image
        if commit:
            profile.save()
        return profile

    image_preview_id = forms.CharField(required=False,
                                       widget=forms.HiddenInput)
    """Hidden field to store ID of uploaded image for next preview/save."""
    forget_unsaved_image = forms.BooleanField(required=False,
                                              label='Forget unsaved image')
    """Checkbox for dropping uploaded and currently previewed image."""
