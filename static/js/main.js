document.addEventListener('DOMContentLoaded', function () {
    // 1. Staggered List Animation
    const listItems = document.querySelectorAll('.feedback-item');

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add a slight delay based on index for the stagger effect
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100); // 100ms delay per item

                // Stop observing once visible
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    listItems.forEach(item => {
        observer.observe(item);
    });

    // 2. Chart Initialization
    const ctx = document.getElementById('sentimentChart');
    if (ctx) {
        // Global defaults
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Outfit', sans-serif";

        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Sentiment Distribution',
                            data: data.data,
                            backgroundColor: [
                                '#34d399', // Positive - Green (Tailwind emerald-400)
                                '#94a3b8', // Neutral - Gray (Tailwind slate-400)
                                '#fb7185'  // Negative - Red (Tailwind rose-400)
                            ],
                            borderColor: 'transparent',
                            hoverOffset: 10,
                            borderRadius: 5,
                            spacing: 5
                        }]
                    },
                    options: {
                        responsive: true,
                        cutout: '70%',
                        animation: {
                            animateScale: true,
                            animateRotate: true,
                            duration: 2000,
                            easing: 'easeOutQuart'
                        },
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 20,
                                    usePointStyle: true,
                                    font: {
                                        size: 12
                                    }
                                }
                            }
                        }
                    }
                });
            });
    }
});
