// 메모장 JavaScript

$(document).ready(function() {
    // 메시지 자동 숨김
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // 삭제 확인 모달
    $('a[href*="delete"]').not('form a').on('click', function(e) {
        if (!$(this).closest('form').length) {
            const confirmed = confirm('정말로 삭제하시겠습니까?');
            if (!confirmed) {
                e.preventDefault();
            }
        }
    });
    
    // 폼 제출 시 로딩 표시
    $('form').on('submit', function() {
        const submitBtn = $(this).find('button[type="submit"]');
        submitBtn.prop('disabled', true);
        submitBtn.html('<span class="spinner-border spinner-border-sm"></span> 처리 중...');
    });
    
    // 카드 호버 효과 강화
    $('.card').hover(
        function() {
            $(this).addClass('shadow-lg');
        },
        function() {
            $(this).removeClass('shadow-lg');
        }
    );
    
    // Textarea 자동 높이 조정
    $('textarea').on('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // 뒤로가기 버튼 확인
    $('.btn-secondary[href*="list"]').on('click', function(e) {
        const form = $('form');
        if (form.length && form.find('input, textarea').filter(function() {
            return $(this).val() !== '';
        }).length > 0) {
            const confirmed = confirm('작성 중인 내용이 있습니다. 정말로 나가시겠습니까?');
            if (!confirmed) {
                e.preventDefault();
            }
        }
    });
    
    // 스크롤 시 네비게이션 바 그림자 효과
    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('.navbar').addClass('shadow');
        } else {
            $('.navbar').removeClass('shadow');
        }
    });
    
    // 툴팁 활성화 (Bootstrap)
    $('[data-toggle="tooltip"]').tooltip();
    
    // 메모 검색 기능 (클라이언트 사이드)
    $('#memoSearch').on('keyup', function() {
        const value = $(this).val().toLowerCase();
        $('.card').filter(function() {
            $(this).parent().toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
});

// 페이지 로드 완료 시
window.addEventListener('load', function() {
    // 페이드인 효과
    $('main').css('opacity', 0).animate({opacity: 1}, 500);
});
