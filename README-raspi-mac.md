# Raspberry Pi のセットアップ

Mac (MacBook Air など）を用いた、Raspberry Pi のセットアップについて説明します。

1. Raspbian のダウンロード

  * Raspbian OS を公式サイトからダウンロードしてください。

    https://www.raspberrypi.org/downloads/

  * RASPBIAN のなかの LITE というGUIを含まないパッケージで OK です。

    2016-05-27-raspbian-jessie-lite.zip

  * ダウンロードして、展開すると、2016-05-27-raspbian-jessie-lite.img ファイルができます。

    `% unzip 2016-05-27-raspbian-jessie-lite.zip`




2. microSD カードの準備

  * SDカードを、SDカードスロットに挿入します。

  * 自動的にマウントされる場合は、マウントを解除してください。
      アプリケーション > ユーティリティ > ディスクユーティリティを使うか、コマンドの場合は

      まず、df コマンドでデバイス名を確認して、（見えないときは、挿しなおしてみてください）
      デバイス名は disk1 とか disk2 とかです。

      `# df`
>      Filesystem    512-blocks      Used Available Capacity  iused    ifree %iused  Mounted on
>      /dev/disk0s2   975425848 782000760 192913088    81% 97814093 24114136   80%   /
>      devfs                371       371         0   100%      642        0  100%   /dev
>      map -hosts             0         0         0   100%        0        0  100%   /net
>      map auto_home          0         0         0   100%        0        0  100%   /home
>      /dev/disk2s1    30302208      4352  30297856     1%        0        0  100%   /Volumes/NO NAME


     そのデバイスをアンマウントします。

      `# diskutil unmount /dev/disk2s1`


3. dd コマンドによる書き込み

  * dd コマンドは、フォーマットやパーティション情報も全部書き込んでくれるので、SD カードをフォーマットし直す必要はありません。

  * dd コマンドのオプションで bs= （ブロックサイズの指定）は、デフォルト値が歴史的経緯で小さい（512バイト）ので、1m 程度のサイズを指定しないと処理に時間がかかります。

  * dd で指定する出力デバイス of= は、SDカードのデバイスを指定しますが、上記で出てきた /dev/disk2 は、ブロックデバイスといい、ディスクとしてアクセスするときはこれを使いますが、dd コマンドは、先頭からすべてをまとめて書き込むので、逆にバッファリングされて遅くなってしまいます。このような場合には、キャラクタデバイスである、/dev/rdisk2 を指定します。

  * /dev/disk2s1 というのは、disk2 のパーティション 1 ですが、/dev/disk2 というのは、ディスク全体です。このイメージファイルはディスク全体に書き込みます。

  * デバイスに直接書き込むためには、root 権限が必要です

    以上、まとめると、次のコマンドラインになります。なお、まちがえて違うデバイスに書き込んだりすると、Mac 側の OS を破壊したりすることがあるので、出力デバイス名はとくに慎重に。

    `# dd bs=1m if=2016-05-27-raspbian-jessie-lite.img of=/dev/rdisk2`

    実行には時間がかかります。


説明が長くなりましたが、実際に必要なコマンドは、２，３ステップほどです。

dd コマンドの実行（OSイメージの書き込み）が成功すると、自動的に再マウントされて、中が見えるようになっていれば OK です。（そうでなければ、書き込みに失敗しています）あらためて、マウントを解除（ディスクの取り出し）をして、SD カードを取り出します。マウント解除は、ディスクユーティリティまたは次のコマンドで

    `% diskutil eject /dev/disk2`


なお、SD カードのライトプロテクトノッチの位置によって、書き込めない場合があるようです。以下の記事を参考にしてください。

http://kanonji.info/blog/2013/11/26/macbook-pro%E3%81%AEsd%E3%82%AB%E3%83%BC%E3%83%89%E3%82%B9%E3%83%AD%E3%83%83%E3%83%88%E3%81%A3%E3%81%A6%E6%9B%B8%E3%81%8D%E8%BE%BC%E3%81%BF%E3%83%AD%E3%83%83%E3%82%AF%E3%81%8C%E3%81%8B%E3%81%8B/

dd コマンドは、unix の初期からあるコマンドなので、コマンドラインオプションの与え方が、他のコマンドと若干違います。昔は、テーブドライブへの読み書き等で使われていました。



4. Raspberry Pi に SD カードをセットして、起動します。

 * ネットワークケーブルを接続します。
 * 電源（USB）を接続します。
 * LED が点滅すれば、多分起動中。だめだと、つきっぱなしとか、点灯しないとかになります。
 * ネットワークは、DHCP でアドレスが付与されることが期待されていますが、自動的に付与されたアドレスを調べるには、以下の手順で確認します。（これは、手元の Mac 上でターミナルを開いて行います）

 ** まず、以下のスクリプトで、自分の arp テーブルに、全端末登録します。

```allping.sh

#! /bin/sh
if [ "$1" != "" ]; then
    NET=$1
else
    NET="10.0.1"	# デフォルトは適当に変更してください。
fi
for i in `seq 1 254`
do
    ping -c 1 -t 1 ${NET}.$i &
done

```


 ** arp コマンドにより、Raspberry Pi のMACアドレスを検索します。

        `% arp -a | grep 'b8:27:eb'`
>        ? (10.0.1.26) at b8:27:eb:d0:a5:43 on en0 ifscope [ethernet]

    これで、IP アドレスが分かりました。


5) Raspberry Pi にログイン

```

% ssh pi@10.0.1.26                     # 上記でわかった IP アドレス
pi@10.0.1.26's password: [raspberry]   # 初期パスワード。入力は表示されません。

```

    パッケージをアップデートします。

```

# apt-get update
# apt-get upgrade


```

時間かかるので、気長に待ちます。


6) カレンダ時計の設定

* タイムゾーンの設定

  ** raspi-config - Internationalisation Options - Change Timezone から "Asia/Tokyo" にします。

* /etc/ntp.conf に以下を追加

    `pool ntp.nict.jp iburst`





6) ライブラリのセットアップ

以下のサイトを参考にさせていただきました。（ナチュラル研究所、石川様ありがとうございます）

http://www.ishikawa-lab.com/RasPi_lightning.html

* 雷センサは AS3935 というチップを使用しています。
* 上記手順に従い以下をおこなっていきます。

** I2C のセットアップ

`raspi-config` というコマンドを使用して設定します。

    + raspi-config
      ++ Advanced Options
        +++ A6 I2C - Enabled に

パッケージをインストールします。

`% sudo apt-get -y install python-smbus i2c-tools python-rpi.gpio`

`% sudo apt-get -y install dnsmasq hostapd`


8. Apache の設定

`% sudo apt-get -y install apache2`

- /etc/apache2 以下にて作業
- apache2.conf に以下追加
```

<Directory /home/pi/Pi-Lightning/htdocs>
	   Options Indexes FollowSymLinks ExecCGI
	   AllowOverride All
	   Require all granted
</Directory>

```
- envvars にて
export APACHE_RUN_USER=pi
export APACHE_RUN_GROUP=pi

- mods-available/cgid.* を mods-enabled 以下にシンボリックリンク
- mods-enabled/mime.conf で、AddHandler cgi-script .cgi の行を有効にする。
- sites-enabled/000-default.conf にて
`  DocumentRoot /home/pi/Pi-Lightning/htdocs`  
とする
