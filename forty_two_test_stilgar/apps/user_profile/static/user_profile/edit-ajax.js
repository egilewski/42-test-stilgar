jQuery.noConflict();
jQuery(document).ready(function($) {
    var form = $('#profile-edit-form');
    var temprarly_disabled_fields;
    form.ajaxForm({
        dataType: 'json',

        beforeSend: function(xhr, options) {
            temprarly_disabled_fields = form.find(':enabled');
            temprarly_disabled_fields.prop('disabled', true);
        },

        success: function(data) {
            // Change form accordingly to returned data.
            if (data.image_preview) {
                $('#image-preview').show()
                        .find('img').attr('src', data.image_preview);
            }
            else {
                $('#image-preview').hide()
                        .find('img').attr('src', '');
            }
            if (data.error_note) {
                $('#error-note').html(data.error_note);
                $('#error-note').show();
                for (var field in data.form_errors) {
                    $('#field-' + field + '-wrapper .field-error').html(
                            '<div>' +
                            data.form_errors[field].join('</div><div>') +
                            '</div>');
                }
            }
            else {
                $('#error-note').hide();
                $('#error-note').html('');
                $('.field-wrapper .field-error').html('');
            }
            $('input#id_forget_unsaved_image').prop('checked', false);
            // Store preview_image_id in hidden input
            // for next previews and saving.
            $('#id_image_preview_id').val(data.image_preview_id);

            // Enable fields in image selector disabled during submit.
            // Need to do it now because they will be overrided and new elements
            // won't be in the list.
            var elements_to_be_removed = temprarly_disabled_fields
                    .filter('#field-image-wrapper .field *');
            elements_to_be_removed.prop('disabled', false);
            temprarly_disabled_fields =
                    temprarly_disabled_fields.not(elements_to_be_removed);
            // Clear file input.
            var file_field_wrapper = $('#field-image-wrapper .input-wrapper');
            file_field_wrapper.html(file_field_wrapper.html());
            // And disable new fields and add them to the list,
            // in case of some long process added after that.
            var elements_newly_created =
                    $('#field-image-wrapper .field :enabled');
            elements_newly_created.prop('disabled', true);
            temprarly_disabled_fields =
                    temprarly_disabled_fields.add(elements_newly_created);

            // Current image in ClearableFileInput.
            if (data.current_image_name)
                $('#field-image-wrapper .field .current-value').show()
                        .find('a')
                        .prop('href', data.current_image_url)
                        .text(data.current_image_name);
            else
                $('#field-image-wrapper .field .current-value').hide();
        },

        complete: function(response, status) {
            // Enable fields disabled during submit.
            temprarly_disabled_fields.prop('disabled', false);
            // File input had been cleared by recreating, so find it manually.
            //form.find(':enabled').prop('disabled', false);
        },
    });
});
