#! /usr/bin/env perl
use CGI;
$q = new CGI;
$p = $q->Vars;
print $q->header(-content_type => "application/json");
if ($p->{'ssid'} ne "") {
    open(JSON,">network.json");
    print JSON << "+++";
{
"ssid":"$p->{'ssid'}",
"passphrase":"$p->{'passphrase'}",
"addrtype":"$p->{'addrtype'}",
"ipaddr":"$p->{'ipaddr'}",
"netmask":"$p->{'netmask'}",
"gateway":"$p->{'gateway'}",
"proxy":"$p->{'proxy'}"
}
+++
	;
    close(JSON);
    print qq({"stat":"OK"});
}
else {
    print qq({"stat":"none"});
}
