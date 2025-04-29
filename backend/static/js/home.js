const song = document.getElementById('song');

function playSong() {
    song.play(); // Запускает песню
}

function pauseSong() {
    song.pause(); // Останавливает песню, когда курсор уходит
    <!-- song.currentTime = 0; // Сбрасывает песню в начало -->
}
