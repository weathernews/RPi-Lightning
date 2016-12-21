#! /usr/bin/env perl
use File::Basename;
$mypath = dirname($0);
use CGI;
$q = new CGI;
print $q->header(-expires       => "now",
		 -content_type  => "application/json",
		 -charset       => "utf-8");

$ifcfg = `ifconfig eth0`;
if ($ifcfg =~ /HWaddr ([0-9a-f:]+)/) {
    @w = split(/:/,$1);
    $x3 = hex($w[3]);
    $x4 = hex($w[4]);
    $x5 = hex($w[5]);
    $sn = $x3 * 65536 + $x4 + 256 + $x5;
}
#if (open(F,">$mypath/../lightning/id.py")) {
#    print F qq(serial_number = "$sn"\n);
#    close(F);
#}

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

$sstr = '"' . join('","',@slst) . '"';
$mstr = join(",",@mlst);
$mstr =~ s/([^ 0-9a-zA-Z])/"%".uc(unpack("H2",$1))/eg;
$mstr =~ s/ /+/g;
$json = qq({"loc":);
open(PROC,"curl -s 'http://mwschat.wni.co.jp:8001/wlid.cgi?u=${sn}&m=${mstr}' |");
$_resp = "";
while (<PROC>){
    $_resp .= $_;
}
close(PROC);
if (open(J,"$mypath/location.json")) {
    while (<J>){
	$json .= $_;
    }
    close(J);
}
else {
    $json .= $_resp;

    if ($_resp =~ /"latd":([0-9\.\-]*)/) {
	$lat = $1;
    }
    if ($_resp =~ /"lond":([0-9\.\-]*)/) {
	$lon = $1;
    }
    if (open(F,">$mypath/../lightning/loc.py")) {
	print F qq(location_lat = "$lat"\n);
	print F qq(location_lon = "$lon"\n);
	close(F);
    }
}


$json .= qq(,"ssid":[$sstr]);
$json .= qq(,"serial":$sn);
$json .= "}";

print $json;
