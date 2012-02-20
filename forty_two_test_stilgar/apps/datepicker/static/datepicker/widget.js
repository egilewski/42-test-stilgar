jQuery.noConflict();
jQuery(document).ready(function($) {
    $('input[data-datepicker-regional]').each(function(index) {
        input = $(this);
        locale = input.data('datepicker-regional')
        format = input.data('datepicker-dateformat')
        input.datepicker(
            $.extend({}, $.datepicker.regional[locale], {dateFormat: format})
        );
    });
});
