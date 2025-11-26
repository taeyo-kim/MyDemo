// Canvas setup
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game variables
let score = 0;
let lives = 3;
let gameRunning = false;
let gamePaused = false;

// Ball properties
const ball = {
    x: canvas.width / 2,
    y: canvas.height - 50,
    dx: 3,
    dy: -3,
    radius: 8,
    speed: 3
};

// Paddle properties
const paddle = {
    width: 80,
    height: 12,
    x: (canvas.width - 80) / 2,
    y: canvas.height - 30,
    speed: 7,
    dx: 0
};

// Brick properties
const brickInfo = {
    rowCount: 6,
    columnCount: 10,
    width: 42,
    height: 20,
    padding: 5,
    offsetTop: 60,
    offsetLeft: 15
};

// Brick colors
const brickColors = [
    '#FF6B6B',  // Red
    '#FF8E53',  // Orange
    '#FEE440',  // Yellow
    '#4ECDC4',  // Turquoise
    '#45B7D1',  // Blue
    '#96CEB4'   // Green
];

// Create bricks
let bricks = [];
function createBricks() {
    bricks = [];
    for (let row = 0; row < brickInfo.rowCount; row++) {
        bricks[row] = [];
        for (let col = 0; col < brickInfo.columnCount; col++) {
            bricks[row][col] = {
                x: 0,
                y: 0,
                status: 1,
                color: brickColors[row]
            };
        }
    }
}

// Draw ball
function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = '#FFFFFF';
    ctx.fill();
    ctx.strokeStyle = '#FFD700';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.closePath();
}

// Draw paddle
function drawPaddle() {
    ctx.beginPath();
    ctx.roundRect(paddle.x, paddle.y, paddle.width, paddle.height, 5);
    ctx.fillStyle = '#FFFFFF';
    ctx.fill();
    ctx.strokeStyle = '#FFD700';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.closePath();
}

// Draw bricks
function drawBricks() {
    for (let row = 0; row < brickInfo.rowCount; row++) {
        for (let col = 0; col < brickInfo.columnCount; col++) {
            if (bricks[row][col].status === 1) {
                const brickX = col * (brickInfo.width + brickInfo.padding) + brickInfo.offsetLeft;
                const brickY = row * (brickInfo.height + brickInfo.padding) + brickInfo.offsetTop;
                
                bricks[row][col].x = brickX;
                bricks[row][col].y = brickY;
                
                ctx.beginPath();
                ctx.roundRect(brickX, brickY, brickInfo.width, brickInfo.height, 3);
                ctx.fillStyle = bricks[row][col].color;
                ctx.fill();
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
                ctx.lineWidth = 1;
                ctx.stroke();
                ctx.closePath();
            }
        }
    }
}

// Move paddle
function movePaddle() {
    paddle.x += paddle.dx;
    
    // Wall detection
    if (paddle.x < 0) {
        paddle.x = 0;
    }
    if (paddle.x + paddle.width > canvas.width) {
        paddle.x = canvas.width - paddle.width;
    }
}

// Move ball
function moveBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;
    
    // Wall collision (left and right)
    if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
        ball.dx *= -1;
    }
    
    // Wall collision (top)
    if (ball.y - ball.radius < 0) {
        ball.dy *= -1;
    }
    
    // Paddle collision
    if (ball.y + ball.radius > paddle.y &&
        ball.x > paddle.x &&
        ball.x < paddle.x + paddle.width) {
        ball.dy *= -1;
        
        // Change ball direction based on where it hits the paddle
        const hitPos = (ball.x - paddle.x) / paddle.width;
        ball.dx = (hitPos - 0.5) * 8;
    }
    
    // Bottom wall - lose life
    if (ball.y + ball.radius > canvas.height) {
        lives--;
        updateLives();
        
        if (lives === 0) {
            gameOver();
        } else {
            resetBall();
        }
    }
}

