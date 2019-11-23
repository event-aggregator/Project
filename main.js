$(document).ready(function() {

    var animating = false;
    var cardsCounter = 0;
    var numOfCards = 10;
    var decisionVal = 80;
    var pullDeltaX = 0;
    var deg = 0;
    var $card, $cardReject, $cardLike;
    var likedCards = [];
    var rejectedCards = [];
    
    function pullChange() {
      animating = true;
      deg = pullDeltaX / 10;
      $card.css("transform", "translateX("+ pullDeltaX +"px) rotate("+ deg +"deg)");
  
      var opacity = pullDeltaX / 100;
      var rejectOpacity = (opacity >= 0) ? 0 : Math.abs(opacity);
      var likeOpacity = (opacity <= 0) ? 0 : opacity;
      $cardReject.css("opacity", rejectOpacity);
      $cardLike.css("opacity", likeOpacity);
    };
  
    function release() {
      if (pullDeltaX >= decisionVal) {
        $card.addClass("to-right");
        likedCards.push($card[0].querySelector('.demo__card__name').innerText);
        console.log(likedCards);
      } else if (pullDeltaX <= -decisionVal) {
        $card.addClass("to-left");
        rejectedCards.push($card[0].querySelector('.demo__card__name').innerText);
        console.log(rejectedCards);
      }
  
      if (Math.abs(pullDeltaX) >= decisionVal) {
        cardsCounter++;
        $card.addClass("inactive");
        if (cardsCounter === numOfCards) {
          $('.result').css('display', 'block');
          
          if (likedCards.length !== 0) {
            likedCards.forEach(function(card, index) {
              $('.liked-cards').append('<li>' + likedCards[index] + '</li>');
            })
          } else {
            $('.liked-cards').append("you've not liked anything :c");
          }
  
          if (rejectedCards.length !== 0) {
            rejectedCards.forEach(function(card, index) {
              $('.rejected-cards').append('<li>' + rejectedCards[index] + '</li>');
            })
          } else {
            $('.rejected-cards').append("you've not rejected anything :c")
          }
        }
      }
  
      if (Math.abs(pullDeltaX) < decisionVal) {
        $card.addClass("reset");
      }
  
      setTimeout(function() {
        $card.attr("style", "").removeClass("reset")
          .find(".demo__card__choice").attr("style", "");
  
        pullDeltaX = 0;
        animating = false;
      }, 300);
    };
  
    $(document).on("mousedown touchstart", ".demo__card:not(.inactive)", function(e) {
      if (animating) return;
  
      $card = $(this);
      $cardReject = $(".demo__card__choice.m--reject", $card);
      $cardLike = $(".demo__card__choice.m--like", $card);
      var startX =  e.pageX || e.originalEvent.touches[0].pageX;
  
      $(document).on("mousemove touchmove", function(e) {
        var x = e.pageX || e.originalEvent.touches[0].pageX;
        pullDeltaX = (x - startX);
        if (!pullDeltaX) return;
        pullChange();
      });
  
      $(document).on("mouseup touchend", function() {
        $(document).off("mousemove touchmove mouseup touchend");
        if (!pullDeltaX) return; // prevents from rapid click events
        release();
      });
    });
  
  });