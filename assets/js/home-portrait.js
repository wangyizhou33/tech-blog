(() => {
    const trigger = document.querySelector('.home-portrait-trigger');
    const portrait = document.getElementById('home-portrait');

    function setOpen(open) {
        if (open === !portrait.hidden) return;

        if (open) {
            const source = trigger.getBoundingClientRect();
            const viewport = document.documentElement;
            portrait.style.setProperty('--portrait-x', `${source.left + (source.width - viewport.clientWidth) / 2}px`);
            portrait.style.setProperty('--portrait-y', `${source.top + (source.height - viewport.clientHeight) / 2}px`);
        }

        portrait.hidden = !open;
        trigger.setAttribute('aria-expanded', String(open));
    }

    trigger.addEventListener('pointerenter', event => {
        if (event.pointerType === 'mouse') setOpen(true);
    });

    trigger.addEventListener('pointerleave', event => {
        if (event.pointerType === 'mouse') setOpen(false);
    });

    trigger.addEventListener('click', () => setOpen(portrait.hidden));

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape') setOpen(false);
    });

    document.addEventListener('pointerdown', event => {
        if (!trigger.contains(event.target)) setOpen(false);
    });
})();
