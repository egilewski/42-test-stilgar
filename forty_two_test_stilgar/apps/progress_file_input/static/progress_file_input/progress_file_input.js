jQuery.noConflict();
jQuery(document).ready(function($) {
    var progress_container_list = $('.upload-progress');
    progress_container_list.each(function() {
        var form = $(this).parents('form');
        //form.find('.upload-progress .status').html('Test');
        form.uploadProgress({
            // Scripts locations for Safari.
            jqueryPath: form.find('.upload-progress').data('jquery-path'),
            uploadProgressPath: form.find('.upload-progress').data(
                    'upload-progress-path'),

            start: function() {
                form.find('.upload-progress .status').html('');
                form.find('.upload-progress').show();
            },
            uploading: function(upload) {
                form.find('.upload-progress .status').html(
                        'Upload progress: ' + upload.percents + '%');
            },
            // Can be run multiple times if there where more the one status
            // requests with "done" response.
            success: function() {
                form.find('.upload-progress .status').html('Upload complete');
            },
            error: function() {
                form.find('.upload-progress .status').html('Upload failed');
            },

            // Selector or element that will be updated.
            // FIXME: doesn't work.
            progressBar: '#' + form.find('.upload-progress .status')
                    .find('.bar').attr('id'),
            // Progress reports url.
            progressUrl: $(this).data('progress-url'),
            interval: 2000,
        });
    });
});
