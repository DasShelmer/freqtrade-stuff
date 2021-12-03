from replace_ho.replace_ho import replace_ho

src = open("./source_strategy.py")
dist = open("./clear_strategy.py")
log_filepath = "./ho_replace.log"
on_error_copy = True

result = replace_ho(
    src, dist, log_filepath=log_filepath, on_error_copy_src=on_error_copy
)

if result != True:
    print("Error occurred: ", result)
