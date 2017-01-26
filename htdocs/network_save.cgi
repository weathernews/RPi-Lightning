#! /usr/bin/env perl
use File::Basename;
$mypath = dirname($0);
use CGI;
$q = new CGI;
$p = $q->Vars;

if (($p->{'ssid'} ne "") || ($ARGV[0] eq "init")) {
    if (open(JSON,">$mypath/network.json")) {
	print JSON << "+++";
{
"serial":"$sn",
"ssid":"$p->{'ssid'}",
"passphrase":"****",
"addrtype":"$p->{'addrtype'}",
"ipaddr":"$p->{'ipaddr'}",
"netmask":"$p->{'netmask'}",
"gateway":"$p->{'gateway'}",
"proxy":"$p->{'proxy'}"
"nameserver":"$p->{'nameserver'}"
}
+++
	;
close(JSON);
    }
}

open($fh,">","$mypath/../piset/np.txt");
print $fh $p->{'passphrase'};
close($fh);

print $q->header(-content_type => "application/json");
if ($p->{'ssid'} ne "") {
    system("perl $mypath/../piset/mkcfg.pl");
    system("sudo $mypath/../piset/config/set_config.sh wifi_client");
    print qq({"stat":"OK"});
}
else {
    print qq({"stat":"none"});
}
