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
function scaleClip(code) { // assuming that the code is common YT embed code
  // assumes that these are the starting dimensions

  marginW = calcFrontpageClipMarginW();
  console.log("marginw: " + marginW);
  w = calcFrontpageClipWidth(marginW);
  console.log("w: " + w);
  //ratio = startingHeight / startingWidth;
  h = calcClipHeight(w);
  console.log("h: " + h);
  return changeHeight(changeWidth(code, w), h);
}

function calcFrontpageClipMarginW() {
  return 40;
  //return ($("iframe").outerWidth(true) - $("iframe").outerWidth(false)) / 2;
}
/*function calcFrontpageClipWidth(marginW) {
  return (window.innerWidth - 5 * marginW) / 4; // 5 margins, 4 clip elements
}
function calcFrontpageClipHeight(width, defaultW = 560, defaultH = 315) {
  return defaultH / defaultW * width;
} */

function calcFrontpageClipWidth(marginW) {
  return window.innerWidth - 500 - 2 * marginW ; // 5 margins, 4 clip elements
}
function calcClipHeight(width) {
  return 1 / (getWidthToHeightRatio() / width);
}

function getCidFromEmbedLink(code) {
  var srcStrStart = code.indexOf('src=\"https://www.youtube.com/embed/') + 35;
  var id = code.substr(srcStrStart, code.indexOf('frameborder') - srcStrStart - 2) // from the space and quote
  return id; 
}

function generateThumbnailUrl(cid, isSmall) {
  if (isSmall)
    return 'https://img.youtube.com/vi/' + cid + '/default.jpg';
  return 'https://img.youtube.com/vi/' + cid + '/0.jpg';
}