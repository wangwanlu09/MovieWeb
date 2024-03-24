let movieSlideIndex = 0; 
  let giftSlideIndex = 0;  

  function moveSlide(step) {
      const slides = document.querySelectorAll('.carousel-slide.movie-slide .card2'); 
      const totalSlides = slides.length;
      const slideWidth = slides[0].getBoundingClientRect().width + 16; 

   
      movieSlideIndex = (movieSlideIndex + step + totalSlides) % totalSlides;

      
      const moveX = -(slideWidth * movieSlideIndex);
      document.querySelector('.carousel-slide.movie-slide').style.transform = `translateX(${moveX}px)`;
  }

  function giftSlide(step) {
      const slides = document.querySelectorAll('.carousel-slide.gift-slide .card'); 
      const totalSlides = slides.length;
      const slideWidth = slides[0].getBoundingClientRect().width + 16; 

      
      giftSlideIndex = (giftSlideIndex + step + totalSlides) % totalSlides;

     
      const moveX = -(slideWidth * giftSlideIndex);
      document.querySelector('.carousel-slide.gift-slide').style.transform = `translateX(${moveX}px)`;
  }