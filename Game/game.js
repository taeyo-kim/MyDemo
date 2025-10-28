// Canvas 설정
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Canvas 크기 설정
canvas.width = 800;
canvas.height = 600;

// 게임 상태
let gameState = {
    score: 0,
    lives: 3,
    level: 1,
    isPlaying: false,
    isPaused: false,
    ballLaunched: false
};

// 패들 설정
const paddle = {
    width: 120,
    height: 15,
    x: canvas.width / 2 - 60,
    y: canvas.height - 40,
    speed: 8,
    dx: 0
};

// 볼 설정
const ball = {
    radius: 8,
    x: canvas.width / 2,
    y: paddle.y - 10,
    speed: 4,
    dx: 0,
    dy: 0
};

// 벽돌 설정 (이미지 기반)
const brickConfig = {
    rows: 6,
    cols: 14,
    width: 55,
    height: 20,
    padding: 2,
    offsetX: 5,
    offsetY: 60
};

// 벽돌 색상 배열 (이미지의 색상 패턴)
const brickColors = [
    ['#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF', '#00BFFF'], // 청록색
    ['#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32', '#32CD32'], // 초록색
    ['#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444', '#FF4444'], // 빨간색
    ['#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00', '#FF8C00'], // 주황색
    ['#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700'], // 노란색
    ['#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700', '#FFD700']  // 노란색
];

// 점수 배열 (행별 점수)
const brickPoints = [7, 7, 4, 4, 1, 1];

let bricks = [];

// 벽돌 초기화
function createBricks() {
    bricks = [];
    for (let row = 0; row < brickConfig.rows; row++) {
        bricks[row] = [];
        for (let col = 0; col < brickConfig.cols; col++) {
            bricks[row][col] = {
                x: col * (brickConfig.width + brickConfig.padding) + brickConfig.offsetX,
                y: row * (brickConfig.height + brickConfig.padding) + brickConfig.offsetY,
                status: 1,
                color: brickColors[row][col],
                points: brickPoints[row]
            };
        }
    }
}

// 패들 그리기
function drawPaddle() {
    ctx.fillStyle = '#FFFFFF';
    ctx.shadowColor = '#667eea';
    ctx.shadowBlur = 10;
    ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
    ctx.shadowBlur = 0;
}

// 볼 그리기
function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = '#FFFFFF';
    ctx.shadowColor = '#FFD700';
    ctx.shadowBlur = 15;
    ctx.fill();
    ctx.closePath();
    ctx.shadowBlur = 0;
}

// 벽돌 그리기
function drawBricks() {
    for (let row = 0; row < brickConfig.rows; row++) {
        for (let col = 0; col < brickConfig.cols; col++) {
            const brick = bricks[row][col];
            if (brick.status === 1) {
                ctx.fillStyle = brick.color;
                ctx.fillRect(brick.x, brick.y, brickConfig.width, brickConfig.height);
                
                // 벽돌 테두리
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 1;
                ctx.strokeRect(brick.x, brick.y, brickConfig.width, brickConfig.height);
                
                // 벽돌 하이라이트
                ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
                ctx.fillRect(brick.x, brick.y, brickConfig.width, brickConfig.height / 3);
            }
        }
    }
}

// 패들 이동
function movePaddle() {
    paddle.x += paddle.dx;

    // 경계 체크
    if (paddle.x < 0) {
        paddle.x = 0;
    }
    if (paddle.x + paddle.width > canvas.width) {
        paddle.x = canvas.width - paddle.width;
    }
}

// 볼 이동
function moveBall() {
    if (!gameState.ballLaunched) {
        // 볼이 발사되기 전에는 패들과 함께 이동
        ball.x = paddle.x + paddle.width / 2;
        ball.y = paddle.y - ball.radius - 2;
        return;
    }

    ball.x += ball.dx;
    ball.y += ball.dy;

    // 벽 충돌
    if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
        ball.dx = -ball.dx;
    }

    if (ball.y - ball.radius < 0) {
        ball.dy = -ball.dy;
    }

    // 패들 충돌
    if (ball.y + ball.radius > paddle.y &&
        ball.x > paddle.x &&
        ball.x < paddle.x + paddle.width) {
        
        // 패들의 어느 위치에 맞았는지에 따라 반사각 조정
        const hitPos = (ball.x - paddle.x) / paddle.width;
        const angle = (hitPos - 0.5) * Math.PI / 3; // -60도 ~ 60도
        
        const speed = Math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy);
        ball.dx = speed * Math.sin(angle);
        ball.dy = -speed * Math.cos(angle);
    }

    // 바닥에 떨어짐
    if (ball.y + ball.radius > canvas.height) {
        gameState.lives--;
        updateLives();
        
        if (gameState.lives <= 0) {
            gameOver();
        } else {
            resetBall();
        }
    }
}

