const sr = ScrollReveal({
    origin: 'top',
    distance: '60px',
    duration: 2500,
    delay: 400,
    // reset: true
})

sr.reveal(`.home-title, .about-container, .group-container, .contact-container, .slogan, .map, .footer`)
sr.reveal(`.home-description`, { delay: 500 })
sr.reveal(`.home-value`, { delay: 600 })
sr.reveal(`.home-button`, { delay: 700 })
sr.reveal(`.home-image`, { delay: 800, origin: 'bottom' })
sr.reveal(`.about-img`, { delay: 900, origin: 'left' })
sr.reveal(`.call`, { delay: 900})
sr.reveal(`.group-img`, { delay: 900, origin: 'right' })