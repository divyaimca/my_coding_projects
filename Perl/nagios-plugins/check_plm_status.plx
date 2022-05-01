#!/usr/bin/perl
use warnings;
####################################################################
# Purpose : To check PLM status ( Tested With Seimens TC 2005 )
#    It checks mux and dsp status and give the feed back to nagios
# to show the status in nagios webpage.
#####################################################################

$muxs = "/user/omfprod/bin/muxstat";
$dsps = "/user/omfprod/bin/dspstat";

system "$dsps > /dev/null";
$dspr = $?; 
#print $dspr;
system "$muxs > /dev/null";
$muxr = $?;
#print $muxr;
if ( $dspr ==0 && $muxr ==0 ){
  my $time = `$muxs | grep -i Up`;
        chomp($time);
        print "OK : PLM is $time\n";
        exit 0;
	}

if ( $dspr ==0 && $muxr !=0){
	print "Critical : PLM is Down (Mux is down)\n";
	exit 2;
	}
	
if ( $dspr !=0 && $muxr ==0){
	print "Critical : PLM is Down (Dispatcher is down)\n";
	exit 2;
	}
if ( $dspr !=0 && $muxr !=0){
	print "Critical : PLM is Down (Both mux and dispatcher are down)\n";
	exit 2;
	}
