ans_num = ??? # INPUT YOUR ANSWER HERE

# -------- DO NOT MODIFY ANY CODE BEYOND THIS POINT --------
checknums = [2,2,2,2,2,3,3,2,3,2,3,2,3,2,3,2,3,3,2,3,2,3,2,3,2,2,3]
ans_num_str = str(ans_num)

if len(ans_num_str) != sum(checknums):
    print("FAILED: Your answer does not match the checknums")

ans_num_split = ""
for i, n in enumerate(checknums):
    ans_num_split += ans_num_str[:n] + " "
    ans_num_str = ans_num_str[n:]

print("PASSED: Your answer matches the checknums")
print("\nPlease decode from Decimal to ASCII the below values:")
print(ans_num_split)

print("\nIf the flag doesn't return after decoding, your answer is incorrect.")