// 벽돌 충돌 감지
function detectBrickCollision() {
    for (let row = 0; row < brickConfig.rows; row++) {
        for (let col = 0; col < brickConfig.cols; col++) {
            const brick = bricks[row][col];
            
            if (brick.status === 1) {
                if (ball.x + ball.radius > brick.x &&
                    ball.x - ball.radius < brick.x + brickConfig.width &&
                    ball.y + ball.radius > brick.y &&
                    ball.y - ball.radius < brick.y + brickConfig.height) {
                    
                    ball.dy = -ball.dy;
                    brick.status = 0;
                    gameState.score += brick.points;
                    updateScore();
                    
                    // 모든 벽돌 파괴 시 레벨 완료
                    if (checkLevelComplete()) {
                        levelComplete();
                    }
                }
            }
        }
    }
}

// 레벨 완료 체크
function checkLevelComplete() {
    for (let row = 0; row < brickConfig.rows; row++) {
        for (let col = 0; col < brickConfig.cols; col++) {
            if (bricks[row][col].status === 1) {
                return false;
            }
        }
    }
    return true;
}

// 볼 리셋
function resetBall() {
    gameState.ballLaunched = false;
    ball.x = paddle.x + paddle.width / 2;
    ball.y = paddle.y - ball.radius - 2;
    ball.dx = 0;
    ball.dy = 0;
}

// 게임 그리기
function draw() {
    // 캔버스 클리어
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawBricks();
    drawPaddle();
    drawBall();
}

// 게임 업데이트
function update() {
    if (!gameState.isPlaying || gameState.isPaused) return;
    
    movePaddle();
    moveBall();
    detectBrickCollision();
    draw();
    
    requestAnimationFrame(update);
}

// 점수 업데이트
function updateScore() {
    document.getElementById('score').textContent = gameState.score;
}

// 생명 업데이트
function updateLives() {
    document.getElementById('lives').textContent = gameState.lives;
}

// 레벨 업데이트
function updateLevel() {
    document.getElementById('level').textContent = gameState.level;
}

// 게임 시작
function startGame() {
    gameState.isPlaying = true;
    gameState.isPaused = false;
    document.getElementById('startBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = false;
    createBricks();
    draw();
    update();
}

// 게임 일시정지
function pauseGame() {
    gameState.isPaused = !gameState.isPaused;
    document.getElementById('pauseBtn').textContent = gameState.isPaused ? '재개' : '일시정지';
    if (!gameState.isPaused) {
        update();
    }
}

// 게임 리셋
function resetGame() {
    gameState.score = 0;
    gameState.lives = 3;
    gameState.level = 1;
    gameState.isPlaying = false;
    gameState.isPaused = false;
    gameState.ballLaunched = false;
    
    paddle.x = canvas.width / 2 - paddle.width / 2;
    resetBall();
    
    updateScore();
    updateLives();
    updateLevel();
    
    document.getElementById('startBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('pauseBtn').textContent = '일시정지';
    
    createBricks();
    draw();
}

// 게임 오버
function gameOver() {
    gameState.isPlaying = false;
    document.getElementById('finalScore').textContent = gameState.score;
    document.getElementById('gameOver').classList.add('show');
}

// 레벨 완료
function levelComplete() {
    gameState.isPlaying = false;
    gameState.level++;
    ball.speed += 0.5;
    document.getElementById('levelComplete').classList.add('show');
}

// 다음 레벨
function nextLevel() {
    updateLevel();
    resetBall();
    createBricks();
    document.getElementById('levelComplete').classList.remove('show');
    gameState.isPlaying = true;
    update();
}

// 키보드 이벤트
function keyDown(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
        paddle.dx = paddle.speed;
    } else if (e.key === 'Left' || e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
        paddle.dx = -paddle.speed;
    } else if (e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        if (gameState.isPlaying && !gameState.ballLaunched) {
            gameState.ballLaunched = true;
            const angle = (Math.random() - 0.5) * Math.PI / 4; // -45도 ~ 45도
            ball.dx = ball.speed * Math.sin(angle);
            ball.dy = -ball.speed * Math.cos(angle);
        }
    }
}

function keyUp(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D' ||
        e.key === 'Left' || e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
        paddle.dx = 0;
    }
}

// 이벤트 리스너
document.addEventListener('keydown', keyDown);
document.addEventListener('keyup', keyUp);

document.getElementById('startBtn').addEventListener('click', startGame);
document.getElementById('pauseBtn').addEventListener('click', pauseGame);
document.getElementById('resetBtn').addEventListener('click', resetGame);
document.getElementById('restartBtn').addEventListener('click', () => {
    document.getElementById('gameOver').classList.remove('show');
    resetGame();
    startGame();
});
document.getElementById('nextLevelBtn').addEventListener('click', nextLevel);

// 초기 그리기
createBricks();
draw();
