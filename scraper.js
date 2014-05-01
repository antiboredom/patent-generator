//var page = require('webpage').create();
//var system = require('system');
//var url = "https://www.google.com/search?tbm=pts&hl=en&q=" 
//var keyword = system.args[1];

//page.onConsoleMessage = function(msg) {
//console.log(msg);
//};


//page.open(encodeURI(url + keyword), function (status) {
//console.log(encodeURI(url + keyword));
//if (status !== "success") {
//console.log("Unable to access network");
//} else {
//setTimeout(function() {
//page.evaluate(function() {
//console.log(document.querySelectorAll('#ires h3').length);
//});
//}, 1000);
//}
////phantom.exit();
//});

//var getLinks = function(doc) {
//console.log('hi');
//var list = doc.querySelectorAll('#ires h3 a');

//for (var i = 0; i < list.length; ++i) {
//console.log((i + 1) + ": " + list[i].innerText);
//}
//};
//
//

var system = require('system');
var url = "https://www.google.com/?tbm=pts";
var url = "http://www.google.com/";
var url = "http://www.google.com/?tbm=pts&hl=en";
var url = "http://www.google.com/advanced_patent_search";
//var url = "http://patents.google.com";
var keyword = system.args[4];
//var url = "https://www.google.com/?tbm=pts#q=" + keyword + "&safe=off&tbm=pts";
var links = [];
var casper = require('casper').create();

function getLinks() {
  var links = document.querySelectorAll('h3.r a');
  return Array.prototype.map.call(links, function(e) {
    return e.getAttribute('href');
  });
}

casper.start(url, function() {
  this.fill('form[action="/patents"]', { as_q: "drone" }, true);
});

//casper.waitFor(function check() {
  //return this.evaluate(function() {
    //return document.querySelectorAll('h3.r a').length > 0;
  //});
//}, function then() {
  //links = this.evaluate(getLinks);
//});

casper.then(function() {
  links = this.evaluate(getLinks);
});
// now search for 'phantomjs' by filling the form again
//this.fill('form[action="/search"]', { q: 'phantomjs' }, true);
//});

//casper.then(function() {
//// aggregate results for the 'phantomjs' search
//links = links.concat(this.evaluate(getLinks));
//});

casper.run(function() {
  // echo results in some pretty fashion
  this.echo(links.length + ' links found:');
  this.echo(' - ' + links.join('\n - ')).exit();
});
