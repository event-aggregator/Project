"use strict";






var swipeContainer = document.querySelector(".swipe");
var allCards = document.querySelectorAll(".swipe--card");
var nope = document.getElementById("nope");
var love = document.getElementById("love");
var likedCards = [];

function initCards(card, index) {
  var newCards = document.querySelectorAll(".swipe--card:not(.removed)");

  newCards.forEach(function(card, index) {
    card.style.zIndex = allCards.length - index;
    card.style.transform =
      "scale(" + (20 - index) / 20 + ") translateY(-" + 30 * index + "px)";
    card.style.opacity = (10 - index) / 10;
  });

  swipeContainer.classList.add("loaded");
}

initCards();

allCards.forEach(function(el) {
  var hammertime = new Hammer(el);

  hammertime.on("pan", function(event) {
    el.classList.add("moving");
  });

  hammertime.on("pan", function(event) {
    if (event.deltaX === 0) return;
    if (event.center.x === 0 && event.center.y === 0) return;

    swipeContainer.classList.toggle("swipe_love", event.deltaX > 0);
    swipeContainer.classList.toggle("swipe_nope", event.deltaX < 0);

    var xMulti = event.deltaX * 0.03;
    var yMulti = event.deltaY / 80;
    var rotate = xMulti * yMulti;

    event.target.style.transform =
      "translate(" +
      event.deltaX +
      "px, " +
      event.deltaY +
      "px) rotate(" +
      rotate +
      "deg)";
  });


  hammertime.on("panend", function(event) {
    el.classList.remove("moving");
    let cards = document.querySelectorAll(".swipe--card:not(.removed)");
    swipeContainer.classList.remove("swipe_love");
    swipeContainer.classList.remove("swipe_nope");

      likedCards.push(cards[0].querySelector('.demo--name').value);
      console.log(likedCards);



    var moveOutWidth = document.body.clientWidth;
    var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

    event.target.classList.toggle("removed", !keep);

    if (keep) {
        likedCards.push(cards[0].querySelector('.demo--name').value);
      console.log(likedCards);
      event.target.style.transform = "";
    } else {

      console.log(1);
      var endX = Math.max(
        Math.abs(event.velocityX) * moveOutWidth,
        moveOutWidth
      );
      var toX = event.deltaX > 0 ? endX : -endX;
      var endY = Math.abs(event.velocityY) * moveOutWidth;
      var toY = event.deltaY > 0 ? endY : -endY;
      var xMulti = event.deltaX * 0.03;
      var yMulti = event.deltaY / 80;
      var rotate = xMulti * yMulti;

      event.target.style.transform =
        "translate(" +
        toX +
        "px, " +
        (toY + event.deltaY) +
        "px) rotate(" +
        rotate +
        "deg)";
      initCards();
    }
  });
});

function createButtonListener(love) {
  return function(event) {
    var cards = document.querySelectorAll(".swipe--card:not(.removed)");
    var moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    var card = cards[0];

    card.classList.add("removed");

    if (love) {
      card.style.transform = "translate(" + moveOutWidth + "px, -100px) rotate(-30deg)";
      likedCards.push(cards[0].querySelector('.demo--name').innerText);
      console.log(likedCards);
    } else {
      card.style.transform = "translate(-" + moveOutWidth + "px, -100px) rotate(30deg)";
    }
var xhr = new XMLHttpRequest();
var json = JSON.stringify({
  name: cards[0].querySelector('.demo--name').value,
    status: love
});
// 2. Конфигурируем его: GET-запрос на URL 'phones.json'
xhr.open('POST', '/abc', false);
xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
// 3. Отсылаем запрос
xhr.send(json);



    initCards();

    event.preventDefault();
  };

}



var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);

nope.addEventListener("click", nopeListener);
love.addEventListener("click", loveListener);

document.getElementsByTagName( "swipe--buttons" )[0].remove();


('.result').css('display', 'block');

if (likedCards.length !== 0) {
    likedCards.forEach(function(card, index) {
    ('.liked-cards').append('<li>' + likedCards[index] + '</li>');
    })
} else {
    ('.liked-cards').append("you've not liked anything :c");
}