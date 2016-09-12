#! /usr/bin/env perl
use CGI;
$q = new CGI;
print $q->header(-content_type => "application/json");
$ssid = $q->param("ssid");
$pass = $q->param("passphrase");
if ($ssid ne "") {
    open(JSON,">network.json");
    print JSON qq({"ssid":"$ssid","passphrase":"$pass"});
    close(JSON);
    print qq({"stat":"OK"});
}
else {
    print qq({"stat":"none"});
}
