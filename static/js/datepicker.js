$(document).ready(function () {
    // Получаем ширину input
    var inputWidth = $('#datepicker').outerWidth();
    $('#datepicker').datepicker({
        dateFormat: 'dd-mm-yy',
        beforeShow: function (input, inst) {
            // Скрываем dropdown-container при открытии datepicker
            $('#dropdown-container').css('display', 'none');
        },
        onSelect: function (dateText, inst) {
            $(this).val(dateText);
        }
    });
});