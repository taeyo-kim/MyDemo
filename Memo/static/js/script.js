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
    
    // 폼 유효성 검사 강화
    $('form').on('submit', function(e) {
        const form = $(this);
        const submitBtn = form.find('button[type="submit"]');
        
        // 필수 입력 필드 검사
        let isValid = true;
        form.find('input[required], textarea[required]').each(function() {
            const field = $(this);
            const value = field.val().trim();
            
            if (!value) {
                isValid = false;
                field.addClass('is-invalid');
                
                // 에러 메시지 추가
                if (!field.next('.invalid-feedback').length) {
                    field.after('<div class="invalid-feedback">이 필드는 필수 입력 항목입니다.</div>');
                }
            } else {
                field.removeClass('is-invalid');
                field.next('.invalid-feedback').remove();
            }
        });
        
        // 이메일 형식 검사
        form.find('input[type="email"]').each(function() {
            const field = $(this);
            const value = field.val().trim();
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (value && !emailPattern.test(value)) {
                isValid = false;
                field.addClass('is-invalid');
                
                if (!field.next('.invalid-feedback').length) {
                    field.after('<div class="invalid-feedback">올바른 이메일 주소를 입력해주세요.</div>');
                }
            }
        });
        
        // 비밀번호 확인 검사 (회원가입)
        const password1 = form.find('input[name="password1"]');
        const password2 = form.find('input[name="password2"]');
        
        if (password1.length && password2.length) {
            if (password1.val() !== password2.val()) {
                isValid = false;
                password2.addClass('is-invalid');
                
                if (!password2.next('.invalid-feedback').length) {
                    password2.after('<div class="invalid-feedback">비밀번호가 일치하지 않습니다.</div>');
                }
            }
        }
        
        if (!isValid) {
            e.preventDefault();
            // 첫 번째 에러 필드로 스크롤
            const firstError = form.find('.is-invalid').first();
            if (firstError.length) {
                $('html, body').animate({
                    scrollTop: firstError.offset().top - 100
                }, 300);
            }
            return false;
        }
        
        // 유효성 검사 통과 시 로딩 표시
        submitBtn.prop('disabled', true);
        const originalText = submitBtn.html();
        submitBtn.data('original-text', originalText);
        submitBtn.html('<span class="spinner-border spinner-border-sm"></span> 처리 중...');
    });
    
    // 입력 시 에러 메시지 제거
    $('input, textarea').on('input', function() {
        $(this).removeClass('is-invalid');
        $(this).next('.invalid-feedback').remove();
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
    
    // 로딩 오버레이 제거
    $('.loading-overlay').removeClass('active');
});

// 긴 작업 시 로딩 오버레이 표시
function showLoadingOverlay(message = '처리 중...') {
    if (!$('.loading-overlay').length) {
        $('body').append(`
            <div class="loading-overlay">
                <div class="text-center text-white">
                    <div class="spinner-border" role="status" style="width: 3rem; height: 3rem;">
                        <span class="sr-only">Loading...</span>
                    </div>
                    <p class="mt-3">${message}</p>
                </div>
            </div>
        `);
    }
    $('.loading-overlay').addClass('active');
}

function hideLoadingOverlay() {
    $('.loading-overlay').removeClass('active');
}

// 키보드 네비게이션 개선
$(document).on('keydown', function(e) {
    // ESC 키로 모달 닫기
    if (e.key === 'Escape') {
        $('.modal').modal('hide');
        $('.alert').fadeOut();
    }
});
