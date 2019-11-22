function getWidthToHeightRatio() {
  return 560./315.
}

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

  marginW = calcFrontpageVideoMarginW();
  console.log("marginw: " + marginW);
  w = calcFrontpageVideoWidth(marginW);
  console.log("w: " + w);
  //ratio = startingHeight / startingWidth;
  h = calcVideoHeight(w);
  console.log("h: " + h);
  return changeHeight(changeWidth(code, w), h);
}

function calcFrontpageVideoMarginW() {
  return 40;
  //return ($("iframe").outerWidth(true) - $("iframe").outerWidth(false)) / 2;
}
/*function calcFrontpageVideoWidth(marginW) {
  return (window.innerWidth - 5 * marginW) / 4; // 5 margins, 4 video elements
}
function calcFrontpageVideoHeight(width, defaultW = 560, defaultH = 315) {
  return defaultH / defaultW * width;
} */

function calcFrontpageVideoWidth(marginW) {
  return window.innerWidth - 300 - 2 * marginW ; // 5 margins, 4 video elements
}
function calcVideoHeight(width) {
  return 1 / (getWidthToHeightRatio() / width);
}

function getVidFromEmbedLink(code) {
  var srcStrStart = code.indexOf('src=\"https://www.youtube.com/embed/') + 35;
  var id = code.substr(srcStrStart, code.indexOf('frameborder') - srcStrStart - 2) // from the space and quote
  return id; 
}

function generateThumbnailUrl(vid, isSmall) {
  if (isSmall)
    return 'https://img.youtube.com/vi/' + vid + '/default.jpg';
  return 'https://img.youtube.com/vi/' + vid + '/0.jpg';
}