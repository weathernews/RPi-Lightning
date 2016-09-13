# Pi-Lightning

Raspberry Pi と、AS3935 を用いた雷センサの制作

1. Raspberry Pi の環境設定

Raspberry Pi の初期設定については、[README-raspi-mac.md](https://github.com/weathernews/Pi-Lightning/blob/master/README-raspi-mac.md) をご覧ください。

2. AS3935 雷センサーと、 Raspberry Pi の接続

 ![配線図](https://github.com/weathernews/Pi-Lightning/blob/master/htdocs/img/wire.png)


3. パッケージのインストール

このパッケージを、/home/pi 以下にダウンロードして下さい。

`git clone https://github.com/weathernews/Pi-Lightning.git`

Raspberry Pi が起動した時に、プログラムを自動で起動できるように、/etc/rc.local に以下の行を追加します。

    /home/pi/Pi-Lightning/lightning/rec.py

