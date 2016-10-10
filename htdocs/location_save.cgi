#! /usr/bin/env perl
use File::Basename;
$mypath = dirname($0);
use CGI;
$q = new CGI;
$p = $q->Vars;

print $q->header(-content_type => "application/json");

if (($p->{'lat'} ne "") && ($p->{'lon'} ne "")) {
    if (open(JSON,">$mypath/location.json")) {
	$lat = $p->{'lat'};
	$lon = $p->{'lon'};
	print JSON << "+++";
{
"lat":"$lat",
"lon":"$lon"
}
+++
	;
close(JSON);

	if (open(F,">$mypath/../lightning/loc.py")) {
	    print F qq(location_lat = "$lat"\n);
	    print F qq(location_lon = "$lon"\n);
	    close(F);
	}
    }
    print qq({"stat":"OK"});
}
else {
    print qq({"stat":"none"});
}
