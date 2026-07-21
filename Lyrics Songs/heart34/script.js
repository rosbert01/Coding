const canvascallback = () => {
    const canvasElement = document.querySelector('canvas');
    const drawingContext = canvasElement.getContext('2d');

    const CONFIG = {
        width: 500,
        height: 500,
        particleCount: 1000,
        particleSize: 2,
        scale: 12,
        speed: 0.4,
        range: { min: -200, max: 200 },
    };

    const animationState = {
        a_parameter: 100,
        direction: 1,
        isInverted: false,
    };

    canvasElement.width = CONFIG.width;
    canvasElement.height = CONFIG.height;

    const toRadians = (deg) => (deg * Math.PI) / 180;

    class HeartDot {
        constructor(angle, centerX, centerY) {
            this.angle = angle;
            this.centerX = centerX;
            this.centerY = centerY;
            this.currentX = centerX;
            this.currentY = centerY;

            const hue = 330 + Math.cos(this.angle) * 30;
            this.primaryColor = `hsl(${hue}, 100%, 60%)`;
            this.secondaryColor = `hsl(${hue}, 100%, 40%)`;
        }

        calculatePosition() {
            const sinT = Math.sin(this.angle);
            const cosT = Math.cos(this.angle);

            const xNormal = 16 * Math.pow(sinT, 3) * animationState.direction;

            const yNormal =
                (13 * cosT -
                    6 * Math.cos(2 * this.angle) -
                    2 * Math.cos(3 * this.angle) -
                    Math.cos(animationState.a_parameter * this.angle)) *
                -1;

            this.currentX = xNormal * CONFIG.scale + this.centerX;
            this.currentY = yNormal * CONFIG.scale + this.centerY;
        }

        draw(ctx) {
            ctx.fillStyle = animationState.isInverted
                ? this.secondaryColor
                : this.primaryColor;

            ctx.beginPath();
            ctx.arc(this.currentX, this.currentY, CONFIG.particleSize, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    class AnimationController {
        constructor() {
            this.particles = [];
            this.centerX = CONFIG.width / 2;
            this.centerY = CONFIG.height / 2;
            this.initParticles();
        }

        initParticles() {
            for (let i = 0; i < CONFIG.particleCount; i++) {
                const angle = toRadians((360 / CONFIG.particleCount) * i);
                this.particles.push(new HeartDot(angle, this.centerX, this.centerY));
            }
        }

        updateState() {
            if (animationState.direction === 1) {
                if (animationState.a_parameter > CONFIG.range.min) {
                    animationState.a_parameter -= CONFIG.speed;
                } else {
                    this.flip();
                }
            } else {
                if (animationState.a_parameter < CONFIG.range.max) {
                    animationState.a_parameter += CONFIG.speed;
                } else {
                    this.flip();
                }
            }

            this.particles.forEach(p => p.calculatePosition());
        }

        flip() {
            animationState.direction *= -1;
            animationState.isInverted = !animationState.isInverted;
        }

        render() {
            drawingContext.clearRect(0, 0, CONFIG.width, CONFIG.height);
            drawingContext.save();
            this.particles.forEach(p => p.draw(drawingContext));
            drawingContext.restore();
        }

        loop() {
            this.updateState();
            this.render();
            requestAnimationFrame(() => this.loop());
        }
    }

    const app = new AnimationController();
    app.loop();
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', canvascallback);
} else {
    canvascallback();
}
