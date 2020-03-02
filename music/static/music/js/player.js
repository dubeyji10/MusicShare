// If play button clicked, change pp.src to pause button and call song.play(). If pause button clicked, change pp.src to play button and call song.pause().let playing = true;function playPause() {
  if (playing) {
    const song = document.querySelector('#song'),
    thumbnail = document.querySelector('#thumbnail');    pPause.src = "./assets/icons/pause.png"; //this will change the 
    Play button to a Pause button
    thumbnail.style.transform = "scale(1.15)"; //this will slightly 
    zoom in the album cover for a cool effect    song.play(); //this will play the audio track
    playing = false;
  } else {
    pPause.src = "./assets/icons/play.png"
    thumbnail.style.transform = "scale(1)" //this will slightly 
    zoom in the album cover for a cool effect
 
    song.pause();
    playing = true;
  }
}
