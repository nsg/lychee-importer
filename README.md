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
    -v /mnt/images:/images \
    ghcr.io/nsg/lychee-importer:master
```

This will output shell commands in the form below that you can pipe to bash, save to a file or do whatever is needed.

```bash
/usr/bin/docker exec lychee php artisan lychee:sync --album_id=1234 --import_via_symlink --skip_duplicates -- "/images/dir1"
/usr/bin/docker exec lychee php artisan lychee:sync --album_id=5678 --import_via_symlink --skip_duplicates -- "/images/dir2"
... and so on
```
