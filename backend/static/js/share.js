const shareButton = document.getElementById('share-button');
const shareModal = document.getElementById('share-modal');
const copyLinkButton = document.getElementById('copy-link');
const shareOptions = document.getElementById('share-options');
const linkCopied = document.getElementById('link-copied');

let autoCloseTimeout;

shareButton.addEventListener('click', () => {
    shareModal.classList.toggle('hidden');
    shareOptions.classList.remove('hidden');
    linkCopied.classList.add('hidden');
    clearTimeout(autoCloseTimeout);
});

copyLinkButton.addEventListener('click', () => {
    navigator.clipboard.writeText(window.location.href);
    shareOptions.classList.add('hidden');
    linkCopied.classList.remove('hidden');

    // авто-закрытие через 3 секунды
    autoCloseTimeout = setTimeout(() => {
        shareModal.classList.add('hidden');
    }, 3000);
});

shareModal.addEventListener('click', (e) => {
    if (e.target === shareModal) {
        shareModal.classList.add('hidden');
        clearTimeout(autoCloseTimeout);
    }
});
