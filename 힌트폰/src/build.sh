#!/bin/sh
# 힌트폰_논리도.html 전체 다시 만들기 (힌트폰 폴더에서 실행)
set -e
SP="$(dirname "$0")"
python -X utf8 "$SP/assets.py" "$SP/assets_part.html"
cp "$SP/backup_before_screens.html" 힌트폰_논리도.html
python -X utf8 "$SP/screens.py" 힌트폰_논리도.html
python -X utf8 "$SP/flow.py" 힌트폰_논리도.html
python -X utf8 "$SP/post.py" 힌트폰_논리도.html
python -X utf8 "$SP/post_ring.py" 힌트폰_논리도.html
python -X utf8 "$SP/post_assets.py" 힌트폰_논리도.html "$SP/assets_part.html"
python -X utf8 "$SP/post_read.py" 힌트폰_논리도.html
python -X utf8 "$SP/post_ph.py" 힌트폰_논리도.html
python -X utf8 "$SP/proto.py" . "$SP/proto_part.json"
python -X utf8 "$SP/post_proto.py" 힌트폰_논리도.html "$SP/proto_part.json"
python -X utf8 "$SP/opts_btn.py"
python -X utf8 "$SP/post_rules.py" 힌트폰_논리도.html
python -X utf8 "$SP/post_tabs.py" 힌트폰_논리도.html
python -X utf8 "$SP/post_theme.py" 힌트폰_논리도.html
