# Lychee Importer

## Usage

```bash
docker run -ti \
    -e LYCHEE_SERVER_URL="http://127.0.0.1" \
    -e LYCHEE_API_KEY="secret-key" \
    -e LYCHEE_USER="user" \
    -e LYCHEE_PASSWORD="secret-password" \
    -e LYCHEE_CONTAINER_NAME="lychee" \
    -e SOURCE_IMAGES="/images" \
    -e OUTPUT_DIR="/out" \
    -v /mnt/images:/images \
    -v /mnt/out:/out \
    ghcr.io/nsg/lychee-importer:master
```

This will output shell commands in the form below to a script in `{OUTPUT_DIR}/lychee-importer.sh`

```bash
#!/bin/bash

mkdir -p /tmp/lychee-importer-process

ln -s "/sorted/Album A" "/tmp/lychee-importer-process/Album A"
/usr/bin/docker exec lychee php artisan lychee:sync --import_via_symlink --skip_duplicates -- /tmp/lychee-importer-process
rm "/tmp/lychee-importer-process/Album A"

ln -s "/sorted/Album B" "/tmp/lychee-importer-process/Album B"
/usr/bin/docker exec lychee php artisan lychee:sync --album_id=16495929835064 --import_via_symlink --skip_duplicates -- /tmp/lychee-importer-process
rm "/tmp/lychee-importer-process/Album B"
```

Let me explain the script, `lychee:sync` will use the name of the sub folders as album names when `--album_id` is omitted. In the first import, the album will be called "Album A". I can't just run this on `/sorted` because that would create a duplicate "Album B". There is no other easy way to specify the name, hence the crazy symlink hack. In the second import, Album B already exists so I have an ID to work with to prevent duplicate albums.
