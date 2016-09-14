#! /usr/bin/env perl
$ENV{'TZ'} = 'Asia/Tokyo';
use Time::Local;
use POSIX qw(strftime);
use File::Basename;
$mypath = dirname($0);
use CGI;
$q = new CGI;
print $q->header(-expires	=> "now",
		 -content_type	=> "application/json",
		 -charset	=> "utf-8");
$spld = "$mypath/../lightning/spool";
if (opendir(D,$spld)) {
    @files = sort grep ! /^\./, readdir(D);
    closedir(D);
}

%buf = ();
$lastf = pop(@files);
if (open(F,"$spld/$lastf")) {
    while (<F>){
	@w = split(/[,\r\n]/,$_);
	next if ($w[1] !~ /lightning/);
	$t0 = $w[0];
	my($yy,$mm,$dd,$hh,$mn,$ss) = split(/[^0-9]+/,$t0);
	my $tm = timelocal($ss,$mn,$hh,$dd,$mm-1,$yy-1900);
	my $ta = int($tm / 600);
	my $tb = int($tm % 600);
	$ta++ if ($tb > 0);
	my $tx = $ta * 600;
	my $ts = strftime("%Y-%m-%d.%T",localtime($tx));
	$buf{$ts}++;
    }
    close(F);
}

$delim = "";
print "[";
foreach $ts (reverse sort keys %buf) {
    print qq(${delim}{"t":"$ts","n":$buf{$ts}});
    $delim = ",\n";
}
print "]";


    
