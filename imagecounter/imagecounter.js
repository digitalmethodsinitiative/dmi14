/*
 * This script requires CasperJS to run: http://casperjs.org/
 *
 * Google reverse search images by URL (and date period) and return the nr. of results
 *
 * parameters: datefrom, dateto, url
 * dates are formatted month/day/year
 *
 * Example:
 * casperjs imagecounter.js "4/1/2014" "5/1/2014" images.txt 
 *
 * Notice there is a big sleep statements in the script to prevent hitting a captcha.
 * Add a sleep of about 15 seconds between invocations to prevent captcha problems.
 *
 * Version 4 july 2014 - DMI summer school
 *
 */

var utils = require('utils');
var stdin = require('system').stdin;

var total;

var links = [];
var found_it = 0;
        //userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20130404 Firefox/23.0"
var casper = require("casper").create({
    waitTimeout: 500000,
    pageSettings: {
        userAgent: 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0'
    }
});

function getLinks() {
    var links = document.querySelectorAll('a');
    return Array.prototype.map.call(links, function(e) {
        return e.getAttribute('href')
    });
}


if (casper.cli.args.length === 0) {
    casper
        .echo("Usage: $ casperjs imagecounter.js date1 date2 url")
        .exit(1)
    ;
}

var cd_min = casper.cli.args[0];
var cd_max = casper.cli.args[1];

casper.start("http://google.com/", function() {
	this.open('http://www.google.com/searchbyimage?image_url=' + casper.cli.args[2], function() {
	});
});

casper.then(function() {
    var partial = this.fetchText("#resultStats");
	var patt=/About ([\.,0-9]*) results/;
	var matches;	


	   if (matches = partial.match(patt)) {
		   total = matches[1].replace(/,/g, '');
	   } else {
           casper.echo(casper.cli.args[2] + ',' + cd_min + ',' + cd_max + ',' + '0' + ',' + '0');
           casper.capture('screenshot-final.png', {
              top: 1,
              left: 1,
              width: 1024,
              height: 1800
           });
           this.exit();
       }

});

var newurl;

casper.then(function() {
    // get string till &tbm=
    // add ,cdr:1,cd_min:6/2/2014,cd_max:7/2/2014
    var url = this.getCurrentUrl();
    //casper.echo(url);
    var index = url.lastIndexOf('&');
    newurl = url.substr(0, index) + encodeURIComponent(',cdr:1,cd_min:' + cd_min + ',cd_max:' + cd_max);
    newurl += url.substr(index);
    //casper.echo(newurl);
});

// sleep 15 seconds
casper.then(function() {
    var seconds = new Date().getTime() / 1000;
    casper.waitFor(function() {
        var now = new Date().getTime() / 1000;
        return (now > seconds + 15);
    },function() {
    });
});

casper.then(function() {
    //casper.echo("opening new url ...");
	this.open(newurl, function() {
	});
});

// sleep 4 seconds
casper.then(function() {
    var seconds = new Date().getTime() / 1000;
    casper.waitFor(function() {
        var now = new Date().getTime() / 1000;
        return (now > seconds + 4);
    },function() {
    });
});

casper.then(function() {
    // <div id="resultStats">Ongeveer 744 resultaten<nobr>

    var partial = this.fetchText("#resultStats");
	var patt=/About ([\.,0-9]*) results/;
	var matches;


	if (matches = partial.match(patt)) {
        this.echo(casper.cli.args[2] + ',' + cd_min + ',' + cd_max + ',' + total + ',' + matches[1].replace(/,/g, ''));
	} else {
        this.echo(casper.cli.args[2] + ',' + cd_min + ',' + cd_max + ',' + total + ',' + '0');
    }

});

/*
casper.then(function() {
	var patt=/ ([\.,0-9]*) results/;
	var matches;

	   if (matches = this.getHTML().match(patt)) {
           this.echo(casper.cli.args[2] + ',' + cd_min + ',' + cd_max + ',' + total + ',' + matches[1].replace(/,/g, ''));
	   } else {
           this.echo(casper.cli.args[2] + ',' + cd_min + ',' + cd_max + ',' + total + ',' + '0');
       }

});

*/

/*
casper.then(function() {
    casper.waitFor(function() {
        return this.exists("#resultStats");
    },function() {
        casper.echo("got result stats ...");
        casper.echo(this.fetchText("#resultStats"));
    });
});
*/

casper.then(function() {
   this.capture('screenshot-final.png', {
        top: 1,
        left: 1,
        width: 1024,
        height: 1800
    });
});

casper.run(function() {
	this.exit();
});

