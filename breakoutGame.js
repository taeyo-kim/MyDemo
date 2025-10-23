// 캔버스 설정
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 게임 변수 설정
let score = 0;
let lives = 3;
let gameOver = false;
let gameWon = false;
let gameStarted = false;

// 패들 설정
const paddleHeight = 15;
const paddleWidth = 100;
let paddleX = (canvas.width - paddleWidth) / 2;
const paddleY = canvas.height - paddleHeight - 10;
const paddleSpeed = 8;

// 공 설정
const ballRadius = 8;
let ballX = canvas.width / 2;
let ballY = canvas.height - 30;
let ballSpeedX = 5;
let ballSpeedY = -5;

// 블록 설정
const blockRows = 6;
const blockColumns = 12;
const blockWidth = 60;
const blockHeight = 25;
const blockPadding = 5;
const blockOffsetTop = 50;
const blockOffsetLeft = 30;

// 블록 색상 배열
const blockColors = [
    '#FF5252', // 빨강
    '#FF9800', // 주황
    '#FFEB3B', // 노랑
    '#4CAF50', // 초록
    '#2196F3', // 파랑
    '#9C27B0'  // 보라
];

// 블록 배열 생성
const blocks = [];
for (let c = 0; c < blockColumns; c++) {
    blocks[c] = [];
    for (let r = 0; r < blockRows; r++) {
        blocks[c][r] = { x: 0, y: 0, status: 1 };
    }
}

// 키보드 입력 처리
const keys = {
    rightPressed: false,
    leftPressed: false
};

// 키보드 이벤트 리스너
document.addEventListener('keydown', keyDownHandler);
document.addEventListener('keyup', keyUpHandler);

// 마우스/터치 이벤트 리스너
document.addEventListener('mousemove', mouseMoveHandler);
canvas.addEventListener('click', startGame);
canvas.addEventListener('touchstart', handleTouch);
canvas.addEventListener('touchmove', handleTouch);

// 키 입력 처리 함수
function keyDownHandler(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight') {
        keys.rightPressed = true;
    } else if (e.key === 'Left' || e.key === 'ArrowLeft') {
        keys.leftPressed = true;
    } else if (e.key === ' ' && !gameStarted) {
        startGame();
    }
}

function keyUpHandler(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight') {
        keys.rightPressed = false;
    } else if (e.key === 'Left' || e.key === 'ArrowLeft') {
        keys.leftPressed = false;
    }
}

// 마우스 이동 처리 함수
function mouseMoveHandler(e) {
    const relativeX = e.clientX - canvas.offsetLeft;
    if (relativeX > 0 && relativeX < canvas.width) {
        paddleX = relativeX - paddleWidth / 2;
        
        // 패들이 캔버스를 벗어나지 않도록 제한
        if (paddleX < 0) {
            paddleX = 0;
        } else if (paddleX + paddleWidth > canvas.width) {
            paddleX = canvas.width - paddleWidth;
        }
    }
}

// 터치 처리 함수
function handleTouch(e) {
    e.preventDefault();
    if (!gameStarted) {
        startGame();
        return;
    }
    
    const relativeX = e.touches[0].clientX - canvas.offsetLeft;
    if (relativeX > 0 && relativeX < canvas.width) {
        paddleX = relativeX - paddleWidth / 2;
        
        // 패들이 캔버스를 벗어나지 않도록 제한
        if (paddleX < 0) {
            paddleX = 0;
        } else if (paddleX + paddleWidth > canvas.width) {
            paddleX = canvas.width - paddleWidth;
        }
    }
}

// 게임 시작 함수
function startGame() {
    if (!gameStarted && !gameOver && !gameWon) {
        gameStarted = true;
        draw();
    }
}

// 충돌 감지 함수
function collisionDetection() {
    for (let c = 0; c < blockColumns; c++) {
        for (let r = 0; r < blockRows; r++) {
            const b = blocks[c][r];
            if (b.status === 1) {
                if (
                    ballX > b.x &&
                    ballX < b.x + blockWidth &&
                    ballY > b.y &&
                    ballY < b.y + blockHeight
                ) {
                    ballSpeedY = -ballSpeedY;
                    b.status = 0;
                    score++;
                    document.getElementById('score').textContent = `점수: ${score}`;
                    
                    // 모든 블록이 제거되었는지 확인
                    if (score === blockRows * blockColumns) {
                        gameWon = true;
                        gameStarted = false;
                    }
                }
            }
        }
    }
}

// 공 그리기 함수
function drawBall() {
    ctx.beginPath();
    ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = '#FFFFFF';
    ctx.fill();
    ctx.closePath();
}

// 패들 그리기 함수
function drawPaddle() {
    ctx.beginPath();
    ctx.rect(paddleX, paddleY, paddleWidth, paddleHeight);
    ctx.fillStyle = '#00AAFF';
    ctx.fill();
    ctx.closePath();
    
    // 패들 효과 (그라데이션)
    ctx.beginPath();
    ctx.rect(paddleX + 5, paddleY + 3, paddleWidth - 10, 5);
    ctx.fillStyle = '#80D0FF';
    ctx.fill();
    ctx.closePath();
}

