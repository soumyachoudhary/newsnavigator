function myFunction() {

  var element = document.body;
  element.classList.toggle("dark-mode");

  var TheCards = document.getElementsByClassName("card")
  for (var i=0; i<TheCards.length; i++) {
    (TheCards[i]).classList.toggle("dark-mode-input");
  }


  (document.getElementsByClassName("form-control")[0]).classList.toggle("dark-mode-input");
  // document.getElementById("container")[0].classList.toggle("dark-card");

}

// $(document).ready(function () {
        		
//   function resizeMe() {
//     //Grab the element to resize:
//     var element = $('.resized');
//     //Grab the current windows's width and height:
//     var w_width = $(window).width();
//     var w_height = $(window).height();

//     //Grab the element to resize's width and height:
//     var resized_width = element.width();
//     var resized_height = element.height();

//     /*
//         	Set the top and left value:
//         	This is the "top-left" corner where the div will be place:
//         		Top: So, this will be (windows' height divided by 2), then substract the (div's height divided by 2)
//         		Left: So, this will be (windows' width divided by 2), then substract the (div's width divided by 2)
//      */

//     //Top:
//     var top_position = (w_height / 2) - (resized_height / 2);
//     //Left:
//     var left_position = (w_width / 2) - (resized_width / 2);

//     element.css({'top': top_position, 'left': left_position});
//   }

//   //Call the 'resizeMe()' function so that it runs immediately when the windows loads:
//   resizeMe();

//   //Then call the 'resizeMe()' function when the windows is resized:
//   $(window).resize(function () {
//     //Invoke the function
//     resizeMe();
//   });
//  });