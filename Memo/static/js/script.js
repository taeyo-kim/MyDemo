// 메모장 JavaScript

// 메시지 자동 숨김
$(document).ready(function() {
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
});
