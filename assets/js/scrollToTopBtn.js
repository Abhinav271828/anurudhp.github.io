var scrollToTopBtn = $('#scrollToTopBtn');
var scrollToBottomBtn = $('#scrollToBottomBtn');

$(window).scroll(function() {
  const tolerance = 300;
  if ($(window).scrollTop() > tolerance) {
    scrollToTopBtn.addClass('show');
  } else {
    scrollToTopBtn.removeClass('show');
  }

  if($(window).scrollTop() + $(window).height() < $(document).height() - tolerance) {
    scrollToBottomBtn.addClass('show');
  } else {
    scrollToBottomBtn.removeClass('show');
  }
});

scrollToTopBtn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:0}, '300');
});
scrollToBottomBtn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:$(document).height()}, '300');
});
