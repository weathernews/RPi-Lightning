#! /usr/bin/env perl
use File::Basename;
$mypath = dirname($0);
use CGI;
$q = new CGI;
print $q->header(-expires       => "now",
		 -content_type  => "application/json",
		 -charset       => "utf-8");

if (open($fh,"$mypath/../lightning/id.py")) {
    while (<$fh>) {
	if (/serial_number = \"(.*)\"/) {
	    $sn = $1;
	}
    }
    close($fh);
}

$mdtm = (stat("$mypath/wlan.txt"))[9];
if ((time - $mdtm) > (86400 * 30)) {
    open(OUT,">$mypath/wlan.txt");
    open(PROC, "sudo iwlist wlan0 scan|");
    @mlst = ();
    @slst = ();
    while (<PROC>) {
	if (/Address: ([0-9A-F:]{17})/) {
	    $ssid = "";
	    $maca = $1;
	    push(@mlst, "$maca");
	}
	if (/ESSID:"(.*)"/) {
	    $ssid = $1;
	    print OUT "$maca\t$ssid\n";
	    push(@slst, "$ssid") if ($ssid ne "");
	}
    }
    close(PROC);
    close(OUT);
}
else {
    open($fh,"$mypath/wlan.txt");
    while (<$fh>) {
	($maca,$ssid) = split(/[\t\r\n]/,$_);
	push(@mlst, "$maca");
	push(@slst, "$ssid") if ($ssid ne "");
    }
    close($fh);
}

$sstr = '"' . join('","',@slst) . '"';

$json = qq({"loc":);
$mdtm = (stat("$mypath/location.json"))[9];
if (((time - $mdtm) < 86400) && (open(J,"$mypath/location.json"))) {
    while (<J>){
	s/"lat"/"latd"/;
	s/"lon"/"lond"/;
	$json .= $_;
    }
    close(J);
}
else {
    $mstr = join(",",@mlst);
    $mstr =~ s/([^ 0-9a-zA-Z])/"%".uc(unpack("H2",$1))/eg;
    $mstr =~ s/ /+/g;
    open(PROC,"curl -s 'http://mwschat.wni.co.jp:8001/wlid.cgi?u=${sn}&m=${mstr}' |");
    $_resp = "";
    while (<PROC>){
	$_resp .= $_;
    }
    close(PROC);

    $json .= $_resp;

    if ($_resp =~ /"latd":([0-9\.\-]*)/) {
	$lat = $1;
    }
    if ($_resp =~ /"lond":([0-9\.\-]*)/) {
	$lon = $1;
    }
    if (open($fh,">","$mypath/../lightning/loc.py")) {
	print $fh qq(location_lat = "$lat"\n);
	print $fh qq(location_lon = "$lon"\n);
	close($fh);
    }
    if (open($fh,">$mypath/location.json")) {
	print $fh qq({\n);
	print $fh qq("latd":"$lat",\n);
	print $fh qq("lond":"$lon"\n);
	print $fh qq(}\n);
	close($fh);
    }
}


$json .= qq(,"ssid":[$sstr]);
$json .= qq(,"serial":"$sn");
$json .= "}";

print $json;
