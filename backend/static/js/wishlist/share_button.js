const shareButton = document.getElementById('share-button');
const shareModal = document.getElementById('share-modal');
const shareOptions = document.getElementById('share-options');
const copyLinkButton = document.getElementById('copy-link');
const linkCopied = document.getElementById('link-copied');

let autoCloseTimeout;

shareButton.addEventListener('click', () => {
    shareModal.classList.toggle('hidden');
    shareOptions.classList.remove('hidden');
    linkCopied.classList.add('hidden');
    clearTimeout(autoCloseTimeout);
});

copyLinkButton.addEventListener('click', () => {
    const shareUrl = shareButton.dataset.shareUrl;
    navigator.clipboard.writeText(shareUrl);
    shareOptions.classList.add('hidden');
    linkCopied.classList.remove('hidden');

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
