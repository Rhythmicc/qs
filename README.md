# QuickStart

## Use QuickStart to simplify the operation in terminal!

| Command                    | Means                                                        |
| :------------------------- | :----------------------------------------------------------- |
| `qs -u [url] `             | open url using default browser                               |
| `qs -a [app/(file...)]`    | open app or open file by app(for MacOS X)                    |
| `qs -f [file...]`          | open file by default app                                     |
| `qs -trans [words]`        | translate the content of `[words]` or the content in clipboard |
| `qs -time`                 | view current time                                            |
| `qs -ftp`                  | start a simple ftp server                                    |
| `qs -top`                  | cpu and memory monitor                                       |
| `qs -rmbg picture`         | remove image background                                      |
| `qs -smms picture/*.md`    | upload images to sm.ms (or replace paths in markdown)        |
| `qs -weather [address]`    | check weather (of address)                                   |
| `qs -dl [urls/""]`         | download file from url(in clipboard)                         |
| `qs -mktar [path]`         | create gzipped archive for path(dir/file)                    |
| `qs -untar [path]`         | extract path.tar.*                                           |
| `qs -mkzip [path]`         | make a zip for path(dir/file)                                |
| `qs -unzip [path]`         | unzip path.zip                                               |
| `qs -upload`               | upload your pypi library                                     |
| `qs -upgrade`              | update qs                                                    |
| `qs -pyuninstaller [name]` | remove files that pyinstaller create                         |

(By the way, if you are the one of China University Of Petroleum(Beijing), run `qs -i` to login school network)

## Some tools for Windows user to normally use qs

- almost have installed automatically by system on Linux/MacOS X

  [tar](http://gnuwin32.sourceforge.net/packages/gtar.htm)

  [zip](http://gnuwin32.sourceforge.net/packages/zip.htm)

  [unzip](http://gnuwin32.sourceforge.net/packages/unzip.htm)

## Some Demo

- rmbg

|                             Raw                              |                         Processed                         |
| :----------------------------------------------------------: | :-------------------------------------------------------: |
| <img src="https://vip1.loli.net/2020/02/29/qwYb2JkSEeIlB9V.jpg" style="zoom:60%;" /> | ![](https://vip1.loli.net/2020/02/29/wTRszv6EofNSr9K.png) |

- smms

  - upload image:

  ```shell
  ➜ Desktop $ qs -smms IMG_4758.jpeg  
  +---------------+--------+------------------------------------------------------+
  |      File     | Status |                         url                          |
  +---------------+--------+------------------------------------------------------+
  | IMG_4758.jpeg |  True  | https://vip1.loli.net/2020/03/01/MkAYliEIx6GHUgt.jpg |
  +---------------+--------+------------------------------------------------------+
  ```

  - Upload images in markdown file, and replace the images path to urls.

  ```shell
  ➜ Desktop $ qs -smms test.md  
  +---------------+--------+-----------------------------------------+
  |      File     | Status |                         url             |
  +---------------+--------+-----------------------------------------+
  |     1.jpg     |  True  | https://vip1.loli.net/2020/03/01/1.jpg  |
  |     2.jpg     |  True  | https://vip1.loli.net/2020/03/01/2.jpg  |
  |     3.jpg     |  True  | https://vip1.loli.net/2020/03/01/3.jpg  |
  +---------------+--------+-----------------------------------------+
  ```

