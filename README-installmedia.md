# インストールメディアについて

## 動作中のシステムのバックアップ

1. SD カード以上の容量がある USB メモリをマウントします。

 - デバイス名は dmesg コマンドでしらべられます。/dev/sda など

- exfat の場合は、追加モジュールをインストールします。
     % sudo apt-get install exfat-fuse

 - コマンドでマウントする場合

     # mount /dev/sda /mnt

2. dd bs=1024k if=/dev/mmcblk0 of=/mnt/lightning.img


## ディスクイメージのリサイズ

同じ容量のSDカードでも、微妙にサイズが違うことがあり、小さいサイズのカードには、大きなイメージを書くことができませんので、不要な部分をカットしてサイズをつめます。

     # cd /mnt
     # ./resizeimage.pl lightning.img


## 新しい SDカードにコピーしてインストール

1. USB を抜き、Mac にさす
2. 新しいSDカードも Mac にさす

     # dd bs=1024k of=/dev/sdbcblk0 of=/mnt/lightning.img

おそいので、一旦 HD にコピーしたほうが良いかも
