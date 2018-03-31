$(document).ready(function() {
	particlesJS.load('particles-js', '../server/static/particlesjs.json', function() {
	console.log('particles.json config loaded');
	});

    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
      }); 
    $('.carousel.carousel-slider').height($(document).height());  

    setTimeout(function() {
        autoplay();
    }, 6000);   

}); 

function autoplay() {
    $('.carousel').carousel('next');
    setTimeout(autoplay, 6500);
}
