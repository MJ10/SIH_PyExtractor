$(document).ready(function() {

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