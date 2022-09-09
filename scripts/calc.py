length = 559
test_size = int(round(length * 0.20, 0))
remaining_length = length - test_size
val_size = int(round(remaining_length * 0.20, 0))
train_size = remaining_length - val_size
print(train_size)