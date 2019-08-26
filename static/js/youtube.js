function changeWidth(code, w) { // assuming that the code is common YT embed code
  return code.replace(/width=\"560\"/g, 'width=\"' + w + '\"');
}

function changeHeight(code, h) { // assuming that the code is common YT embed code
  return code.replace(/height=\"315\"/g, 'height=\"' + h + '\"');
}

// this is the "master function" where all the stuff happens. returns the adjusted
// code with the new dimensions
function scaleVideo(code) { // assuming that the code is common YT embed code
  // assumes that these are the starting dimensions
  startingWidth = 560;
  startingHeight = 315;

  marginW = calcFrontpageVideoMarginW();
  console.log("marginw: " + marginW);
  w = calcFrontpageVideoWidth(marginW);
  console.log("w: " + w);
  //ratio = startingHeight / startingWidth;
  h = calcFrontpageVideoHeight(w);
  console.log("h: " + h);
  return changeHeight(changeWidth(code, w), h);
}

function calcFrontpageVideoMarginW() {
  return 40;
  //return ($("iframe").outerWidth(true) - $("iframe").outerWidth(false)) / 2;
}
function calcFrontpageVideoWidth(marginW) {
  return (window.innerWidth - 5 * marginW) / 4; // 5 margins, 4 video elements
}
function calcFrontpageVideoHeight(width, defaultW = 560, defaultH = 315) {
  return defaultH / defaultW * width;
}
