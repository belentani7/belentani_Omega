/**
 * BELENTANI GSAP ENHANCEMENTS
 * Advanced parallax, scroll triggering, and cinemat animations
 */

document.addEventListener('DOMContentLoaded', () => {
    gsap.registerPlugin(ScrollTrigger);

    // Stagger all section titles with parallax
    gsap.utils.toArray('.section-title').forEach((element, index) => {
        gsap.from(element, {
            opacity: 0,
            y: 100,
            rotationX: -90,
            transformOrigin: '50% 50%',
            duration: 1.2,
            ease: 'back.out',
            scrollTrigger: {
                trigger: element.closest('.section'),
                start: 'top 80%',
                end: 'top 20%',
                scrub: 0.5,
                markers: false
            }
        });
    });

    // Parallax effect on section subtitles
    gsap.utils.toArray('.section-subtitle').forEach((element) => {
        gsap.from(element, {
            opacity: 0,
            y: 40,
            duration: 1,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: element.closest('.section'),
                start: 'top 75%',
                end: 'top 25%',
                scrub: 1,
                markers: false
            }
        });
    });

    // Parallax on narrative photos
    gsap.utils.toArray('.section-photo').forEach((photo) => {
        gsap.to(photo, {
            y: -60,
            duration: 1,
            ease: 'none',
            scrollTrigger: {
                trigger: photo,
                start: 'top bottom',
                end: 'top top',
                scrub: 1,
                markers: false
            }
        });
    });

    // Narrative text reveal with stagger
    gsap.utils.toArray('.narrative-text').forEach((text, index) => {
        gsap.from(text, {
            opacity: 0,
            y: 30,
            duration: 0.8,
            ease: 'power2.out',
            delay: index * 0.15,
            scrollTrigger: {
                trigger: text.closest('.narrative-block'),
                start: 'top 80%',
                end: 'top 30%',
                scrub: 0.3,
                markers: false
            }
        });
    });

    // Glass card parallax on Judas section
    gsap.utils.toArray('.glass-card.lg-panel').forEach((card, index) => {
        gsap.from(card, {
            opacity: 0,
            x: index % 2 === 0 ? -60 : 60,
            rotationY: index % 2 === 0 ? -15 : 15,
            duration: 1.2,
            ease: 'back.out',
            scrollTrigger: {
                trigger: card,
                start: 'top 70%',
                end: 'top 30%',
                scrub: 1.5,
                markers: false
            }
        });
    });

    // Tool card cascade reveal
    gsap.utils.toArray('.tool-card').forEach((card, index) => {
        gsap.from(card, {
            opacity: 0,
            scale: 0.8,
            y: 40,
            duration: 0.6,
            ease: 'back.out',
            delay: index * 0.08,
            scrollTrigger: {
                trigger: card.closest('.grid-4') || card.parentElement,
                start: 'top 80%',
                end: 'top 20%',
                scrub: 0.5,
                markers: false
            }
        });

        // Hover effect with momentum
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                y: -10,
                duration: 0.3,
                ease: 'power2.out'
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                y: 0,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });

    // CTA button pulse on scroll into view
    const ctaBtn = document.getElementById('ctaBtn');
    if (ctaBtn) {
        gsap.from(ctaBtn, {
            opacity: 0,
            scale: 0.8,
            y: 40,
            duration: 1,
            ease: 'elastic.out(1, 0.5)',
            scrollTrigger: {
                trigger: ctaBtn.closest('section'),
                start: 'top center',
                end: 'top top',
                scrub: 1,
                markers: false
            }
        });

        // Continuous pulse
        gsap.to(ctaBtn, {
            boxShadow: '0 0 60px rgba(255, 0, 60, 1), 0 0 100px rgba(255, 0, 60, 0.6)',
            duration: 1.5,
            repeat: -1,
            yoyo: true,
            ease: 'sine.inOut'
        });
    }

    // Scroll-driven rotation on core/planet
    const webglCanvas = document.getElementById('webgl-canvas');
    if (webglCanvas) {
        gsap.to(webglCanvas, {
            rotationZ: 360,
            duration: 60,
            repeat: -1,
            ease: 'none',
            scrollTrigger: {
                trigger: 'body',
                start: 'top top',
                end: 'bottom bottom',
                scrub: 0,
                markers: false
            }
        });
    }

    // Section background parallax
    gsap.utils.toArray('section').forEach((section) => {
        gsap.to(section, {
            backgroundPosition: '0% 100%',
            ease: 'none',
            scrollTrigger: {
                trigger: section,
                start: 'top bottom',
                end: 'bottom top',
                scrub: 1,
                markers: false
            }
        });
    });

    // Text reveal animations for hero section
    const heroTitle = document.getElementById('heroTitle');
    if (heroTitle) {
        // Already has keyframe animation, but add scroll-based interaction
        ScrollTrigger.create({
            trigger: heroTitle.closest('section'),
            start: 'top center',
            onEnter: () => {
                gsap.fromTo(heroTitle, 
                    { filter: 'blur(10px)', opacity: 0 },
                    { filter: 'blur(0px)', opacity: 1, duration: 1.5, ease: 'power2.out' }
                );
            }
        });
    }

    // Refresh ScrollTrigger after all animations load
    setTimeout(() => {
        ScrollTrigger.refresh();
    }, 500);
});

// Re-register plugins and refresh on window resize
window.addEventListener('resize', () => {
    ScrollTrigger.refresh();
});
