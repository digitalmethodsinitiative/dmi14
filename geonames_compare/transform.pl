#!/usr/bin/perl

%file1 = ();

while ($ARGV = shift @ARGV) {
  open ARGV, $ARGV;
  LINE: while (defined($_ = <ARGV>)) {
    $l = $_;
    if ($l =~ m/^(.+)\t/) {
	$w = $1;
    } 
    $seen{$w} .= @ARGV;
    if ($seen{$w} =~ /10/) {
	print $file1{$w} . "\t" . $l;
	#print $l;
    } elsif (not exists $file1{$w}) {
    	# l uit file1 bewaren!
	chomp($l);
	$file1{$w} = $l;
    }
  }
}
