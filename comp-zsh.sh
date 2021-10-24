_qs() {
  local cur cword words
  read -cn cword
  read -Ac words
  cur="${words[$cword-1]}"
  if [ "$cur" = "qs" ]; then
    reply=(
      basic system net api image lesson
      u a f cal time pcat fcopy
      top clear go2git mktar untar mkzip unzip unrar mk7z un7z md5 sha1 sha256 sha512 diff
      http netinfo dl wifi upload upgrade
      trans pinyin rmbg smms upimg alioss txcos qiniu weather LG nlp cb pasteme bcv gbc svi svd acg photo bing phi kd loli setu exc zhihu wallhaven lmgtfy d60
      stbg icat v2gif v2mp4 v2mp3 rmaudio i2png i2jpg fmti
    )
  elif [ "$cur" = "dl" ]; then
    reply=(-px -v)
  elif [ "$cur" = "rmbg" ] || [ "$cur" = "LG" ]; then
    reply=(*.jpg *.jpeg *.png *.webp)
  elif [ "$cur" = "smms" ] || [ "$cur" = "upimg" ]; then
    reply=(*.jpg *.jpeg *.png *.gif *.md)
  elif [ "$cur" = "alioss" ] || [ "$cur" = "txcos" ] || [ "$cur" = "qiniu" ]; then
    reply=(-help -up -dl -rm -ls)
  elif [ "$cur" = "cb" ]; then
    reply=(get post)
  elif [ "$cur" = "acg" ] || [ "$cur" = "photo" ] || [ "$cur" = "bing" ] || [ "$cur" = "wallhaven" ]; then
    reply=(-save)
  elif [ "$cur" = "loli" ] || [ "$cur" = "setu" ]; then
    reply=(-save -p)
  else
    reply=(* */* */*/*)
  fi
}

compctl -K _qs qs
