#! /usr/bin/env perl
use File::Basename;
$mypath = dirname($0);
use CGI;
$q = new CGI;
$p = $q->Vars;

print $q->header(-content_type => "application/json");

if (($p->{'lat'} ne "") && ($p->{'lon'} ne "")) {
    $lat = $p->{'lat'};
    $lon = $p->{'lon'};
    if (open($fh,">$mypath/location.json")) {
	print $fh qq({\n);
	print $fh qq("latd":"$lat",\n);
	print $fh qq("lond":"$lon"\n);
	print $fh qq(}\n);
	close($fh);

	if (open($fh,">","$mypath/../lightning/loc.py")) {
	    print $fh qq(location_lat = "$lat"\n);
	    print $fh qq(location_lon = "$lon"\n);
	    close($fh);
	}
    }
    print qq({"stat":"OK"});
}
else {
    print qq({"stat":"none"});
}