// Brick collision
function brickCollision() {
    for (let row = 0; row < brickInfo.rowCount; row++) {
        for (let col = 0; col < brickInfo.columnCount; col++) {
            const brick = bricks[row][col];
            
            if (brick.status === 1) {
                if (ball.x > brick.x &&
                    ball.x < brick.x + brickInfo.width &&
                    ball.y > brick.y &&
                    ball.y < brick.y + brickInfo.height) {
                    
                    ball.dy *= -1;
                    brick.status = 0;
                    score += 10;
                    updateScore();
                    
                    // Check win
                    if (score === brickInfo.rowCount * brickInfo.columnCount * 10) {
                        winGame();
                    }
                }
            }
        }
    }
}

// Update score display
function updateScore() {
    document.getElementById('score').textContent = score;
}

// Update lives display
function updateLives() {
    document.getElementById('lives').textContent = lives;
}

// Reset ball position
function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height - 50;
    ball.dx = 3 * (Math.random() > 0.5 ? 1 : -1);
    ball.dy = -3;
}

// Draw everything
function draw() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawBricks();
    drawBall();
    drawPaddle();
}

// Game loop
function update() {
    if (!gameRunning || gamePaused) return;
    
    movePaddle();
    moveBall();
    brickCollision();
    draw();
    
    requestAnimationFrame(update);
}

// Start game
function startGame() {
    if (!gameRunning) {
        gameRunning = true;
        gamePaused = false;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        update();
    }
}

// Pause game
function pauseGame() {
    gamePaused = !gamePaused;
    document.getElementById('pauseBtn').textContent = gamePaused ? '재개' : '일시정지';
    
    if (!gamePaused) {
        update();
    }
}

// Reset game
function resetGame() {
    gameRunning = false;
    gamePaused = false;
    score = 0;
    lives = 3;
    
    resetBall();
    createBricks();
    paddle.x = (canvas.width - paddle.width) / 2;
    
    updateScore();
    updateLives();
    
    document.getElementById('startBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('pauseBtn').textContent = '일시정지';
    
    draw();
}

// Game over
function gameOver() {
    gameRunning = false;
    ctx.font = '48px Arial';
    ctx.fillStyle = '#FF6B6B';
    ctx.textAlign = 'center';
    ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2);
    
    setTimeout(() => {
        alert('게임 오버! 최종 점수: ' + score);
        resetGame();
    }, 100);
}

// Win game
function winGame() {
    gameRunning = false;
    ctx.font = '48px Arial';
    ctx.fillStyle = '#4ECDC4';
    ctx.textAlign = 'center';
    ctx.fillText('YOU WIN!', canvas.width / 2, canvas.height / 2);
    
    setTimeout(() => {
        alert('축하합니다! 모든 벽돌을 깼습니다!\n최종 점수: ' + score);
        resetGame();
    }, 100);
}

// Keyboard controls
function keyDown(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight') {
        paddle.dx = paddle.speed;
    } else if (e.key === 'Left' || e.key === 'ArrowLeft') {
        paddle.dx = -paddle.speed;
    }
}

function keyUp(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight' ||
        e.key === 'Left' || e.key === 'ArrowLeft') {
        paddle.dx = 0;
    }
}

// Mouse controls
function mouseMove(e) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    
    if (mouseX > 0 && mouseX < canvas.width) {
        paddle.x = mouseX - paddle.width / 2;
        
        // Keep paddle in bounds
        if (paddle.x < 0) paddle.x = 0;
        if (paddle.x + paddle.width > canvas.width) {
            paddle.x = canvas.width - paddle.width;
        }
    }
}

// Event listeners
document.addEventListener('keydown', keyDown);
document.addEventListener('keyup', keyUp);
canvas.addEventListener('mousemove', mouseMove);

document.getElementById('startBtn').addEventListener('click', startGame);
document.getElementById('pauseBtn').addEventListener('click', pauseGame);
document.getElementById('resetBtn').addEventListener('click', resetGame);

// Initialize game
createBricks();
draw();
document.getElementById('pauseBtn').disabled = true;
