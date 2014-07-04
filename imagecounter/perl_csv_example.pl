#!/usr/bin/perl
#
# Very simple PERL example script to read the image URLs from a input file and invoke the reverse lookup script.
#


open LIST, "<images.csv";

while ($url = <LIST>) {
    chomp($url);
    system('casperjs countbyurlbydate_silent.js "4/23/2014" "5/11/2014" "' . $url . '"');
    sleep(16);
}

close LIST;
