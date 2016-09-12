# Raspberry Pi のセットアップ
- Raspbian をコピーして立ち上げ
- アップデート

    # apt-get update
    # apt-get upgrade
    # apt-get install emacs
    # apt-get install apache2

# pi アカウントのパスワード設定
    (reporter1101)

# apache の起動と終了

    # /etc/initd.apache2 (start|stop|restart)

# Wi-Fi AP 化

    https://frillip.com/using-your-raspberry-pi-3-as-a-wifi-access-point-with-hostapd/


 1. hostapd

    # apt-get install dnsmasq hostapd

 2. wlan0 に固定IP



# Wi-Fi パスフレーズ
    # wpa_passphrase [SSID] [PASSPHRASE]
    
