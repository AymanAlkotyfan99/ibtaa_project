// --- Custom Cursor ---
const cursorDot = document.querySelector(".cursor-dot");
const cursorOutline = document.querySelector(".cursor-outline");

if (cursorDot && cursorOutline) {
    window.addEventListener("mousemove", (e) => {
        const posX = e.clientX;
        const posY = e.clientY;

        // Dot follows immediately
        cursorDot.style.left = `${posX}px`;
        cursorDot.style.top = `${posY}px`;

        // Outline follows with slight delay (animation in CSS or via GSAP lag)
        cursorOutline.animate(
            {
                left: `${posX}px`,
                top: `${posY}px`,
            },
            { duration: 500, fill: "forwards" },
        );
    });

    // Interactive elements hover effect for cursor
    const interactiveElements = document.querySelectorAll(
        "a, button, input, textarea",
    );
    interactiveElements.forEach((el) => {
        el.addEventListener("mouseenter", () => {
            cursorOutline.style.transform = "translate(-50%, -50%) scale(1.5)";
            cursorOutline.style.backgroundColor = "rgba(255, 255, 255, 0.1)";
            cursorOutline.style.borderColor = "transparent";
        });
        el.addEventListener("mouseleave", () => {
            cursorOutline.style.transform = "translate(-50%, -50%) scale(1)";
            cursorOutline.style.backgroundColor = "transparent";
            cursorOutline.style.borderColor = "rgba(255, 255, 255, 0.5)";
        });
    });
}

// --- GSAP Animations ---
gsap.registerPlugin(ScrollTrigger);

// Hero Reveal
const tl = gsap.timeline();

tl.to(".hero-reveal", {
    y: 0,
    opacity: 1,
    duration: 1,
    stagger: 0.2,
    ease: "power4.out",
    delay: 0.5,
});

// Navbar Scroll Effect
window.addEventListener("scroll", () => {
    const nav = document.querySelector(".navbar");
    if (nav) {
        if (window.scrollY > 50) {
            nav.classList.add("scrolled");
        } else {
            nav.classList.remove("scrolled");
        }
    }
});

// Scroll Triggers
gsap.utils.toArray(".reveal-up").forEach((elem) => {
    gsap.from(elem, {
        scrollTrigger: {
            trigger: elem,
            start: "top 80%",
            toggleActions: "play none none reverse",
        },
        y: 50,
        opacity: 0,
        duration: 1,
        ease: "power2.out",
    });
});

gsap.utils.toArray(".reveal-left").forEach((elem) => {
    gsap.from(elem, {
        scrollTrigger: {
            trigger: elem,
            start: "top 85%",
            toggleActions: "play none none reverse",
        },
        x: -50,
        opacity: 0,
        duration: 1,
        ease: "power2.out",
    });
});

gsap.utils.toArray(".reveal-right").forEach((elem) => {
    gsap.from(elem, {
        scrollTrigger: {
            trigger: elem,
            start: "top 85%",
            toggleActions: "play none none reverse",
        },
        x: 50,
        opacity: 0,
        duration: 1,
        ease: "power2.out",
    });
});

// Project Image Scale
gsap.utils.toArray(".reveal-scale").forEach((elem) => {
    gsap.from(elem, {
        scrollTrigger: {
            trigger: elem,
            start: "top 90%",
            toggleActions: "play none none reverse",
        },
        scale: 0.8,
        opacity: 0,
        duration: 1.2,
        ease: "power3.out",
    });
});

// Magnetic Buttons
const magneticBtns = document.querySelectorAll(".magnetic-btn");

magneticBtns.forEach((btn) => {
    btn.addEventListener("mousemove", (e) => {
        const position = btn.getBoundingClientRect();
        const x = e.clientX - position.left - position.width / 2;
        const y = e.clientY - position.top - position.height / 2;

        gsap.to(btn, {
            x: x * 0.3,
            y: y * 0.3,
            duration: 0.3,
            ease: "power2.out",
        });
    });

    btn.addEventListener("mouseleave", () => {
        gsap.to(btn, {
            x: 0,
            y: 0,
            duration: 0.3,
            ease: "elastic.out(1, 0.3)",
        });
    });
});

// --- Three.js Background ---
const canvas = document.querySelector("#webgl-canvas");
if (canvas) {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000,
    );
    const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
    });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 2000;

    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        // Spread particles in a wide area
        posArray[i] = (Math.random() - 0.5) * 15; // Range -7.5 to 7.5
    }

    particlesGeometry.setAttribute(
        "position",
        new THREE.BufferAttribute(posArray, 3),
    );

    // Material
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.02,
        color: 0x00f2ea,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending,
    });

    // Mesh
    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    // Lights
    const pointLight = new THREE.PointLight(0xffffff, 0.1);
    pointLight.position.x = 2;
    pointLight.position.y = 3;
    pointLight.position.z = 4;
    scene.add(pointLight);

    camera.position.z = 3;

    // Mouse Interaction variables
    let mouseX = 0;
    let mouseY = 0;

    window.addEventListener("mousemove", (event) => {
        mouseX = event.clientX / window.innerWidth - 0.5;
        mouseY = event.clientY / window.innerHeight - 0.5;
    });

    // Animation Loop
    const clock = new THREE.Clock();

    const tick = () => {
        const elapsedTime = clock.getElapsedTime();

        // Constant rotation
        particlesMesh.rotation.y = elapsedTime * 0.05;
        particlesMesh.rotation.x = elapsedTime * 0.02;

        // Mouse interaction (parallax)
        // Smooth transition
        particlesMesh.rotation.y += 0.5 * (mouseX - particlesMesh.rotation.y) * 0.01;
        particlesMesh.rotation.x += 0.5 * (mouseY - particlesMesh.rotation.x) * 0.01;

        renderer.render(scene, camera);
        window.requestAnimationFrame(tick);
    };

    tick();

    // Handle Resize
    window.addEventListener("resize", () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    });
}