// 블록 그리기 함수
function drawBlocks() {
    for (let c = 0; c < blockColumns; c++) {
        for (let r = 0; r < blockRows; r++) {
            if (blocks[c][r].status === 1) {
                const blockX = c * (blockWidth + blockPadding) + blockOffsetLeft;
                const blockY = r * (blockHeight + blockPadding) + blockOffsetTop;
                blocks[c][r].x = blockX;
                blocks[c][r].y = blockY;
                
                // 블록 그리기
                ctx.beginPath();
                ctx.rect(blockX, blockY, blockWidth, blockHeight);
                ctx.fillStyle = blockColors[r];
                ctx.fill();
                ctx.closePath();
                
                // 블록 효과 (하이라이트)
                ctx.beginPath();
                ctx.rect(blockX + 2, blockY + 2, blockWidth - 25, 5);
                ctx.rect(blockX + 2, blockY + 2, 5, blockHeight - 4);
                ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
                ctx.fill();
                ctx.closePath();
            }
        }
    }
}

// 게임 상태 메시지 그리기
function drawGameStatus() {
    if (gameOver) {
        ctx.font = '36px Arial';
        ctx.fillStyle = 'red';
        ctx.textAlign = 'center';
        ctx.fillText('게임 오버', canvas.width / 2, canvas.height / 2);
        ctx.font = '18px Arial';
        ctx.fillStyle = 'white';
        ctx.fillText('다시 시작하려면 화면을 클릭하세요', canvas.width / 2, canvas.height / 2 + 40);
    } else if (gameWon) {
        ctx.font = '36px Arial';
        ctx.fillStyle = 'green';
        ctx.textAlign = 'center';
        ctx.fillText('승리!', canvas.width / 2, canvas.height / 2);
        ctx.font = '18px Arial';
        ctx.fillStyle = 'white';
        ctx.fillText('다시 시작하려면 화면을 클릭하세요', canvas.width / 2, canvas.height / 2 + 40);
    } else if (!gameStarted) {
        ctx.font = '24px Arial';
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.fillText('시작하려면 화면을 클릭하세요', canvas.width / 2, canvas.height / 2);
    }
}

// 게임 초기화 함수
function resetGame() {
    score = 0;
    lives = 3;
    gameOver = false;
    gameWon = false;
    gameStarted = false;
    
    // 블록 재설정
    for (let c = 0; c < blockColumns; c++) {
        for (let r = 0; r < blockRows; r++) {
            blocks[c][r].status = 1;
        }
    }
    
    // 공과 패들 위치 초기화
    ballX = canvas.width / 2;
    ballY = canvas.height - 30;
    ballSpeedX = 5;
    ballSpeedY = -5;
    paddleX = (canvas.width - paddleWidth) / 2;
    
    // UI 업데이트
    document.getElementById('score').textContent = `점수: ${score}`;
    document.getElementById('lives').textContent = `생명: ${lives}`;
    
    // 첫 화면 그리기
    draw();
}

// 메인 게임 루프 함수
function draw() {
    // 화면 지우기
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 게임 요소 그리기
    drawBlocks();
    drawBall();
    drawPaddle();
    
    // 게임 진행 중이 아닐 때 메시지 표시
    drawGameStatus();
    
    // 게임이 진행 중이 아닌 경우 애니메이션 중지
    if (!gameStarted || gameOver || gameWon) {
        return;
    }
    
    // 충돌 감지
    collisionDetection();
    
    // 공 위치 업데이트
    ballX += ballSpeedX;
    ballY += ballSpeedY;
    
    // 벽과 공의 충돌 검사
    if (ballX + ballSpeedX > canvas.width - ballRadius || ballX + ballSpeedX < ballRadius) {
        ballSpeedX = -ballSpeedX;
    }
    
    // 천장과 공의 충돌 검사
    if (ballY + ballSpeedY < ballRadius) {
        ballSpeedY = -ballSpeedY;
    } 
    
    // 패들과 공의 충돌 검사 - 패들의 윗면만 감지하도록 개선
    if (ballY + ballRadius > paddleY && ballY + ballRadius < paddleY + 10 && 
        ballX > paddleX && ballX < paddleX + paddleWidth && ballSpeedY > 0) {
        // 패들의 어느 부분에 부딪혔는지에 따라 공의 반사 각도 조절
        const paddleCenter = paddleX + paddleWidth / 2;
        const hitPosition = ballX - paddleCenter;
        
        ballSpeedX = hitPosition * 0.2; // 부딪힌 위치에 따라 X 속도 조절
        ballSpeedY = -ballSpeedY;
        
        // 속도 제한
        const maxSpeed = 8;
        if (Math.abs(ballSpeedX) > maxSpeed) {
            ballSpeedX = maxSpeed * Math.sign(ballSpeedX);
        }
    }
    // 바닥과 공의 충돌 검사 (실패)
    else if (ballY + ballSpeedY > canvas.height - ballRadius) {
        // 생명 감소
        lives--;
        document.getElementById('lives').textContent = `생명: ${lives}`;
        
        if (lives <= 0) {
            gameOver = true;
            gameStarted = false;
        } else {
            // 공과 패들 재설정
            ballX = canvas.width / 2;
            ballY = canvas.height - 30;
            ballSpeedX = 5;
            ballSpeedY = -5;
            paddleX = (canvas.width - paddleWidth) / 2;
            
            // 잠시 게임 중지
            gameStarted = false;
        }
    }
    
    // 패들 이동 처리
    if (keys.rightPressed && paddleX < canvas.width - paddleWidth) {
        paddleX += paddleSpeed;
    } else if (keys.leftPressed && paddleX > 0) {
        paddleX -= paddleSpeed;
    }
    
    // 다음 프레임 요청
    requestAnimationFrame(draw);
}

// 클릭 이벤트로 게임 리셋
canvas.addEventListener('click', function() {
    if (gameOver || gameWon) {
        resetGame();
    }
});

// 초기 게임 화면 그리기
resetGame();