# Script for replacing HO parameters with their default values.

## How to use:

### CLI:

```
python3 replace_ho.py -s SRC_FILE -d DIST_FILE [-l LOG_FILE --on-error-copy-src]
```

#### Arguments:

- `-h, --help` - info,
- `-s SRC_FILE` - strategy source file,
- `-d DIST_FILE` - strategy destination filepath,
- `-l LOG_FILE` - log file path,
- `--on-error-copy-src` - on error copy source file to destination path.

### As module:

```
from replace_ho import replace_ho

src = open("./source_strategy.py")
dist = open("./clear_strategy.py")
log_filepath = "./ho_replace.log"
on_error_copy = True

result = replace_ho(src, dist, log_filepath=log_filepath, on_error_copy_src=on_error_copy)

if result != True:
    print("Error occurred: ", result)
```
